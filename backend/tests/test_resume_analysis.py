import asyncio
import io
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from starlette.datastructures import UploadFile

from app.database import Base
from app.models import CandidateReport
from app.services import RESUME_SCORE_RUBRIC, analyze_resume_text, score_resume
import main as api_main


class ResumeScoringTests(unittest.TestCase):
    def test_rubric_is_a_transparent_100_point_scale(self):
        self.assertEqual(sum(item["max_score"] for item in RESUME_SCORE_RUBRIC), 100)

    def test_profile_completeness_changes_with_resume_evidence(self):
        sparse_resume = "Alex Doe\nalex@example.com\nPython"
        detailed_resume = """
Alex Doe
alex@example.com | +1 555 123 4567 | linkedin.com/in/alex
EDUCATION
Bachelor of Computer Science, 2021
EXPERIENCE
Software Engineer, 2021 - 2024
- Developed Python services and reduced request latency by 35%.
- Built a React dashboard used by 2,000 customers.
PROJECTS
- Designed and deployed a Django application.
SKILLS
Python, React, Django, PostgreSQL, Docker, AWS
CERTIFICATIONS
AWS Certified Developer
"""

        sparse_score = score_resume(sparse_resume, "")[0]
        detailed_score = score_resume(detailed_resume, "")[0]
        self.assertLess(sparse_score, detailed_score)
        self.assertLess(detailed_score, 100)

    def test_job_match_uses_role_requirements_and_is_unavailable_without_jd(self):
        resume = "Python developer with Django and PostgreSQL. Built web services."
        target_role = "Python developer with Django, PostgreSQL, Docker and AWS cloud deployment experience."

        _, no_jd_score = score_resume(resume, "")
        _, role_score = score_resume(resume, target_role)
        with patch.dict(os.environ, {"AI_PROVIDER": "rule-based"}):
            result = analyze_resume_text(resume, target_role)
            no_role_result = analyze_resume_text(resume)

        self.assertEqual(no_jd_score, 0)
        self.assertGreater(role_score, no_jd_score)
        self.assertTrue(result["job_match_available"])
        self.assertIn("docker", result["missing_skills"])

        self.assertFalse(no_role_result["job_match_available"])
        self.assertEqual(no_role_result["job_match_score"], 0)

    def test_model_returned_scores_cannot_override_the_fixed_rubric(self):
        resume = """
Alex Doe
alex@example.com | +1 555 123 4567
EDUCATION
Bachelor of Computer Science
SKILLS
Python, SQL
"""
        expected_score = score_resume(resume, "")[0]
        with patch.dict(os.environ, {"AI_PROVIDER": "ollama"}):
            with patch(
                "app.services.llm_analyze_resume",
                return_value={
                    "resume_score": 100,
                    "job_match_score": 100,
                    "summary": "A short profile summary.",
                    "strengths": [],
                    "missing_skills": [],
                },
            ):
                result = analyze_resume_text(resume)

        self.assertEqual(result["resume_score"], expected_score)
        self.assertEqual(result["job_match_score"], 0)
        self.assertEqual(result["scoring_method"], "fixed_rubric_v1")

    def test_uploaded_resume_persists_a_report_and_returns_storage_status(self):
        engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(bind=engine)
        session = sessionmaker(bind=engine)()
        resume_text = """
Alex Doe
alex@example.com | +1 555 123 4567
EDUCATION
Bachelor of Computer Science, 2021
EXPERIENCE
Software Engineer, 2021 - 2024
- Developed Python services and reduced request latency by 35%.
PROJECTS
- Built a Django application.
SKILLS
Python, Django, PostgreSQL
"""

        try:
            with tempfile.TemporaryDirectory() as upload_dir:
                with patch.object(api_main, "UPLOAD_DIR", Path(upload_dir)):
                    with patch.object(api_main, "extract_text_from_file", return_value=resume_text):
                        with patch.object(api_main, "save_uploaded_file", return_value="gridfs-file-id"):
                            with patch.object(
                                api_main,
                                "save_candidate_profile",
                                return_value={"status": "saved", "profile_id": "mongo-profile-id"},
                            ):
                                with patch.dict(os.environ, {"AI_PROVIDER": "rule-based"}):
                                    response = asyncio.run(api_main.upload_resume(
                                        UploadFile(filename="alex.txt", file=io.BytesIO(b"resume")),
                                        "Python developer with Django and PostgreSQL cloud services",
                                        None,
                                        session,
                                    ))

            saved_report = session.query(CandidateReport).filter_by(id=response["report_id"]).one()
            self.assertEqual(response["mongo_file_id"], "gridfs-file-id")
            self.assertEqual(response["mongo_profile_status"], "saved")
            self.assertEqual(saved_report.resume_score, response["analysis"]["resume_score"])
            self.assertTrue(saved_report.feedback_json)
        finally:
            session.close()
            engine.dispose()


if __name__ == "__main__":
    unittest.main()
