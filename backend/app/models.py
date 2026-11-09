from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import relationship

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(120), nullable=False)
    email = Column(String(180), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(40), nullable=False, index=True)


class UserVerification(Base):
    __tablename__ = "user_verifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True, index=True)
    status = Column(String(32), nullable=False, default="pending")
    similarity_score = Column(Float, nullable=False, default=0.0)
    rejection_reason = Column(Text, nullable=True)
    id_card_path = Column(String(255), nullable=True)
    selfie_path = Column(String(255), nullable=True)
    verified_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True)

    user = relationship("User", backref="verification")


class CandidateReport(Base):
    __tablename__ = "candidate_reports"

    id = Column(Integer, primary_key=True, index=True)
    candidate_name = Column(String(120), nullable=False, index=True)
    role = Column(String(120), nullable=False, index=True)
    resume_score = Column(Integer, nullable=False, default=0)
    interview_score = Column(Integer, nullable=False, default=0)
    coding_score = Column(Integer, nullable=False, default=0)
    overall_score = Column(Integer, nullable=False, index=True, default=0)
    recommendation = Column(String(120), nullable=False)
    feedback_json = Column(Text, nullable=True)        # JSON array of feedback strings
    questions_json = Column(Text, nullable=True)       # JSON array of Q&A with scores
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True)
