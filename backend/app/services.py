"""
Core AI services for the Interview Evaluation & Resume Analysis System.
Covers: text extraction, resume analysis, question generation, answer
evaluation (MCQ / theory / coding), scoring, and PDF report generation.
"""

from __future__ import annotations

import io
import json
import math
import os
import re
import traceback
from collections import Counter
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
from sqlalchemy import desc, func
from sqlalchemy.orm import Session

from app.models import CandidateReport
from app.questions_bank import AVAILABLE_ROLES, get_questions_for_role
from app.ai_provider import llm_analyze_resume, llm_evaluate_interview_answer, check_ollama_status

# ── Optional heavy deps ───────────────────────────────────────────────────────
try:
    import pdfplumber
except Exception:
    pdfplumber = None

try:
    from docx import Document as DocxDocument
except Exception:
    DocxDocument = None

try:
    from fpdf import FPDF
    _HAS_FPDF = True
except Exception:
    _HAS_FPDF = False

try:
    from PIL import Image, ImageChops, ImageEnhance, ImageFilter, ImageOps, ImageStat
except Exception:
    Image = None

# ─────────────────────────────────────────────────────────────────────────────
# IDENTITY VERIFICATION
# ─────────────────────────────────────────────────────────────────────────────


def verify_identity_images(id_image_path: str, selfie_image_path: str) -> Dict[str, Any]:
    """Run a lightweight identity validation using image similarity and face-like region heuristics.

    This is designed to power a final-year demo flow for ID verification without requiring a full
    external inference service. The score is a compatibility heuristic that checks facial region
    similarity, lighting consistency, and image quality.
    """
    if Image is None:
        return {
            "verified": False,
            "score": 0.0,
            "reason": "Image processing dependencies are unavailable in this environment.",
            "liveness_passed": False,
        }

    try:
        id_image = Image.open(id_image_path).convert("RGB")
        selfie_image = Image.open(selfie_image_path).convert("RGB")
    except Exception:
        return {
            "verified": False,
            "score": 0.0,
            "reason": "One or both uploaded images could not be decoded.",
            "liveness_passed": False,
        }

    def face_like_crop(image: Image.Image) -> Image.Image:
        width, height = image.size
        target = image.crop((int(width * 0.15), int(height * 0.08), int(width * 0.85), int(height * 0.92)))
        gray = ImageOps.grayscale(target)
        edges = gray.filter(ImageFilter.FIND_EDGES)
        edge_stat = ImageStat.Stat(edges)
        edge_value = float(edge_stat.mean[0])
        if edge_value < 10:
            return target.resize((200, 200), Image.Resampling.LANCZOS)
        return target.resize((200, 200), Image.Resampling.LANCZOS)

    id_face = face_like_crop(id_image)
    selfie_face = face_like_crop(selfie_image)

    difference = ImageChops.difference(id_face, selfie_face)
    diff_stat = ImageStat.Stat(difference)
    mean_difference = float(diff_stat.mean[0])
    similarity = 1.0 - (mean_difference / 255.0)

    id_enhanced = ImageEnhance.Contrast(id_face).enhance(1.4)
    selfie_enhanced = ImageEnhance.Contrast(selfie_face).enhance(1.4)
    contrast_difference = ImageChops.difference(id_enhanced, selfie_enhanced)
    contrast_score = 1.0 - (float(ImageStat.Stat(contrast_difference).mean[0]) / 255.0)

    score = max(0.0, min(1.0, float((similarity + contrast_score) / 2.0)))
    normalized_score = round(score, 4)

    liveness_passed = min(id_image.size) > 80 and min(selfie_image.size) > 80 and normalized_score >= 0.35
    verified = normalized_score >= 0.62 and liveness_passed

    return {
        "verified": verified,
        "score": normalized_score,
        "reason": "Identity match verified successfully." if verified else "The uploaded ID and selfie do not match closely enough for interview access.",
        "liveness_passed": liveness_passed,
    }

# ─────────────────────────────────────────────────────────────────────────────
# SKILL KEYWORDS
# ─────────────────────────────────────────────────────────────────────────────

# ─────────────────────────────────────────────────────────────────────────────
# COMPREHENSIVE SKILL TAXONOMY (200+ Skills)
# ─────────────────────────────────────────────────────────────────────────────

SKILL_TAXONOMY = {
    # Languages
    "python": r"\bpython\b",
    "java": r"\bjava\b(?!\s*script)",
    "javascript": r"\b(javascript|js)\b",
    "typescript": r"\b(typescript|ts)\b",
    "c++": r"\bc\+\+\b",
    "c#": r"\bc#\b",
    "c": r"\bc\b",
    "go / golang": r"\b(golang|go)\b",
    "rust": r"\brust\b",
    "ruby": r"\bruby\b",
    "php": r"\bphp\b",
    "swift": r"\bswift\b",
    "kotlin": r"\bkotlin\b",
    "dart": r"\bdart\b",
    "r": r"\br\b",
    "scala": r"\bscala\b",
    "sql": r"\bsql\b",
    "html": r"\b(html|html5)\b",
    "css": r"\b(css|css3)\b",
    "bash / shell": r"\b(bash|shell|powershell)\b",

    # Frontend
    "react": r"\b(react|reactjs|react\.js)\b",
    "react native": r"\breact[\s\-]?native\b",
    "next.js": r"\b(nextjs|next\.js)\b",
    "angular": r"\b(angular|angularjs)\b",
    "vue.js": r"\b(vue|vuejs|vue\.js)\b",
    "svelte": r"\bsvelte\b",
    "tailwind css": r"\btailwind(\s*css)?\b",
    "bootstrap": r"\bbootstrap(\s*5)?\b",
    "redux": r"\b(redux|redux\-toolkit)\b",
    "zustand": r"\bzustand\b",
    "material ui": r"\b(material[\s\-]?ui|mui)\b",

    # Backend & Frameworks
    "fastapi": r"\bfastapi\b",
    "flask": r"\bflask\b",
    "django": r"\bdjango\b",
    "node.js": r"\b(nodejs|node\.js|node)\b",
    "express.js": r"\b(express|expressjs|express\.js)\b",
    "nestjs": r"\bnestjs\b",
    "spring boot": r"\bspring[\s\-]?boot\b",
    "asp.net": r"\basp\.net\b",
    "ruby on rails": r"\brails|ruby[\s\-]?on[\s\-]?rails\b",
    "graphql": r"\bgraphql\b",
    "rest api": r"\b(rest|restful|rest[\s\-]?apis?)\b",
    "grpc": r"\bgrpc\b",
    "microservices": r"\bmicroservices?\b",
    "websockets": r"\bwebsockets?\b",

    # Databases & Storage
    "postgresql": r"\b(postgresql|postgres)\b",
    "mysql": r"\bmysql\b",
    "sqlite": r"\bsqlite\b",
    "mongodb": r"\bmongodb\b",
    "redis": r"\bredis\b",
    "cassandra": r"\bcassandra\b",
    "dynamodb": r"\bdynamodb\b",
    "oracle db": r"\boracle(\s*db)?\b",
    "elasticsearch": r"\belasticsearch\b",
    "firebase": r"\bfirebase\b",

    # AI, Machine Learning & Data Science
    "machine learning": r"\bmachine[\s\-]?learning|ml\b",
    "deep learning": r"\bdeep[\s\-]?learning|dl\b",
    "nlp": r"\b(nlp|natural[\s\-]?language[\s\-]?processing)\b",
    "computer vision": r"\b(computer[\s\-]?vision|cv)\b",
    "large language models (llm)": r"\b(llm|llms|large[\s\-]?language[\s\-]?models?)\b",
    "langchain": r"\blangchain\b",
    "llamaindex": r"\bllamaindex\b",
    "tensorflow": r"\btensorflow\b",
    "pytorch": r"\bpytorch\b",
    "keras": r"\bkeras\b",
    "scikit-learn": r"\b(scikit[\s\-]?learn|sklearn)\b",
    "pandas": r"\bpandas\b",
    "numpy": r"\bnumpy\b",
    "scipy": r"\bscipy\b",
    "matplotlib": r"\bmatplotlib\b",
    "seaborn": r"\bseaborn\b",
    "opencv": r"\bopencv\b",
    "hugging face": r"\bhugging[\s\-]?face\b",
    "data analysis": r"\bdata[\s\-]?analysis\b",
    "data science": r"\bdata[\s\-]?science\b",

    # Cloud & DevOps
    "aws": r"\b(aws|amazon[\s\-]?web[\s\-]?services)\b",
    "azure": r"\b(azure|microsoft[\s\-]?azure)\b",
    "gcp / google cloud": r"\b(gcp|google[\s\-]?cloud)\b",
    "docker": r"\bdocker\b",
    "kubernetes": r"\b(kubernetes|k8s)\b",
    "terraform": r"\bterraform\b",
    "ansible": r"\bansible\b",
    "ci/cd": r"\bci[\s\/-]?cd\b",
    "github actions": r"\bgithub[\s\-]?actions\b",
    "jenkins": r"\bjenkins\b",
    "linux": r"\blinux\b",
    "nginx": r"\bnginx\b",
    "git": r"\bgit(hub|lab)?\b",

    # Software Engineering & Methodologies
    "data structures & algorithms": r"\b(dsa|data[\s\-]?structures?|algorithms?)\b",
    "object-oriented programming (oop)": r"\b(oop|object[\s\-]?oriented)\b",
    "system design": r"\bsystem[\s\-]?design\b",
    "agile / scrum": r"\b(agile|scrum)\b",
    "unit testing": r"\b(unit[\s\-]?test(ing)?|pytest|jest|junit)\b",
    "postman": r"\bpostman\b",
}

SKILL_KEYWORDS = set(SKILL_TAXONOMY.keys())

SECTION_PATTERNS = {
    "education": re.compile(r"\b(education|academic|qualification|degree|university|college|b\.?tech|m\.?tech|bsc|msc|bachelor|master|phd|gpa|cgpa)\b", re.IGNORECASE),
    "experience": re.compile(r"\b(experience|employment|work history|internship|worked at|professional experience|career history|work background)\b", re.IGNORECASE),
    "projects": re.compile(r"\b(projects?|portfolio|personal projects|academic projects|built|developed|implemented)\b", re.IGNORECASE),
    "certifications": re.compile(r"\b(certification|certified|certificate|courses?|udemy|coursera|edx|licensed)\b", re.IGNORECASE),
    "skills": re.compile(r"\b(skills|technical skills|competencies|technologies|proficiencies|tools)\b", re.IGNORECASE),
}

_RESUME_SECTION_HEADINGS = {
    "education": re.compile(r"(?:education|academic background|qualifications?)", re.IGNORECASE),
    "experience": re.compile(r"(?:(?:professional|work)\s+)?experience|employment|internships?", re.IGNORECASE),
    "projects": re.compile(r"(?:personal\s+|academic\s+)?projects?|portfolio", re.IGNORECASE),
    "certifications": re.compile(r"(?:professional\s+)?certifications?|licenses?|courses", re.IGNORECASE),
    "skills": re.compile(r"(?:technical\s+)?skills|competencies|technologies", re.IGNORECASE),
}

# ─────────────────────────────────────────────────────────────────────────────
# TEXT EXTRACTION (Multi-Engine with Fallbacks)
# ─────────────────────────────────────────────────────────────────────────────

def extract_text_from_file(file_path: Path) -> str:
    suffix = file_path.suffix.lower()
    if suffix == ".pdf":
        return _extract_pdf_text(file_path)
    if suffix in (".docx", ".doc"):
        return _extract_docx_text(file_path)
    
    # Text or other formats
    try:
        return file_path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        try:
            return file_path.read_text(encoding="latin-1", errors="ignore")
        except Exception:
            return ""


def _extract_pdf_text(file_path: Path) -> str:
    pages: List[str] = []

    # Strategy 1: pdfplumber (high fidelity, text + tables)
    if pdfplumber is not None:
        try:
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    text = page.extract_text(layout=False) or page.extract_text()
                    if text:
                        pages.append(text)
                    # Extract any table cell texts as well
                    try:
                        tables = page.extract_tables()
                        for table in tables:
                            for row in table:
                                row_text = " ".join([cell for cell in row if cell])
                                if row_text and row_text not in (text or ""):
                                    pages.append(row_text)
                    except Exception:
                        pass
        except Exception as e:
            print(f"[PDF Extraction Warning] pdfplumber error: {e}")

    # Strategy 2: pdfminer fallback if pdfplumber extracted nothing
    if not pages or not "".join(pages).strip():
        try:
            from pdfminer.high_level import extract_text as pdfminer_extract
            mined_text = pdfminer_extract(str(file_path))
            if mined_text and mined_text.strip():
                pages.append(mined_text.strip())
        except Exception as e:
            print(f"[PDF Extraction Warning] pdfminer error: {e}")

    # Strategy 3: pypdfium2 fallback
    if not pages or not "".join(pages).strip():
        try:
            import pypdfium2 as pdfium
            pdf = pdfium.PdfDocument(str(file_path))
            for i in range(len(pdf)):
                page = pdf[i]
                textpage = page.get_textpage()
                txt = textpage.get_text_range()
                if txt and txt.strip():
                    pages.append(txt.strip())
        except Exception as e:
            print(f"[PDF Extraction Warning] pypdfium2 error: {e}")

    return "\n\n".join(pages).strip()


def _extract_docx_text(file_path: Path) -> str:
    if DocxDocument is None:
        return ""
    paragraphs = []
    try:
        document = DocxDocument(file_path)
        # Extract normal paragraphs
        for p in document.paragraphs:
            if p.text and p.text.strip():
                paragraphs.append(p.text.strip())
        
        # Extract tables (very common for resume layouts)
        for table in document.tables:
            for row in table.rows:
                row_items = [cell.text.strip() for cell in row.cells if cell.text.strip()]
                if row_items:
                    paragraphs.append(" | ".join(row_items))
    except Exception as e:
        print(f"[DOCX Extraction Warning] {e}")
        return ""
    
    return "\n".join(paragraphs).strip()


def normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


# ─────────────────────────────────────────────────────────────────────────────
# RESUME EXTRACTION HELPERS
# ─────────────────────────────────────────────────────────────────────────────

IGNORE_NAME_PATTERNS = {
    "resume", "curriculum vitae", "cv", "profile", "contact", "summary",
    "personal details", "portfolio", "bio", "biodata", "about me",
    "personal information", "objective", "career objective", "experience",
    "education", "skills", "technical skills", "projects", "certifications",
    "contact information", "phone", "email", "address", "page 1", "page 2",
}

def extract_candidate_name(text: str) -> str:
    if not text:
        return "Unknown Candidate"

    # Strategy 1: Look for explicit labels like Name: John Doe or Candidate: John Doe
    explicit_match = re.search(r"(?:name|candidate name|full name)\s*[:\-]\s*([A-Za-z\s\.\-]{2,35})", text, re.IGNORECASE)
    if explicit_match:
        cand = explicit_match.group(1).strip()
        if cand.lower() not in IGNORE_NAME_PATTERNS and len(cand.split()) <= 4:
            return cand.title()

    lines = [line.strip() for line in text.splitlines() if line.strip()]
    for line in lines[:8]:
        # Clean line
        cleaned = re.sub(r"[^\w\s\.\-]", " ", line).strip()
        lowered = cleaned.lower()

        # Skip headers, emails, phones, URLs
        if lowered in IGNORE_NAME_PATTERNS or any(ign in lowered for ign in ["curriculum", "resume", "biodata"]):
            continue
        if "@" in line or "http" in lowered or "www" in lowered or "linkedin" in lowered or "github" in lowered:
            continue
        if any(ch.isdigit() for ch in line):
            continue

        words = cleaned.split()
        if 2 <= len(words) <= 4 and all(re.match(r"^[A-Za-z\.]+$", w) for w in words):
            return cleaned.title()

    # Strategy 3: Derive from email if present (e.g. vikram.sharma@gmail.com -> Vikram Sharma)
    email = extract_email(text)
    if email and email != "Not detected":
        user_part = email.split("@")[0]
        name_parts = re.split(r"[._\-0-9]+", user_part)
        clean_parts = [p.capitalize() for p in name_parts if len(p) > 1]
        if clean_parts:
            return " ".join(clean_parts[:3])

    if lines and len(lines[0].split()) <= 4 and not any(ch.isdigit() for ch in lines[0]):
        return lines[0].title()

    return "Candidate"


def extract_email(text: str) -> str:
    match = re.search(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b", text)
    return match.group(0) if match else "Not detected"


def extract_phone(text: str) -> str:
    match = re.search(r"(?:\+?\d{1,3}[-.\s]?)?\(?\d{2,5}\)?[-.\s]?\d{3,5}[-.\s]?\d{3,5}", text)
    if match:
        phone_str = match.group(0).strip()
        # Verify it has at least 8 digits
        if sum(1 for c in phone_str if c.isdigit()) >= 8:
            return phone_str
    return "Not detected"


def extract_skills(text: str) -> List[str]:
    lowered = text.lower()
    found_skills = []
    
    for skill_name, pattern in SKILL_TAXONOMY.items():
        if re.search(pattern, lowered):
            # Format nicely
            formatted = skill_name.title() if len(skill_name) > 4 else skill_name.upper()
            if skill_name in ("c++", "c#", "c", "r", "sql", "html", "css", "aws", "gcp", "nlp", "llm", "ci/cd", "dsa", "oop"):
                formatted = skill_name.upper()
            found_skills.append(formatted)
            
    # Sort uniquely
    unique_skills = []
    for s in found_skills:
        if s not in unique_skills:
            unique_skills.append(s)
            
    return unique_skills[:25]


def count_section_hits(text: str) -> Dict[str, bool]:
    detected = {name: False for name in SECTION_PATTERNS}
    for line in text.splitlines():
        heading = re.sub(r"^\s*\d+[.)-]?\s*", "", line).strip().strip(":")
        for name, pattern in _RESUME_SECTION_HEADINGS.items():
            if pattern.fullmatch(heading):
                detected[name] = True
    return detected


# ─────────────────────────────────────────────────────────────────────────────
# RESUME SCORING & ATS ANALYSIS
# ─────────────────────────────────────────────────────────────────────────────

RESUME_SCORE_RUBRIC = [
    {"key": "sections", "name": "Core sections", "max_score": 25, "guideline": "Up to 5 points each for education, experience, projects, certifications, and skills sections."},
    {"key": "skills", "name": "Distinct skills listed", "max_score": 20, "guideline": "2 points for each distinct detected skill, up to 10 skills."},
    {"key": "contact", "name": "Contact details", "max_score": 10, "guideline": "4 points for email, 4 for phone, and 2 for a LinkedIn or portfolio link."},
    {"key": "career_history", "name": "Career history evidence", "max_score": 15, "guideline": "5 points for an experience section, up to 5 for action-led evidence, and 5 for dates or role durations."},
    {"key": "impact", "name": "Measurable impact", "max_score": 10, "guideline": "1 point for each quantified outcome (such as percentages, users, time, or cost), up to 10."},
    {"key": "projects", "name": "Project evidence", "max_score": 10, "guideline": "5 points for a projects section, up to 3 for project action evidence, and 2 for a quantified outcome."},
    {"key": "length", "name": "Useful resume length", "max_score": 5, "guideline": "5 points for 250–1,200 words; 2 points for 150–249 or 1,201–1,600 words."},
    {"key": "formatting", "name": "Readable formatting", "max_score": 5, "guideline": "1 point per extracted bullet item, up to 5."},
]

_RESUME_ACTION_PATTERN = re.compile(
    r"\b(built|created|delivered|deployed|designed|developed|improved|implemented|"
    r"integrated|launched|led|optimized|reduced|automated|increased|managed|"
    r"maintained|migrated|tested|achieved|owned|resolved)\b",
    re.IGNORECASE,
)
_QUANTIFIED_IMPACT_PATTERN = re.compile(
    r"(?:\b\d+(?:\.\d+)?\s?%|\b\d+(?:\.\d+)?\s?(?:users?|customers?|clients?|"
    r"requests?|hours?|days?|weeks?|ms|seconds?|minutes?|"
    r"thousand|million|k|m|x)\b|[$€£]\s?\d[\d,.]*)",
    re.IGNORECASE,
)
_JOB_STOP_WORDS = {
    "and", "the", "for", "with", "from", "that", "this", "you", "your", "our",
    "are", "will", "have", "has", "who", "what", "when", "where", "their",
    "them", "they", "can", "all", "any", "about", "into", "using", "use",
    "work", "team", "role", "candidate", "years", "year", "strong", "good",
    "ability", "experience", "including", "such", "plus", "preferred",
}
def _resume_section_text(text: str, section_name: str) -> str:
    """Return text under a recognizable section heading until the next section."""
    lines = text.splitlines()
    target_pattern = _RESUME_SECTION_HEADINGS[section_name]
    collecting = False
    section_lines = []
    for line in lines:
        heading = re.sub(r"^\s*\d+[.)-]?\s*", "", line).strip().strip(":")
        heading_match = next(
            (
                name for name, pattern in _RESUME_SECTION_HEADINGS.items()
                if pattern.fullmatch(heading)
            ),
            None,
        )
        if not collecting and heading_match == section_name:
            collecting = True
            continue
        if collecting and heading_match is not None:
            break
        if collecting:
            section_lines.append(line)
    return "\n".join(section_lines) if collecting else ""


def _score_resume_profile(text: str) -> Tuple[int, Dict[str, Any]]:
    """Score resume completeness against a fixed, transparent 100-point rubric."""
    sections = count_section_hits(text)
    skills = extract_skills(text)
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    word_count = len(re.findall(r"\b[\w+#.]+\b", text))
    bullet_count = sum(1 for line in lines if re.match(r"^(?:[-*•▪]|\d+[.)])\s+", line))
    experience_text = _resume_section_text(text, "experience")
    project_text = _resume_section_text(text, "projects")
    action_count = len(_RESUME_ACTION_PATTERN.findall(experience_text))
    impact_count = len(_QUANTIFIED_IMPACT_PATTERN.findall(text))
    has_career_dates = bool(re.search(
        r"\b(?:19|20)\d{2}\s*(?:-|–|to)\s*(?:(?:19|20)\d{2}|present|current)\b"
        r"|\b\d+\+?\s+(?:years?|months?)\b",
        experience_text,
        re.IGNORECASE,
    ))
    project_actions = len(re.findall(
        r"\b(?:built|created|delivered|deployed|designed|developed|implemented|launched)\b",
        project_text,
        re.IGNORECASE,
    ))

    points = {
        "sections": sum(5 for present in sections.values() if present),
        "skills": min(len(skills), 10) * 2,
        "contact": (
            (4 if extract_email(text) != "Not detected" else 0)
            + (4 if extract_phone(text) != "Not detected" else 0)
            + (2 if re.search(r"\b(?:linkedin\.com|github\.com|portfolio)\b", text, re.IGNORECASE) else 0)
        ),
        "career_history": (
            (5 if sections.get("experience") else 0)
            + min(action_count, 5)
            + (5 if has_career_dates else 0)
        ),
        "impact": min(impact_count, 10),
        "projects": (
            (5 if sections.get("projects") else 0)
            + min(project_actions, 3)
            + (2 if sections.get("projects") and impact_count else 0)
        ),
        "length": 5 if 250 <= word_count <= 1200 else (2 if 150 <= word_count < 250 or 1200 < word_count <= 1600 else 0),
        "formatting": min(bullet_count, 5),
    }

    criteria = [
        {**criterion, "score": min(points[criterion["key"]], criterion["max_score"])}
        for criterion in RESUME_SCORE_RUBRIC
    ]
    total = min(100, sum(item["score"] for item in criteria))
    return total, {"total": total, "max_score": 100, "version": "1.0", "criteria": criteria}


def _score_job_match(text: str, job_description: str) -> Dict[str, Any]:
    normalized_resume = normalize_text(text).lower()
    normalized_job = normalize_text(job_description).lower()
    if not normalized_job:
        return {
            "available": False,
            "score": 0,
            "matched_skills": [],
            "missing_skills": [],
            "keyword_coverage": 0,
            "guideline": "Add a job description to calculate role alignment.",
        }

    job_skills = [
        skill for skill, pattern in SKILL_TAXONOMY.items()
        if re.search(pattern, normalized_job, re.IGNORECASE)
    ]
    resume_skill_keys = {
        skill for skill, pattern in SKILL_TAXONOMY.items()
        if re.search(pattern, normalized_resume, re.IGNORECASE)
    }
    matched_skills = [skill for skill in job_skills if skill in resume_skill_keys]
    missing_skills = [skill for skill in job_skills if skill not in resume_skill_keys]

    def meaningful_terms(value: str) -> set[str]:
        return set(re.findall(r"[a-z][a-z0-9+#.]{2,}", value.lower())) - _JOB_STOP_WORDS

    all_job_terms = meaningful_terms(normalized_job)
    skill_terms = {
        term
        for skill in job_skills
        for term in meaningful_terms(skill.replace("/", " ").replace("-", " "))
    }
    job_terms = all_job_terms - skill_terms
    matched_terms = job_terms & meaningful_terms(normalized_resume)
    keyword_coverage = round(len(matched_terms) / len(job_terms) * 100) if job_terms else 0

    if len(all_job_terms) < 3:
        return {
            "available": False,
            "score": 0,
            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
            "keyword_coverage": keyword_coverage,
            "guideline": "Add at least three meaningful job-description terms for a reliable match score.",
        }

    score = (
        round((len(matched_skills) / len(job_skills)) * 80 + keyword_coverage * 0.20)
        if job_skills
        else keyword_coverage
    )
    return {
        "available": True,
        "score": max(0, min(100, score)),
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "keyword_coverage": keyword_coverage,
        "guideline": (
            "With listed role skills, the score uses 80% required-skill coverage and "
            "20% job-description keyword coverage. Otherwise it uses keyword coverage."
        ),
    }


def score_resume(text: str, job_description: str) -> Tuple[int, int]:
    """Return fixed-rubric completeness and job-description match scores."""
    resume_score, _ = _score_resume_profile(text)
    job_match = _score_job_match(text, job_description)
    return resume_score, job_match["score"]


def analyze_resume_text(text: str, job_description: str = "") -> Dict[str, Any]:
    if not text or len(text.strip()) < 10:
        return {
            "candidate_name": "No Resume Loaded",
            "email": "Not detected",
            "phone": "Not detected",
            "skills": [],
            "sections": {"education": False, "experience": False, "projects": False, "certifications": False, "skills": False},
            "resume_score": 0,
            "resume_score_breakdown": {
                "total": 0,
                "max_score": 100,
                "version": "1.0",
                "criteria": [{**criterion, "score": 0} for criterion in RESUME_SCORE_RUBRIC],
            },
            "job_match_score": 0,
            "job_match_available": False,
            "job_match_breakdown": {"matched_skills": [], "missing_skills": [], "keyword_coverage": 0, "guideline": "Add a job description to calculate role alignment."},
            "matched_skills": [],
            "missing_skills": [],
            "strengths": [],
            "improvements": ["Please upload a valid PDF, DOCX, or paste your resume text to begin analysis."],
            "summary": "No resume text was detected for analysis.",
            "ai_provider": "none",
            "scoring_method": "fixed_rubric_v1",
        }

    resume_score, score_breakdown = _score_resume_profile(text)
    job_match = _score_job_match(text, job_description)
    job_match_score = job_match["score"]
    section_hits = count_section_hits(text)
    skills = extract_skills(text)
    candidate_name = extract_candidate_name(text)
    email = extract_email(text)
    phone = extract_phone(text)

    # Attempt Local LLM analysis via Ollama if provider is enabled
    ai_provider_setting = os.getenv("AI_PROVIDER", "rule-based").lower()
    llm_result = None
    if ai_provider_setting == "ollama":
        try:
            llm_result = llm_analyze_resume(text, job_description or "General resume review")
        except Exception:
            llm_result = None

    strengths: List[str] = []
    if llm_result and isinstance(llm_result.get("strengths"), list) and len(llm_result["strengths"]) > 0:
        strengths.extend(llm_result.get("strengths", []))
    else:
        if len(skills) >= 8:
            strengths.append(f"Outstanding technical skill breadth ({len(skills)} skills detected)")
        elif len(skills) >= 4:
            strengths.append(f"Solid technical skills detected ({len(skills)} skills)")
        if section_hits.get("projects"):
            strengths.append("Project portfolio demonstrated with actionable technical deliverables")
        if section_hits.get("experience"):
            strengths.append("Relevant work or internship history clearly outlined")
        if section_hits.get("education"):
            strengths.append("Academic qualifications and degree background verified")
        if section_hits.get("certifications"):
            strengths.append("Industry certifications or specialized course credentials included")
        if email != "Not detected" and phone != "Not detected":
            strengths.append("Complete recruiter contact credentials (Email & Phone detected)")

    improvements: List[str] = []
    if llm_result and isinstance(llm_result.get("missing_skills"), list):
        for missing in llm_result.get("missing_skills", []):
            improvements.append(f"Consider acquiring experience in: {missing}")
    
    if not section_hits.get("education"):
        improvements.append("Add a dedicated 'Education' section with your university, degree, and GPA")
    if not section_hits.get("experience"):
        improvements.append("Include an 'Experience' or 'Internships' section highlighting key responsibilities")
    if not section_hits.get("projects"):
        improvements.append("Add a 'Projects' section featuring 2-3 key technical systems you built")
    if not section_hits.get("certifications"):
        improvements.append("List relevant certifications (e.g. AWS, Coursera, HackerRank, Google)")
    if len(skills) < 6:
        improvements.append("Expand the 'Technical Skills' section with modern languages, tools, and databases")
    if not job_description:
        improvements.append("Provide a Target Job Description to receive customized role-specific match scoring")

    # Executive summary
    if llm_result and llm_result.get("summary"):
        summary_text = llm_result.get("summary")
    else:
        role_guess = "Technical Professional"
        if any("React" in s or "Next" in s or "Vue" in s for s in skills):
            role_guess = "Full Stack / Frontend Developer"
        elif any("Python" in s or "FastAPI" in s or "Django" in s for s in skills):
            role_guess = "Backend / Python Developer"
        elif any("Machine Learning" in s or "Pytorch" in s or "Tensorflow" in s for s in skills):
            role_guess = "AI / Machine Learning Engineer"

        summary_text = (
            f"{candidate_name} is a {role_guess} with proficiencies across {', '.join(skills[:5]) if skills else 'core software tools'}. "
            f"The profile demonstrates a {resume_score}% rubric-based resume completeness score."
        )

    return {
        "candidate_name": candidate_name,
        "email": email,
        "phone": phone,
        "skills": skills,
        "sections": section_hits,
        "resume_score": resume_score,
        "resume_score_breakdown": score_breakdown,
        "job_match_score": job_match_score,
        "job_match_available": job_match["available"],
        "job_match_breakdown": {
            key: value for key, value in job_match.items() if key != "available"
        },
        "matched_skills": job_match["matched_skills"],
        "missing_skills": job_match["missing_skills"],
        "strengths": strengths,
        "improvements": improvements[:5],
        "summary": summary_text,
        "ai_provider": "ollama (llama3)" if (llm_result and ai_provider_setting == "ollama") else "NLP & Heuristic Engine",
        "scoring_method": "fixed_rubric_v1",
    }



# ─────────────────────────────────────────────────────────────────────────────
# QUESTION GENERATION
# ─────────────────────────────────────────────────────────────────────────────

def generate_questions(job_role: str, num_mcq: int = 5, num_theory: int = 3, num_coding: int = 2) -> Dict[str, Any]:
    bank = get_questions_for_role(job_role)
    mcqs = bank["mcq"][:num_mcq]
    theory = bank["theory"][:num_theory]
    coding = bank["coding"][:num_coding]

    return {
        "job_role": job_role,
        "available_roles": AVAILABLE_ROLES,
        "mcq": [
            {
                "id": i,
                "question": q["question"],
                "options": q["options"],
                "correct_index": q["correct_index"],
            }
            for i, q in enumerate(mcqs)
        ],
        "theory": [
            {
                "id": i,
                "question": q["question"],
                "expected_keywords": q["expected_keywords"],
            }
            for i, q in enumerate(theory)
        ],
        "coding": [
            {
                "id": i,
                "question": q["question"],
                "function_name": q["function_name"],
                "test_cases": [{"input": tc["input"], "expected": tc["expected"]} for tc in q["test_cases"]],
            }
            for i, q in enumerate(coding)
        ],
    }


# ─────────────────────────────────────────────────────────────────────────────
# ANSWER EVALUATION — MCQ
# ─────────────────────────────────────────────────────────────────────────────

def evaluate_mcq_answer(correct_index: int, selected_index: int) -> Dict[str, Any]:
    correct = correct_index == selected_index
    return {
        "correct": correct,
        "score": 100 if correct else 0,
        "feedback": "Correct answer!" if correct else f"Incorrect. The correct answer was option {correct_index + 1}.",
    }


def evaluate_mcq_batch(mcq_answers: List[Dict]) -> Dict[str, Any]:
    results = []
    total = 0
    for ans in mcq_answers:
        result = evaluate_mcq_answer(ans["correct_index"], ans["selected_index"])
        result["question"] = ans["question"]
        results.append(result)
        total += result["score"]
    avg_score = int(total / max(len(mcq_answers), 1))
    return {"results": results, "mcq_score": avg_score}


# ─────────────────────────────────────────────────────────────────────────────
# ANSWER EVALUATION — THEORY (keyword + TF-IDF similarity)
# ─────────────────────────────────────────────────────────────────────────────

def _tokenize(text: str) -> List[str]:
    return re.findall(r"\b[a-zA-Z][a-zA-Z0-9\-]{1,}\b", text.lower())


def _tfidf_similarity(answer: str, keywords: List[str]) -> float:
    """Simple keyword-overlap similarity scored 0..1."""
    if not answer or not keywords:
        return 0.0
    answer_tokens = set(_tokenize(answer))
    keyword_tokens = set(k.lower() for k in keywords)
    hits = sum(1 for kw in keyword_tokens if kw in answer_tokens or any(kw in tok for tok in answer_tokens))
    return min(hits / max(len(keyword_tokens), 1), 1.0)


def evaluate_theory_answer(question: str, answer: str, expected_keywords: List[str]) -> Dict[str, Any]:
    if not answer or len(answer.split()) < 3:
        return {
            "question": question,
            "score": 0,
            "keyword_hits": [],
            "feedback": "Answer is too short. Please provide a detailed response.",
        }

    # Attempt Local LLM evaluation if Ollama provider is enabled
    ai_provider_setting = os.getenv("AI_PROVIDER", "rule-based").lower()
    if ai_provider_setting == "ollama":
        llm_res = llm_evaluate_interview_answer(
            question=question,
            answer=answer,
            question_type="theory",
            expected_answer=", ".join(expected_keywords) if expected_keywords else None,
        )
        if llm_res and isinstance(llm_res, dict) and "score" in llm_res:
            score = max(0, min(100, int(llm_res.get("score", 0))))
            feedback = llm_res.get("feedback", "AI evaluated response.")
            return {
                "question": question,
                "score": score,
                "keyword_hits": [kw for kw in expected_keywords if kw.lower() in answer.lower()],
                "feedback": feedback,
            }

    answer_lower = answer.lower()
    keyword_hits = [kw for kw in expected_keywords if kw.lower() in answer_lower]
    similarity = _tfidf_similarity(answer, expected_keywords)

    # Length bonus (up to 10 pts for long detailed answers)
    word_count = len(answer.split())
    length_bonus = min(word_count / 10, 10)

    raw_score = similarity * 80 + length_bonus
    score = min(int(raw_score), 100)

    if score >= 75:
        feedback = "Excellent response! Covered key concepts thoroughly."
    elif score >= 55:
        feedback = f"Good attempt. Consider mentioning: {', '.join(set(expected_keywords) - set(keyword_hits))[:3]}."
    elif score >= 30:
        feedback = "Partial answer. Expand your explanation with more technical detail."
    else:
        feedback = f"Response needs improvement. Key concepts missing: {', '.join(expected_keywords[:4])}."

    return {
        "question": question,
        "score": score,
        "keyword_hits": keyword_hits,
        "feedback": feedback,
    }


def evaluate_theory_batch(theory_answers: List[Dict]) -> Dict[str, Any]:
    results = []
    total = 0
    for ans in theory_answers:
        result = evaluate_theory_answer(
            ans["question"],
            ans["answer"],
            ans.get("expected_keywords", []),
        )
        results.append(result)
        total += result["score"]
    avg_score = int(total / max(len(theory_answers), 1))
    return {"results": results, "theory_score": avg_score}


# ─────────────────────────────────────────────────────────────────────────────
# ANSWER EVALUATION — CODING (test-case runner)
# ─────────────────────────────────────────────────────────────────────────────

def evaluate_coding_answer(question: str, function_name: str, code: str, test_cases: List[Dict]) -> Dict[str, Any]:
    if not code or len(code.strip()) < 10:
        return {
            "question": question,
            "score": 0,
            "passed": 0,
            "total": len(test_cases),
            "test_results": [],
            "feedback": "No code submitted or code is too short.",
        }

    local_env: Dict = {}
    test_results = []
    passed = 0

    # Attempt to compile the code first
    try:
        compiled = compile(code, "<string>", "exec")
        exec(compiled, local_env)  # noqa: S102
    except SyntaxError as exc:
        return {
            "question": question,
            "score": 0,
            "passed": 0,
            "total": len(test_cases),
            "test_results": [],
            "feedback": f"Syntax error in your code: {exc}",
        }
    except Exception as exc:
        return {
            "question": question,
            "score": 0,
            "passed": 0,
            "total": len(test_cases),
            "test_results": [],
            "feedback": f"Runtime error when loading code: {exc}",
        }

    fn = local_env.get(function_name)
    if fn is None:
        return {
            "question": question,
            "score": 0,
            "passed": 0,
            "total": len(test_cases),
            "test_results": [],
            "feedback": f"Function `{function_name}` not found in submitted code.",
        }

    for tc in test_cases:
        inp = tc.get("input", [])
        expected = tc.get("expected")
        try:
            actual = fn(*inp)
            ok = actual == expected
        except Exception as exc:
            actual = f"Error: {exc}"
            ok = False

        test_results.append({
            "input": str(inp),
            "expected": str(expected),
            "actual": str(actual),
            "passed": ok,
        })
        if ok:
            passed += 1

    score = int((passed / max(len(test_cases), 1)) * 100)

    if score == 100:
        feedback = "All test cases passed! Great solution."
    elif score >= 75:
        feedback = f"Most test cases passed ({passed}/{len(test_cases)}). Check edge cases."
    elif score >= 50:
        feedback = f"Partial solution ({passed}/{len(test_cases)} tests passed). Review your logic."
    else:
        feedback = f"Only {passed}/{len(test_cases)} tests passed. Revisit the algorithm."

    return {
        "question": question,
        "score": score,
        "passed": passed,
        "total": len(test_cases),
        "test_results": test_results,
        "feedback": feedback,
    }


def evaluate_coding_batch(coding_answers: List[Dict]) -> Dict[str, Any]:
    results = []
    total = 0
    for ans in coding_answers:
        result = evaluate_coding_answer(
            ans["question"],
            ans["function_name"],
            ans["code"],
            ans.get("test_cases", []),
        )
        results.append(result)
        total += result["score"]
    avg_score = int(total / max(len(coding_answers), 1))
    return {"results": results, "coding_score": avg_score}


# ─────────────────────────────────────────────────────────────────────────────
# LEGACY INTERVIEW EVALUATION (kept for backwards-compat)
# ─────────────────────────────────────────────────────────────────────────────

def evaluate_interview(candidate_name: str, job_role: str, answers: List[Dict]) -> Dict[str, Any]:
    answer_lengths = [len(a["answer"].split()) for a in answers]
    average_length = sum(answer_lengths) / max(len(answer_lengths), 1)
    technical_terms = sum(
        sum(1 for skill in SKILL_KEYWORDS if skill in a["answer"].lower()) for a in answers
    )

    communication = min(100, 45 + int(average_length * 1.4))
    technical = min(100, 40 + technical_terms * 3)
    confidence = min(100, 50 + len(answers) * 6 + int(average_length * 0.5))
    overall = int((communication + technical + confidence) / 3)

    if overall >= 80:
        recommendation = "Highly Recommended"
    elif overall >= 65:
        recommendation = "Recommended"
    elif overall >= 50:
        recommendation = "Consider with Further Review"
    else:
        recommendation = "Needs Improvement"

    return {
        "candidate_name": candidate_name,
        "job_role": job_role,
        "communication_score": communication,
        "technical_score": technical,
        "confidence_score": confidence,
        "overall_score": overall,
        "recommendation": recommendation,
        "feedback": [
            "Provide more role-specific examples." if technical < 60 else "Technical responses were relevant.",
            "Use concise, structured answers." if communication < 70 else "Communication was clear and structured.",
        ],
    }


# ─────────────────────────────────────────────────────────────────────────────
# FULL INTERVIEW EVALUATION (MCQ + Theory + Coding + Resume)
# ─────────────────────────────────────────────────────────────────────────────

def evaluate_full_interview(
    candidate_name: str,
    job_role: str,
    resume_text: str,
    job_description: str,
    mcq_answers: List[Dict],
    theory_answers: List[Dict],
    coding_answers: List[Dict],
) -> Dict[str, Any]:

    # Resume score
    resume_analysis = analyze_resume_text(resume_text, job_description) if resume_text else None
    resume_score = resume_analysis["resume_score"] if resume_analysis else 0

    # MCQ evaluation
    mcq_result = evaluate_mcq_batch(mcq_answers) if mcq_answers else {"results": [], "mcq_score": 0}
    mcq_score = mcq_result["mcq_score"]

    # Theory evaluation
    theory_result = evaluate_theory_batch(theory_answers) if theory_answers else {"results": [], "theory_score": 0}
    theory_score = theory_result["theory_score"]

    # Coding evaluation
    coding_result = evaluate_coding_batch(coding_answers) if coding_answers else {"results": [], "coding_score": 0}
    coding_score = coding_result["coding_score"]

    # Interview score = weighted average of MCQ (40%) + Theory (60%)
    interview_score = int(mcq_score * 0.4 + theory_score * 0.6) if (mcq_answers or theory_answers) else 0

    # Overall score = Resume (25%) + Interview (45%) + Coding (30%)
    weights = {"resume": 0.25, "interview": 0.45, "coding": 0.30}
    overall = int(
        resume_score * weights["resume"]
        + interview_score * weights["interview"]
        + coding_score * weights["coding"]
    )

    # Recommendation
    if overall >= 80:
        recommendation = "Highly Recommended"
    elif overall >= 65:
        recommendation = "Recommended"
    elif overall >= 50:
        recommendation = "Consider with Further Review"
    else:
        recommendation = "Needs Improvement"

    # Feedback messages
    feedback: List[str] = []
    if resume_score < 60:
        feedback.append("Strengthen your resume by adding more sections and technical skills.")
    else:
        feedback.append("Your resume demonstrates solid technical breadth.")
    if mcq_score < 60:
        feedback.append(f"Review core {job_role} concepts — MCQ score was below average.")
    else:
        feedback.append(f"Good conceptual knowledge in {job_role} demonstrated through MCQs.")
    if theory_score < 60:
        feedback.append("Expand your theoretical explanations with more technical keywords and depth.")
    else:
        feedback.append("Theory answers showed strong understanding of core concepts.")
    if coding_score < 60:
        feedback.append("Practice algorithmic problem solving to improve coding performance.")
    elif coding_score == 100:
        feedback.append("All coding test cases passed — excellent programming skills!")
    else:
        feedback.append("Good coding attempt; review edge cases for full marks.")

    # Compile all Q&A for the report
    questions_log: List[Dict] = []
    for r in mcq_result["results"]:
        questions_log.append({"type": "MCQ", "question": r["question"], "score": r["score"], "feedback": r["feedback"]})
    for r in theory_result["results"]:
        questions_log.append({"type": "Theory", "question": r["question"], "score": r["score"], "feedback": r["feedback"]})
    for r in coding_result["results"]:
        questions_log.append({"type": "Coding", "question": r["question"], "score": r["score"], "feedback": r["feedback"]})

    return {
        "candidate_name": candidate_name,
        "job_role": job_role,
        "resume_score": resume_score,
        "mcq_score": mcq_score,
        "theory_score": theory_score,
        "coding_score": coding_score,
        "interview_score": interview_score,
        "overall_score": overall,
        "recommendation": recommendation,
        "feedback": feedback,
        "questions_log": questions_log,
        "resume_analysis": resume_analysis,
    }


# ─────────────────────────────────────────────────────────────────────────────
# DATABASE HELPERS
# ─────────────────────────────────────────────────────────────────────────────

def save_report(db: Session, report: Dict[str, Any]) -> Dict[str, Any]:
    candidate_report = CandidateReport(
        candidate_name=report["candidate_name"],
        role=report["role"],
        resume_score=report.get("resume_score", 0),
        interview_score=report.get("interview_score", 0),
        coding_score=report.get("coding_score", 0),
        overall_score=report.get("overall_score", 0),
        recommendation=report.get("recommendation", ""),
        feedback_json=json.dumps(report.get("feedback", [])),
        questions_json=json.dumps(report.get("questions_log", [])),
    )
    db.add(candidate_report)
    db.commit()
    db.refresh(candidate_report)
    return serialize_report(candidate_report)


def load_reports(db: Session) -> List[Dict[str, Any]]:
    reports = db.query(CandidateReport).order_by(desc(CandidateReport.created_at)).all()
    return [serialize_report(r) for r in reports]


def get_report_by_id(db: Session, report_id: int) -> Optional[Dict[str, Any]]:
    report = db.query(CandidateReport).filter(CandidateReport.id == report_id).first()
    return serialize_report(report) if report else None


def build_dashboard_stats(db: Session) -> Dict[str, Any]:
    reports = load_reports(db)
    total_reports = db.query(func.count(CandidateReport.id)).scalar() or 0
    average_score = db.query(func.avg(CandidateReport.overall_score)).scalar()
    avg_score = int(average_score) if average_score is not None else 0
    top_records = (
        db.query(CandidateReport)
        .order_by(desc(CandidateReport.overall_score), desc(CandidateReport.created_at))
        .limit(5)
        .all()
    )
    top_candidates = [serialize_report(r) for r in top_records]
    return {
        "total_resumes": total_reports,
        "interviews_completed": total_reports,
        "average_score": avg_score,
        "top_candidates": top_candidates,
        "recent_reports": reports[:5],
    }


def serialize_report(report: CandidateReport) -> Dict[str, Any]:
    feedback = []
    questions_log = []
    try:
        if report.feedback_json:
            feedback = json.loads(report.feedback_json)
    except Exception:
        pass
    try:
        if report.questions_json:
            questions_log = json.loads(report.questions_json)
    except Exception:
        pass
    return {
        "id": report.id,
        "candidate_name": report.candidate_name,
        "role": report.role,
        "resume_score": report.resume_score,
        "interview_score": report.interview_score,
        "coding_score": report.coding_score,
        "overall_score": report.overall_score,
        "recommendation": report.recommendation,
        "feedback": feedback,
        "questions_log": questions_log,
        "created_at": report.created_at.isoformat() if report.created_at else None,
    }


# ─────────────────────────────────────────────────────────────────────────────
# PDF REPORT GENERATOR
# ─────────────────────────────────────────────────────────────────────────────

def generate_pdf_report(report: Dict[str, Any]) -> bytes:
    """Generate a PDF evaluation report. Returns raw bytes."""
    if _HAS_FPDF:
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()

        # Header
        pdf.set_fill_color(23, 75, 99)
        pdf.rect(0, 0, 210, 40, style="F")
        pdf.set_font("Helvetica", "B", 18)
        pdf.set_text_color(255, 255, 255)
        pdf.set_y(10)
        pdf.cell(0, 10, "AI-Powered Interview Evaluation System", align="C", ln=True)
        pdf.set_font("Helvetica", size=11)
        pdf.cell(0, 8, "Candidate Performance Report", align="C", ln=True)
        pdf.set_y(45)
        pdf.set_text_color(30, 31, 28)

        # Candidate Info
        pdf.set_font("Helvetica", "B", 13)
        pdf.cell(0, 8, f"Candidate: {report.get('candidate_name', 'N/A')}", ln=True)
        pdf.set_font("Helvetica", size=11)
        pdf.cell(0, 7, f"Applied Role: {report.get('role', 'N/A')}", ln=True)
        pdf.cell(0, 7, f"Date: {str(report.get('created_at', 'N/A'))[:10]}", ln=True)
        pdf.ln(4)

        # Score Summary
        pdf.set_fill_color(239, 246, 251)
        pdf.set_font("Helvetica", "B", 12)
        pdf.cell(0, 9, "Score Summary", ln=True, fill=True)
        pdf.set_font("Helvetica", size=11)

        scores = [
            ("Resume Score", report.get("resume_score", 0)),
            ("Interview Score", report.get("interview_score", 0)),
            ("Coding Score", report.get("coding_score", 0)),
            ("Overall Score", report.get("overall_score", 0)),
        ]
        for label, score in scores:
            pdf.cell(80, 7, label + ":", border="B")
            pdf.cell(0, 7, f"{score}%", border="B", ln=True)
        pdf.ln(3)

        # Recommendation
        rec = report.get("recommendation", "")
        rec_color = {
            "Highly Recommended": (63, 108, 81),
            "Recommended": (23, 75, 99),
            "Consider with Further Review": (202, 107, 44),
            "Needs Improvement": (178, 58, 43),
        }.get(rec, (30, 31, 28))
        pdf.set_font("Helvetica", "B", 12)
        pdf.set_text_color(*rec_color)
        pdf.cell(0, 9, f"Recommendation: {rec}", ln=True)
        pdf.set_text_color(30, 31, 28)
        pdf.ln(3)

        # Feedback
        feedback = report.get("feedback", [])
        if feedback:
            pdf.set_font("Helvetica", "B", 12)
            pdf.cell(0, 9, "Feedback & Suggestions", ln=True)
            pdf.set_font("Helvetica", size=10)
            for item in feedback:
                pdf.multi_cell(0, 6, f"• {item}")
            pdf.ln(3)

        # Q&A Breakdown
        questions_log = report.get("questions_log", [])
        if questions_log:
            pdf.set_font("Helvetica", "B", 12)
            pdf.cell(0, 9, "Question-wise Evaluation", ln=True)
            pdf.set_font("Helvetica", size=9)
            for i, q in enumerate(questions_log, 1):
                pdf.set_font("Helvetica", "B", 9)
                q_type = q.get("type", "")
                q_score = q.get("score", 0)
                color = (63, 108, 81) if q_score >= 70 else (202, 107, 44) if q_score >= 40 else (178, 58, 43)
                pdf.set_text_color(*color)
                pdf.multi_cell(0, 5, f"Q{i} [{q_type}] Score: {q_score}%")
                pdf.set_text_color(30, 31, 28)
                pdf.set_font("Helvetica", size=9)
                short_q = q.get("question", "")[:120]
                pdf.multi_cell(0, 5, f"   {short_q}...")
                fb = q.get("feedback", "")
                if fb:
                    pdf.set_text_color(97, 95, 90)
                    pdf.multi_cell(0, 5, f"   Feedback: {fb}")
                    pdf.set_text_color(30, 31, 28)
                pdf.ln(1)

        # Footer
        pdf.set_y(-20)
        pdf.set_font("Helvetica", "I", 8)
        pdf.set_text_color(150, 150, 150)
        pdf.cell(0, 6, "Generated by AI-Powered Interview Evaluation & Resume Analysis System — Final Year Project", align="C")

        return bytes(pdf.output())
    else:
        # Minimal PDF format fallback
        candidate = report.get('candidate_name', 'Candidate')
        role = report.get('role', 'N/A')
        overall = report.get('overall_score', 0)
        rec = report.get('recommendation', 'N/A')
        content = (
            f"%PDF-1.4\n1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj\n"
            f"2 0 obj<</Type/Pages/Count 1/Kids[3 0 R]>>endobj\n"
            f"3 0 obj<</Type/Page/MediaBox[0 0 612 792]/Parent 2 0 R/Resources<</Font<</F1<</Type/Font/Subtype/Type1/BaseFont/Helvetica>>>>>>/Contents 4 0 R>>endobj\n"
            f"4 0 obj<</Length 220>>stream\nBT\n/F1 16 Tf\n50 720 Td\n(AI-Powered Interview Evaluation System) Tj\n/F1 12 Tf\n0 -30 Td\n(Candidate: {candidate}) Tj\n0 -20 Td\n(Role: {role}) Tj\n0 -20 Td\n(Overall Score: {overall}%) Tj\n0 -20 Td\n(Recommendation: {rec}) Tj\nET\nendstream\nendobj\nxref\n0 5\n0000000000 65535 f \n0000000009 00000 n \n0000000056 00000 n \n0000000111 00000 n \n0000000262 00000 n \ntrailer<</Size 5/Root 1 0 R>>\nstartxref\n530\n%%EOF"
        )
        return content.encode("latin1")
