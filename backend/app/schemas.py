from typing import List, Optional

from pydantic import BaseModel, Field


# ─── Auth ─────────────────────────────────────────────────────────────────────

class LoginRequest(BaseModel):
    email: str = Field(..., min_length=3)
    password: str = Field(..., min_length=3)
    role: str = Field(..., min_length=3)


class UserResponse(BaseModel):
    name: str
    email: str
    role: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


# ─── Resume ───────────────────────────────────────────────────────────────────

class ResumeAnalysisRequest(BaseModel):
    resume_text: str = Field(..., min_length=1)
    job_description: str = ""


class MatchJobRequest(BaseModel):
    resume_text: str = Field(..., min_length=1)
    job_description: str = Field(..., min_length=1)


class AgentChatRequest(BaseModel):
    message: str = Field(..., min_length=1)
    context: Optional[dict] = None


# ─── Question Generation ──────────────────────────────────────────────────────

class GenerateQuestionsRequest(BaseModel):
    job_role: str = Field(..., min_length=1)
    num_mcq: int = Field(default=5, ge=1, le=10)
    num_theory: int = Field(default=3, ge=1, le=5)
    num_coding: int = Field(default=2, ge=1, le=3)


# ─── Interview Evaluation ─────────────────────────────────────────────────────

class MCQAnswer(BaseModel):
    question_id: int
    question: str
    options: List[str]
    correct_index: int
    selected_index: int


class TheoryAnswer(BaseModel):
    question_id: int
    question: str
    expected_keywords: List[str]
    answer: str


class CodingAnswer(BaseModel):
    question_id: int
    question: str
    function_name: str
    test_cases: List[dict]
    code: str


class FullInterviewRequest(BaseModel):
    candidate_name: str = Field(..., min_length=1)
    job_role: str = Field(..., min_length=1)
    resume_text: str = ""
    job_description: str = ""
    mcq_answers: List[MCQAnswer] = []
    theory_answers: List[TheoryAnswer] = []
    coding_answers: List[CodingAnswer] = []


# Legacy recruiter evaluation (kept for backwards-compat)
class InterviewAnswer(BaseModel):
    question: str = Field(..., min_length=1)
    answer: str = Field(..., min_length=1)


class InterviewEvaluationRequest(BaseModel):
    candidate_name: str = Field(..., min_length=1)
    job_role: str = Field(..., min_length=1)
    answers: List[InterviewAnswer]


# ─── Reports ─────────────────────────────────────────────────────────────────

class CandidateReportSchema(BaseModel):
    id: int
    candidate_name: str
    role: str
    resume_score: int
    interview_score: int
    coding_score: int
    overall_score: int
    recommendation: str
    created_at: Optional[str] = None
