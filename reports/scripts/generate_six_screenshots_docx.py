#!/usr/bin/env python3
"""
Compile the exact 6 key screenshots for the AI-Powered Interview Evaluation
& Resume Analysis System into a clean Microsoft Word (.docx) file.
"""

from pathlib import Path
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

ROOT = Path("/Users/viki/Final_Year_Project/reports")
OUT_IMG_DIR = ROOT / "results_images"
DOCX_OUT = ROOT / "AI_Interview_Six_Screenshots_Results.docx"

SIX_FIGURES = [
    {
        "num": "Screenshot 1",
        "title": "Portal Landing Page (Candidate & Recruiter Entry)",
        "file": "result_1_home_landing.png",
        "desc": "The main landing interface provides dedicated candidate and recruiter pathways, an overview of the system's core capabilities (NLP resume analysis, biometric ID verification, AI dynamic interview scoring), and live platform aggregate statistics."
    },
    {
        "num": "Screenshot 2",
        "title": "Resume Analysis & Skill Gap Extraction",
        "file": "result_2_resume_analysis.png",
        "desc": "Demonstrates automated entity parsing from uploaded candidate resumes (PDF/DOCX). The system identifies structured fields (candidate details, education, years of experience, core skills) and calculates a semantic job-match score (88%) against the target job description."
    },
    {
        "num": "Screenshot 3",
        "title": "Biometric Identity Verification & Anti-Spoofing",
        "file": "result_3_identity_verification.png",
        "desc": "Captures the candidate identity validation pipeline. The candidate uploads a government ID card, and the system performs facial landmark extraction and compares it with a live proctored webcam selfie (96.4% match confirmed) to prevent impersonation."
    },
    {
        "num": "Screenshot 4",
        "title": "AI Interactive Interview & Code Evaluation",
        "file": "result_4_interview_evaluation.png",
        "desc": "The dynamic multi-modal technical testing environment. Features technical MCQs, NLP-evaluated theory answers with semantic clarity scoring, and an interactive code editor with an automated unit test case runner (3/3 test cases passed)."
    },
    {
        "num": "Screenshot 5",
        "title": "Recruiter Analytics Dashboard & Leaderboard",
        "file": "result_5_recruiter_dashboard.png",
        "desc": "The recruiter analytics dashboard displays aggregate metrics (total candidates evaluated, completion rates, average score) and an interactive candidate leaderboard ranking applicants by weighted overall performance."
    },
    {
        "num": "Screenshot 6",
        "title": "Comprehensive AI Evaluation Report & PDF Export",
        "file": "result_6_evaluation_reports.png",
        "desc": "The comprehensive candidate evaluation dossier combining the weighted assessment matrix (Resume 30%, MCQ 25%, Theory 25%, Coding 20%), biometric proctoring status, qualitative candidate strengths, onboarding recommendations, and instant PDF report export."
    },
]

def build_six_screenshots_doc():
    doc = docx.Document()
    
    # 1-inch margins
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        
    style = doc.styles['Normal']
    font = style.font
    font.name = 'Times New Roman'
    font.size = Pt(12)
    font.color.rgb = RGBColor(0x1e, 0x29, 0x3b)
    
    # Title
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_uni = p_title.add_run("DEPARTMENT OF INFORMATION SCIENCE AND ENGINEERING\n")
    r_uni.bold = True
    r_uni.font.size = Pt(14)
    r_uni.font.color.rgb = RGBColor(0x1e, 0x3a, 0x8a)
    
    r_proj = p_title.add_run("AI-Powered Interview Evaluation & Resume Analysis System\n")
    r_proj.bold = True
    r_proj.font.size = Pt(16)
    r_proj.font.color.rgb = RGBColor(0x0f, 0x17, 0x2a)
    
    r_sub = p_title.add_run("WORKING SYSTEM SNAPSHOTS — RESULTS AND DISCUSSION\n")
    r_sub.bold = True
    r_sub.font.size = Pt(13)
    r_sub.font.color.rgb = RGBColor(0x25, 0x63, 0xeb)
    
    doc.add_paragraph().paragraph_format.space_after = Pt(10)
    
    p_intro = doc.add_paragraph()
    p_intro.paragraph_format.line_spacing = 1.15
    p_intro.paragraph_format.space_after = Pt(12)
    p_intro.add_run(
        "This document contains the 6 key functional screenshots of the running working system, capturing the user interface, "
        "AI processing outputs, biometric identity verification checks, interactive coding evaluation engine, recruiter analytics dashboard, "
        "and downloadable final candidate reports."
    )
    
    for item in SIX_FIGURES:
        img_path = OUT_IMG_DIR / item["file"]
        
        h2 = doc.add_heading(level=2)
        r_h2 = h2.add_run(f"{item['num']}: {item['title']}")
        r_h2.font.name = 'Times New Roman'
        r_h2.font.size = Pt(13)
        r_h2.bold = True
        r_h2.font.color.rgb = RGBColor(0x1e, 0x3a, 0x8a)
        h2.paragraph_format.space_before = Pt(14)
        h2.paragraph_format.space_after = Pt(6)
        
        p_desc = doc.add_paragraph()
        p_desc.paragraph_format.line_spacing = 1.15
        p_desc.paragraph_format.space_after = Pt(8)
        p_desc.add_run(item["desc"])
        
        if img_path.exists():
            p_img = doc.add_paragraph()
            p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_img.paragraph_format.space_after = Pt(4)
            p_img.paragraph_format.space_before = Pt(4)
            p_img.add_run().add_picture(str(img_path), width=Inches(6.2))
            
            p_cap = doc.add_paragraph()
            p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_cap.paragraph_format.space_after = Pt(16)
            r_cap = p_cap.add_run(f"{item['num']} — {item['title']}")
            r_cap.italic = True
            r_cap.font.size = Pt(10.5)
            r_cap.font.color.rgb = RGBColor(0x47, 0x55, 0x69)
            
        doc.add_paragraph().paragraph_format.space_after = Pt(6)
        
    doc.save(str(DOCX_OUT))
    print(f"Saved 6 Screenshots Word document to: {DOCX_OUT}")

if __name__ == "__main__":
    build_six_screenshots_doc()
