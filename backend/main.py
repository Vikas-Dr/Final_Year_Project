import io
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Optional

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.auth import authenticate_user, create_access_token, get_optional_user, require_role, seed_demo_users
from app.database import (
    Base,
    SessionLocal,
    check_mongo_connection,
    engine,
    get_db,
    save_candidate_profile,
    save_uploaded_file,
)
from app.ai_provider import check_ollama_status, llm_chat_agent, stream_llm_chat_agent
from app.models import User, UserVerification
from app.questions_bank import AVAILABLE_ROLES
from app.schemas import (
    AgentChatRequest,
    FullInterviewRequest,
    GenerateQuestionsRequest,
    InterviewEvaluationRequest,
    LoginResponse,
    LoginRequest,
    MatchJobRequest,
    ResumeAnalysisRequest,
)
from app.services import (
    analyze_resume_text,
    build_dashboard_stats,
    evaluate_full_interview,
    evaluate_interview,
    extract_text_from_file,
    generate_pdf_report,
    generate_questions,
    get_report_by_id,
    load_reports,
    save_report,
    verify_identity_images,
)

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

BASE_DIR = Path(__file__).resolve().parent.parent
UPLOAD_DIR = Path(os.getenv("UPLOAD_DIR", str(BASE_DIR / "uploads")))
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

app = FastAPI(
    title="AI-Powered Interview Evaluation & Resume Analysis System",
    version="2.0.0",
    description="Final Year Project — AI recruitment intelligence platform",
)

CORS_ORIGINS = os.getenv("CORS_ORIGINS", "").split(",")
CORS_ORIGINS = [o.strip() for o in CORS_ORIGINS if o.strip()]
CORS_ORIGINS += [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://vikas-dr.github.io",
    "https://Vikas-Dr.github.io",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_origin_regex=r"https://.*\.github\.io",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup() -> None:
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_demo_users(db)
    finally:
        db.close()
    
    mongo_health = check_mongo_connection()
    print(f"[*] MongoDB Status: {mongo_health.get('status')} ({mongo_health.get('url', 'N/A')})")


# ─────────────────────────────────────────────────────────────────────────────
# Health & DB Status
# ─────────────────────────────────────────────────────────────────────────────

@app.get("/")
def root() -> dict:
    return {
        "message": "AI-Powered Interview Evaluation & Resume Analysis API is running!",
        "version": "2.0.0",
        "docs": "/docs",
        "health": "/health",
    }


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "version": "2.0.0"}


@app.get("/db-status")
def db_status() -> dict:
    mongo_info = check_mongo_connection()
    return {
        "sql_database": {"status": "connected", "engine": str(engine.url)},
        "mongodb": mongo_info,
    }


@app.get("/ai-status")
def ai_status() -> dict:
    provider = os.getenv("AI_PROVIDER", "rule-based")
    ollama_info = check_ollama_status()
    return {
        "configured_provider": provider,
        "ollama": ollama_info,
    }


# ─────────────────────────────────────────────────────────────────────────────
# Auth
# ─────────────────────────────────────────────────────────────────────────────

@app.post("/auth/login", response_model=LoginResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)) -> dict:
    user = authenticate_user(db, request.email, request.password, request.role.lower())
    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    return {
        "access_token": create_access_token(user),
        "token_type": "bearer",
        "user": {"name": user.name, "email": user.email, "role": user.role},
    }


@app.get("/auth/me")
def auth_me(current_user: User = Depends(require_role("candidate", "recruiter"))) -> dict:
    return {"name": current_user.name, "email": current_user.email, "role": current_user.role}


# ─────────────────────────────────────────────────────────────────────────────
# Identity Verification Gate
# ─────────────────────────────────────────────────────────────────────────────

@app.post("/verification/verify")
async def verify_identity(
    id_image: UploadFile = File(...),
    selfie_image: UploadFile = File(...),
    current_user: User = Depends(require_role("candidate", "recruiter")),
    db: Session = Depends(get_db),
) -> dict:
    allowed_types = {"image/jpeg", "image/png", "image/jpg"}
    for file_obj in (id_image, selfie_image):
        if file_obj.content_type not in allowed_types:
            raise HTTPException(status_code=400, detail=f"Unsupported file type for {file_obj.filename}. Use JPG or PNG.")

    verification_dir = UPLOAD_DIR / "verification" / str(current_user.id)
    verification_dir.mkdir(parents=True, exist_ok=True)

    id_bytes = await id_image.read()
    selfie_bytes = await selfie_image.read()

    id_path = verification_dir / f"id_{current_user.id}_{int(datetime.now(timezone.utc).timestamp())}.png"
    selfie_path = verification_dir / f"selfie_{current_user.id}_{int(datetime.now(timezone.utc).timestamp())}.png"

    id_path.write_bytes(id_bytes)
    selfie_path.write_bytes(selfie_bytes)

    mongo_id = save_uploaded_file(id_bytes, id_path.name, {
        "user_id": current_user.id,
        "user_email": current_user.email,
        "document_type": "id_card",
        "stored_local_path": str(id_path),
    })
    mongo_selfie_id = save_uploaded_file(selfie_bytes, selfie_path.name, {
        "user_id": current_user.id,
        "user_email": current_user.email,
        "document_type": "selfie",
        "stored_local_path": str(selfie_path),
    })

    result = verify_identity_images(str(id_path), str(selfie_path))
    status = "verified" if result["verified"] else "rejected"
    reason = result["reason"] if not result["verified"] else None

    verification = db.query(UserVerification).filter(UserVerification.user_id == current_user.id).first()
    if verification is None:
        verification = UserVerification(user_id=current_user.id)
        db.add(verification)

    verification.status = status
    verification.similarity_score = float(result["score"])
    verification.rejection_reason = reason
    verification.id_card_path = str(id_path)
    verification.selfie_path = str(selfie_path)
    verification.verified_at = datetime.now(timezone.utc) if result["verified"] else None
    db.commit()
    db.refresh(verification)

    save_candidate_profile({
        "user_id": current_user.id,
        "email": current_user.email,
        "name": current_user.name,
        "role": current_user.role,
        "verification": {
            "status": status,
            "similarity_score": float(result["score"]),
            "id_card_path": str(id_path),
            "selfie_path": str(selfie_path),
            "id_card_mongo_id": mongo_id,
            "selfie_mongo_id": mongo_selfie_id,
            "verified_at": datetime.now(timezone.utc).isoformat() if result["verified"] else None,
            "rejection_reason": reason,
        },
    })

    return {
        "status": status,
        "verified": result["verified"],
        "score": result["score"],
        "liveness_passed": result["liveness_passed"],
        "message": result["reason"],
    }


@app.get("/verification/status")
def get_verification_status(
    current_user: User = Depends(require_role("candidate", "recruiter")),
    db: Session = Depends(get_db),
) -> dict:
    record = db.query(UserVerification).filter(UserVerification.user_id == current_user.id).order_by(UserVerification.created_at.desc()).first()
    if record is None:
        return {"status": "pending", "verified": False, "score": 0.0, "message": "Identity verification has not been completed."}
    return {
        "status": record.status,
        "verified": record.status == "verified",
        "score": float(record.similarity_score or 0.0),
        "message": "Identity verification completed." if record.status == "verified" else (record.rejection_reason or "Verification rejected."),
    }


# ─────────────────────────────────────────────────────────────────────────────
# Dashboard
# ─────────────────────────────────────────────────────────────────────────────

@app.get("/dashboard-stats")
def dashboard_stats(
    current_user: Optional[User] = Depends(get_optional_user),
    db: Session = Depends(get_db),
) -> dict:
    return build_dashboard_stats(db)


# ─────────────────────────────────────────────────────────────────────────────
# Resume
# ─────────────────────────────────────────────────────────────────────────────

@app.post("/upload-resume")
async def upload_resume(
    file: UploadFile = File(...),
    job_description: Optional[str] = Form(None),
    current_user: Optional[User] = Depends(get_optional_user),
    db: Session = Depends(get_db),
) -> dict:
    if not file.filename:
        raise HTTPException(status_code=400, detail="Missing filename")

    user_id = current_user.id if current_user else 1
    user_email = current_user.email if current_user else "candidate@example.com"
    user_name = current_user.name if current_user else "Candidate"
    user_role = current_user.role if current_user else "candidate"

    candidate_dir = UPLOAD_DIR / "candidates" / str(user_id)
    candidate_dir.mkdir(parents=True, exist_ok=True)

    destination = candidate_dir / file.filename
    content = await file.read()
    destination.write_bytes(content)

    mongo_metadata = {
        "user_id": user_id,
        "user_email": user_email,
        "role": user_role,
        "document_type": "resume",
        "original_filename": file.filename,
        "stored_local_path": str(destination),
        "uploaded_at": datetime.now(timezone.utc).isoformat(),
    }
    saved_mongo_id = save_uploaded_file(content, file.filename, mongo_metadata)

    extracted_text = extract_text_from_file(destination)
    analysis = analyze_resume_text(extracted_text, job_description or "")

    candidate_name = analysis.get("candidate_name")
    if not candidate_name or candidate_name in ("Candidate", "Unknown Candidate"):
        candidate_name = user_name

    saved_profile = save_candidate_profile({
        "user_id": user_id,
        "email": user_email,
        "name": candidate_name,
        "role": user_role,
        "resume": {
            "filename": file.filename,
            "stored_path": str(destination),
            "mongo_file_id": saved_mongo_id,
            "uploaded_at": datetime.now(timezone.utc).isoformat(),
        },
        "analysis": analysis,
    })

    # Save report entry in relational database (SQL)
    if not analysis["job_match_available"]:
        rec = "Job description needed"
    else:
        rec = "Highly Recommended" if analysis["job_match_score"] >= 80 else ("Recommended" if analysis["job_match_score"] >= 60 else "Consider with Review")
    saved_report = save_report(db, {
        "candidate_name": candidate_name,
        "role": (job_description[:30] + "...") if job_description and len(job_description) > 30 else (job_description or "General resume review"),
        "resume_score": analysis.get("resume_score", 0),
        "interview_score": 0,
        "coding_score": 0,
        "overall_score": analysis.get("job_match_score", 0) if analysis["job_match_available"] else analysis.get("resume_score", 0),
        "recommendation": rec,
        "feedback": analysis.get("strengths", []) + analysis.get("improvements", []),
        "questions_log": [],
    })

    return {
        "filename": file.filename,
        "stored_path": str(destination),
        "mongo_file_id": saved_mongo_id,
        "extracted_text": extracted_text,
        "analysis": analysis,
        "report_id": saved_report.get("id"),
        "mongo_profile_status": saved_profile.get("status"),
        "mongo_profile_id": saved_profile.get("profile_id"),
        "mongo_profile_message": saved_profile.get("message"),
    }


@app.post("/analyze-resume")
def analyze_resume(
    request: ResumeAnalysisRequest,
    current_user: Optional[User] = Depends(get_optional_user),
) -> dict:
    return analyze_resume_text(request.resume_text, request.job_description)


@app.post("/match-job")
def match_job(
    request: MatchJobRequest,
    current_user: Optional[User] = Depends(get_optional_user),
) -> dict:
    result = analyze_resume_text(request.resume_text, request.job_description)
    return {
        "candidate_name": result["candidate_name"],
        "resume_score": result["resume_score"],
        "job_match_score": result["job_match_score"],
        "job_match_available": result["job_match_available"],
        "matched_skills": result["matched_skills"],
        "missing_skills": result["missing_skills"],
        "recommendation": (
            "Job description needed" if not result["job_match_available"]
            else "Good fit" if result["job_match_score"] >= 70
            else "Needs closer review"
        ),
    }


@app.post("/agent-chat/stream")
def stream_agent_chat(
    request: AgentChatRequest,
    current_user: Optional[User] = Depends(get_optional_user),
) -> StreamingResponse:
    user_context = dict(request.context or {})
    if current_user:
        user_context["user_name"] = current_user.name
        user_context["user_role"] = current_user.role

    def events():
        for event in stream_llm_chat_agent(request.message, user_context):
            yield json.dumps(event, ensure_ascii=False) + "\n"

    return StreamingResponse(
        events(),
        media_type="application/x-ndjson",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


@app.post("/agent-chat")
def agent_chat(
    request: AgentChatRequest,
    current_user: Optional[User] = Depends(get_optional_user),
) -> dict:
    user_context = request.context or {}
    if current_user:
        user_context["user_name"] = current_user.name
        user_context["user_role"] = current_user.role
    return llm_chat_agent(request.message, user_context)


# ─────────────────────────────────────────────────────────────────────────────
# Question Generation
# ─────────────────────────────────────────────────────────────────────────────

@app.get("/available-roles")
def available_roles() -> dict:
    return {"roles": AVAILABLE_ROLES}


@app.post("/generate-questions")
def generate_interview_questions(
    request: GenerateQuestionsRequest,
    current_user: Optional[User] = Depends(get_optional_user),
) -> dict:
    return generate_questions(
        request.job_role,
        request.num_mcq,
        request.num_theory,
        request.num_coding,
    )


# ─────────────────────────────────────────────────────────────────────────────
# Full Interview Evaluation (Candidate Flow)
# ─────────────────────────────────────────────────────────────────────────────

@app.post("/evaluate-full-interview")
def evaluate_full(
    request: FullInterviewRequest,
    current_user: Optional[User] = Depends(get_optional_user),
    db: Session = Depends(get_db),
) -> dict:
    evaluation = evaluate_full_interview(
        candidate_name=request.candidate_name,
        job_role=request.job_role,
        resume_text=request.resume_text,
        job_description=request.job_description,
        mcq_answers=[a.model_dump() for a in request.mcq_answers],
        theory_answers=[a.model_dump() for a in request.theory_answers],
        coding_answers=[a.model_dump() for a in request.coding_answers],
    )
    report = save_report(
        db,
        {
            "candidate_name": evaluation["candidate_name"],
            "role": evaluation["job_role"],
            "resume_score": evaluation["resume_score"],
            "interview_score": evaluation["interview_score"],
            "coding_score": evaluation["coding_score"],
            "overall_score": evaluation["overall_score"],
            "recommendation": evaluation["recommendation"],
            "feedback": evaluation["feedback"],
            "questions_log": evaluation["questions_log"],
        },
    )
    return {"evaluation": evaluation, "report": report}


# ─────────────────────────────────────────────────────────────────────────────
# Legacy Recruiter Evaluation
# ─────────────────────────────────────────────────────────────────────────────

@app.post("/evaluate-interview")
def evaluate(
    request: InterviewEvaluationRequest,
    current_user: Optional[User] = Depends(get_optional_user),
    db: Session = Depends(get_db),
) -> dict:
    evaluation = evaluate_interview(
        request.candidate_name,
        request.job_role,
        [answer.model_dump() for answer in request.answers],
    )
    report = save_report(
        db,
        {
            "candidate_name": request.candidate_name,
            "role": request.job_role,
            "resume_score": max(evaluation["technical_score"] - 5, 0),
            "interview_score": evaluation["overall_score"],
            "coding_score": 0,
            "overall_score": evaluation["overall_score"],
            "recommendation": evaluation["recommendation"],
            "feedback": evaluation["feedback"],
            "questions_log": [],
        },
    )
    return {"evaluation": evaluation, "report": report}


# ─────────────────────────────────────────────────────────────────────────────
# Reports
# ─────────────────────────────────────────────────────────────────────────────

@app.get("/reports")
def list_reports(
    current_user: Optional[User] = Depends(get_optional_user),
    db: Session = Depends(get_db),
) -> List[dict]:
    return load_reports(db)


@app.get("/candidate-report/{report_id}")
def candidate_report(
    report_id: int,
    current_user: Optional[User] = Depends(get_optional_user),
    db: Session = Depends(get_db),
) -> dict:
    report = get_report_by_id(db, report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    return report


@app.get("/report/{report_id}/pdf")
def download_report_pdf(
    report_id: int,
    current_user: Optional[User] = Depends(get_optional_user),
    db: Session = Depends(get_db),
) -> StreamingResponse:
    report = get_report_by_id(db, report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    try:
        pdf_bytes = generate_pdf_report(report)
    except RuntimeError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    candidate = report.get("candidate_name", "candidate").replace(" ", "_")
    filename = f"report_{candidate}_{report_id}.pdf"
    return StreamingResponse(
        io.BytesIO(pdf_bytes),
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )
