#!/usr/bin/env python3
"""Build Project Report PPT (~20 slides) with hand-drawn diagrams + screenshots."""

from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

ROOT = Path(__file__).resolve().parents[1]
DIAG = ROOT / "hand_drawn_diagrams"
SHOTS = ROOT / "project_images"
OUT_PPTX = ROOT / "Project_Report_PPT.pptx"
OUT_TXT = ROOT / "Project_Report_PPT_Content.txt"

# Colors – plain academic look (no purple marketing theme)
NAVY = RGBColor(20, 50, 110)
BLACK = RGBColor(0, 0, 0)
DARK = RGBColor(40, 40, 40)
WHITE = RGBColor(255, 255, 255)
LIGHT_BG = RGBColor(248, 250, 252)


def set_run(run, size=18, bold=False, color=BLACK, font_name="Arial"):
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.color.rgb = color
    run.font.name = font_name


def add_title_bar(slide, prs, text):
    shape = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), prs.slide_width, Inches(0.85)
    )
    shape.fill.solid()
    shape.fill.fore_color.rgb = NAVY
    shape.line.fill.background()
    tf = shape.text_frame
    tf.clear()
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.LEFT
    run = p.add_run()
    run.text = "  " + text
    set_run(run, 24, True, WHITE)


def add_bullets(slide, left, top, width, height, items, size=16):
    box = slide.shapes.add_textbox(left, top, width, height)
    tf = box.text_frame
    tf.word_wrap = True
    for i, item in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = "•  " + item
        p.level = 0
        p.space_after = Pt(8)
        for run in p.runs:
            set_run(run, size, False, DARK)
    return box


def add_paragraph(slide, left, top, width, height, text, size=16, bold=False):
    box = slide.shapes.add_textbox(left, top, width, height)
    tf = box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    run = p.add_run()
    run.text = text
    set_run(run, size, bold, DARK)
    return box


def fit_image(slide, path, left, top, max_w, max_h):
    """Place image fitting inside max box, preserving aspect ratio."""
    from PIL import Image
    with Image.open(path) as im:
        iw, ih = im.size
    aspect = iw / ih
    box_aspect = max_w / max_h
    if aspect > box_aspect:
        w = max_w
        h = max_w / aspect
    else:
        h = max_h
        w = max_h * aspect
    # center in box
    x = left + (max_w - w) / 2
    y = top + (max_h - h) / 2
    slide.shapes.add_picture(str(path), int(x), int(y), width=int(w), height=int(h))


def blank_slide(prs):
    return prs.slides.add_slide(prs.slide_layouts[6])  # blank


def build_txt():
    content = """AI-Powered Interview Evaluation & Resume Analysis System
Project Report – PowerPoint Content (~20 slides)
================================================

SLIDE 1 – Title
---------------
Title: AI-Powered Interview Evaluation & Resume Analysis System
Subtitle: Project Phase II Presentation
Department of Information Science and Engineering
Project Associates | Guide | Coordinators

SLIDE 2 – Contents
------------------
• Abstract
• Introduction / Problem Statement
• Objectives
• Existing vs Proposed System
• System Architecture & Modules
• Candidate Workflow
• Technology Stack
• Scoring Model
• Implementation Highlights
• Screenshots (Home, Login, Verification)
• Testing & Results
• Advantages / Conclusion / Future Work
• References / Thank You

SLIDE 3 – Abstract
------------------
This project is an AI-powered recruitment support system that reduces recruiter workload by automating resume screening, interview assessment, and final candidate evaluation. It extracts skills, education, and experience from resumes, compares them with job requirements, and calculates a job-match score. Identity verification uses ID upload and face matching. A structured interview covers MCQ, theory, and coding. The final report helps recruiters make faster, fairer decisions.

SLIDE 4 – Introduction
----------------------
• Combines resume analysis, verification, and interview evaluation
• Manual hiring is slow, inconsistent, and hard to scale
• Uses AI-based logic and structured scoring for reliability
• Supports multiple job roles and role-based questions
• Suitable for companies, HR teams, and academic assessment

SLIDE 5 – Problem Statement
---------------------------
Recruitment is often slow and manual. Recruiters must read many resumes, compare skills with job requirements, and evaluate interviews. Fake candidates may try to attend without proper identity checks. This project addresses these issues with automated resume analysis, verification, interview evaluation, and report generation.

SLIDE 6 – Objectives
--------------------
• Design an intelligent resume analysis system
• Extract skills, education, and experience automatically
• Match profiles with job descriptions
• Verify identity (ID + selfie)
• Generate and evaluate role-based interview questions
• Produce structured reports for recruiters

SLIDE 7 – Existing vs Proposed System
-------------------------------------
[Diagram: existing_vs_proposed.png]
Existing: manual screening, inconsistent scoring, weak identity checks
Proposed: auto parsing, structured scoring, ID+face verify, dashboard reports

SLIDE 8 – System Architecture
-----------------------------
[Diagram: architecture_diagram.png]
Layers: Presentation (React) → API (FastAPI) → Business Logic + AI Engine → Data Layer

SLIDE 9 – System Modules
------------------------
[Diagram: system_modules.png]
User, Resume, Verification, Interview, Scoring, Reporting modules

SLIDE 10 – Candidate Workflow
-----------------------------
[Diagram: candidate_workflow.png]
Login → Upload Resume → Identity Verification → Interview → Score & Report

SLIDE 11 – Technology Stack
---------------------------
[Diagram: tech_stack.png]
Frontend: React.js | Backend: FastAPI | DB: SQLite/SQLAlchemy
AI/NLP: rule-based (+ optional Ollama) | Tools: VS Code, Git, Postman

SLIDE 12 – Scoring Model
------------------------
[Diagram: scoring_model.png]
Weighted score: Resume 30% | MCQ 25% | Theory 25% | Coding 20%
Output: Final score (0–100) + recommendation

SLIDE 13 – Use Case / Data Flow
-------------------------------
[Diagram: use_case_diagram.png or data_flow_diagram.png]
Actors: Candidate, Recruiter | Core use cases: login, upload, verify, interview, report

SLIDE 14 – Screenshot: Home Page
--------------------------------
[Image: project_images/home.png]
Landing page with navigation to Identity Check and Resume Analysis

SLIDE 15 – Screenshot: Candidate Login
--------------------------------------
[Image: project_images/candidate_login.png]
Role-based login for candidates (demo credentials supported)

SLIDE 16 – Screenshot: Identity Verification
--------------------------------------------
[Image: project_images/verification.png]
Steps: ID upload → Selfie capture → Access unlock

SLIDE 17 – Testing
------------------
Unit, Integration, System, Acceptance testing
Sample cases: login, resume upload, verification pass/fail, interview scoring, report PDF
Tools: Manual testing, browser testing, Postman

SLIDE 18 – Results & Advantages
-------------------------------
Results: successful resume extraction, verification gating, role-based interview scoring, recruiter dashboard
Advantages: time saving, consistent evaluation, identity security, role-based assessment
Limitations: complex answer scoring and resume formatting edge cases

SLIDE 19 – Conclusion & Future Enhancements
-------------------------------------------
Conclusion: Practical end-to-end AI recruitment support system
Future: voice/video analysis, stronger biometrics, cloud hosting, multilingual support, advanced LLM scoring

SLIDE 20 – References / Thank You
---------------------------------
References: recruitment/NLP papers, FastAPI/React docs, project libraries
Thank You…!
"""
    OUT_TXT.write_text(content, encoding="utf-8")
    print(f"Wrote {OUT_TXT}")


def build_pptx():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    # ---- Slide 1: Title ----
    s = blank_slide(prs)
    # light paper-like background bar
    bg = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    bg.fill.solid()
    bg.fill.fore_color.rgb = LIGHT_BG
    bg.line.fill.background()
    bar = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, Inches(2.2), prs.slide_width, Inches(2.4))
    bar.fill.solid()
    bar.fill.fore_color.rgb = NAVY
    bar.line.fill.background()
    tb = s.shapes.add_textbox(Inches(0.8), Inches(2.4), Inches(11.7), Inches(2))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    r = p.add_run()
    r.text = "AI-Powered Interview Evaluation & Resume Analysis System"
    set_run(r, 28, True, WHITE)
    p2 = tf.add_paragraph()
    p2.alignment = PP_ALIGN.CENTER
    r2 = p2.add_run()
    r2.text = "\nProject Phase II Presentation  |  Dept. of Information Science & Engineering"
    set_run(r2, 16, False, WHITE)
    foot = s.shapes.add_textbox(Inches(0.8), Inches(5.2), Inches(11.7), Inches(1.5))
    ft = foot.text_frame
    fp = ft.paragraphs[0]
    fp.alignment = PP_ALIGN.CENTER
    fr = fp.add_run()
    fr.text = "Project Associates  •  Under the Guidance of Project Guide\nProgram Coordinator: Dr. Vinutha H P  •  Project Coordinators: Dr. Arun Kumar G H, Prof. Santhosh T"
    set_run(fr, 14, False, DARK)

    # ---- Slide 2: Contents ----
    s = blank_slide(prs)
    add_title_bar(s, prs, "Contents")
    left_items = [
        "Abstract",
        "Introduction & Problem Statement",
        "Objectives",
        "Existing vs Proposed System",
        "System Architecture",
        "System Modules",
        "Candidate Workflow",
        "Technology Stack",
        "Scoring Model",
    ]
    right_items = [
        "Use Case / Data Flow",
        "Home Page Screenshot",
        "Login Screenshot",
        "Verification Screenshot",
        "Testing",
        "Results & Advantages",
        "Conclusion & Future Work",
        "References",
        "Thank You",
    ]
    add_bullets(s, Inches(0.8), Inches(1.2), Inches(5.5), Inches(5.5), left_items, 18)
    add_bullets(s, Inches(7), Inches(1.2), Inches(5.5), Inches(5.5), right_items, 18)

    # ---- Slide 3: Abstract ----
    s = blank_slide(prs)
    add_title_bar(s, prs, "Abstract")
    add_paragraph(
        s, Inches(0.8), Inches(1.3), Inches(11.7), Inches(5.5),
        "This project is an AI-powered recruitment support system that helps reduce recruiter workload by automating resume screening, interview assessment, and final candidate evaluation.\n\n"
        "It extracts skill, education, and experience details from resumes, compares them with job requirements, and calculates a job-match score. Identity verification uses ID upload and face matching. A structured interview includes MCQ, theory, and coding questions.\n\n"
        "The final output is a generated report that helps recruiters make faster, fairer, and more informed decisions.",
        18,
    )

    # ---- Slide 4: Introduction ----
    s = blank_slide(prs)
    add_title_bar(s, prs, "Introduction")
    add_bullets(s, Inches(0.8), Inches(1.2), Inches(11.5), Inches(5.5), [
        "Makes hiring smarter by combining resume analysis, verification, and interview evaluation",
        "Many companies still rely on manual screening — slow and sometimes biased",
        "Uses AI-based logic and structured evaluation to improve speed and reliability",
        "Supports multiple job roles and generates role-based interview questions",
        "Provides clear scores and recommendations for decision-making",
        "Suitable for companies, recruitment teams, and academic assessment systems",
    ], 18)

    # ---- Slide 5: Problem ----
    s = blank_slide(prs)
    add_title_bar(s, prs, "Problem Statement")
    add_paragraph(
        s, Inches(0.8), Inches(1.3), Inches(11.7), Inches(5.5),
        "The recruitment process is often slow, inconsistent, and manual. Recruiters must read large numbers of resumes, compare candidate skills with job requirements, and evaluate technical ability through interviews.\n\n"
        "In many cases this makes the process inefficient and unfair. There is also a risk of fake candidates attempting to attend interviews without proper identity verification.\n\n"
        "This project addresses these issues by building an AI-powered system that automates resume analysis, candidate verification, interview evaluation, and report generation.",
        18,
    )

    # ---- Slide 6: Objectives ----
    s = blank_slide(prs)
    add_title_bar(s, prs, "Objectives")
    add_bullets(s, Inches(0.8), Inches(1.2), Inches(11.5), Inches(5.5), [
        "Design an intelligent system for candidate resume analysis",
        "Extract skills, education, and experience from resumes automatically",
        "Match candidate profiles with the required job description",
        "Verify candidate identity using ID upload and selfie comparison",
        "Generate role-based interview questions and evaluate responses",
        "Produce fair and structured candidate reports for recruiters",
        "Improve the speed, efficiency, and reliability of recruitment",
    ], 18)

    # ---- Slide 7: Existing vs Proposed ----
    s = blank_slide(prs)
    add_title_bar(s, prs, "Existing System vs Proposed System")
    fit_image(s, DIAG / "existing_vs_proposed.png", Inches(0.6), Inches(1.0), Inches(12.1), Inches(6.2))

    # ---- Slide 8: Architecture ----
    s = blank_slide(prs)
    add_title_bar(s, prs, "System Architecture")
    fit_image(s, DIAG / "architecture_diagram.png", Inches(0.6), Inches(1.0), Inches(12.1), Inches(6.2))

    # ---- Slide 9: Modules ----
    s = blank_slide(prs)
    add_title_bar(s, prs, "System Modules")
    fit_image(s, DIAG / "system_modules.png", Inches(0.6), Inches(1.0), Inches(12.1), Inches(6.2))

    # ---- Slide 10: Workflow ----
    s = blank_slide(prs)
    add_title_bar(s, prs, "Candidate Workflow")
    fit_image(s, DIAG / "candidate_workflow.png", Inches(0.4), Inches(1.5), Inches(12.5), Inches(5.2))

    # ---- Slide 11: Tech Stack ----
    s = blank_slide(prs)
    add_title_bar(s, prs, "Technology Stack")
    fit_image(s, DIAG / "tech_stack.png", Inches(0.6), Inches(1.0), Inches(12.1), Inches(6.2))

    # ---- Slide 12: Scoring ----
    s = blank_slide(prs)
    add_title_bar(s, prs, "Scoring Model")
    fit_image(s, DIAG / "scoring_model.png", Inches(0.6), Inches(1.0), Inches(12.1), Inches(6.2))

    # ---- Slide 13: Use Case ----
    s = blank_slide(prs)
    add_title_bar(s, prs, "Use Case Diagram")
    fit_image(s, DIAG / "use_case_diagram.png", Inches(3.5), Inches(0.95), Inches(6.3), Inches(6.3))

    # ---- Slide 14: Home screenshot ----
    s = blank_slide(prs)
    add_title_bar(s, prs, "Screenshot: Home Page")
    fit_image(s, SHOTS / "home.png", Inches(2.5), Inches(1.0), Inches(8.3), Inches(6.2))

    # ---- Slide 15: Login ----
    s = blank_slide(prs)
    add_title_bar(s, prs, "Screenshot: Candidate Login")
    fit_image(s, SHOTS / "candidate_login.png", Inches(2.2), Inches(1.0), Inches(8.9), Inches(6.2))

    # ---- Slide 16: Verification ----
    s = blank_slide(prs)
    add_title_bar(s, prs, "Screenshot: Identity Verification")
    fit_image(s, SHOTS / "verification.png", Inches(2.2), Inches(1.0), Inches(8.9), Inches(6.2))

    # ---- Slide 17: Testing ----
    s = blank_slide(prs)
    add_title_bar(s, prs, "Testing")
    add_paragraph(s, Inches(0.8), Inches(1.1), Inches(11.5), Inches(0.5), "Testing Strategies", 18, True)
    add_bullets(s, Inches(0.8), Inches(1.6), Inches(5.8), Inches(2.5), [
        "Unit Testing – parsing, scoring, validation",
        "Integration Testing – frontend, backend, DB",
        "System Testing – full login-to-report flow",
        "Acceptance Testing – meets project requirements",
    ], 16)
    add_paragraph(s, Inches(0.8), Inches(4.2), Inches(11.5), Inches(0.4), "Sample Test Cases (Pass)", 18, True)
    add_bullets(s, Inches(0.8), Inches(4.7), Inches(11.5), Inches(2.2), [
        "TC01 Valid candidate login  |  TC03 Resume upload  |  TC05 Identity verification pass",
        "TC07 Interview generation  |  TC08 Score calculation  |  TC09 Report PDF generation",
    ], 16)

    # ---- Slide 18: Results ----
    s = blank_slide(prs)
    add_title_bar(s, prs, "Results & Advantages")
    add_paragraph(s, Inches(0.8), Inches(1.1), Inches(5.5), Inches(0.4), "Results", 18, True)
    add_bullets(s, Inches(0.8), Inches(1.6), Inches(5.8), Inches(4.5), [
        "Resume details extracted with job-match score",
        "Identity verification blocks invalid attempts",
        "Role-based MCQ, theory, coding evaluation works",
        "Dashboard shows rankings and summary metrics",
        "PDF reports generated for recruiters",
    ], 16)
    add_paragraph(s, Inches(7), Inches(1.1), Inches(5.5), Inches(0.4), "Advantages", 18, True)
    add_bullets(s, Inches(7), Inches(1.6), Inches(5.5), Inches(4.5), [
        "Saves time in screening",
        "Improves evaluation consistency",
        "Adds identity security layer",
        "Supports role-based assessments",
        "Enables better candidate comparison",
    ], 16)

    # ---- Slide 19: Conclusion ----
    s = blank_slide(prs)
    add_title_bar(s, prs, "Conclusion & Future Enhancements")
    add_paragraph(
        s, Inches(0.8), Inches(1.2), Inches(11.7), Inches(2.2),
        "Conclusion: The project successfully demonstrates how AI can improve recruitment by combining resume analysis, identity verification, role-based interview evaluation, and report generation into one practical system. It reduces manual effort and helps recruiters make better decisions.",
        17,
    )
    add_paragraph(s, Inches(0.8), Inches(3.5), Inches(11.5), Inches(0.4), "Future Enhancements", 18, True)
    add_bullets(s, Inches(0.8), Inches(4.0), Inches(11.5), Inches(3), [
        "Voice / video interview analysis and stronger biometric verification",
        "Advanced LLM-based scoring and multilingual interfaces",
        "Cloud hosting, recruiter notifications, and mobile support",
    ], 16)

    # ---- Slide 20: Thank You ----
    s = blank_slide(prs)
    bg = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    bg.fill.solid()
    bg.fill.fore_color.rgb = LIGHT_BG
    bg.line.fill.background()
    bar = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, Inches(2.4), prs.slide_width, Inches(2.2))
    bar.fill.solid()
    bar.fill.fore_color.rgb = NAVY
    bar.line.fill.background()
    tb = s.shapes.add_textbox(Inches(1), Inches(2.6), Inches(11.3), Inches(1.8))
    tf = tb.text_frame
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    r = p.add_run()
    r.text = "Thank You…!"
    set_run(r, 40, True, WHITE)
    p2 = tf.add_paragraph()
    p2.alignment = PP_ALIGN.CENTER
    r2 = p2.add_run()
    r2.text = "\nQuestions & Discussion"
    set_run(r2, 18, False, WHITE)
    ref = s.shapes.add_textbox(Inches(0.8), Inches(5.2), Inches(11.7), Inches(1.8))
    rtf = ref.text_frame
    rtf.word_wrap = True
    rp = rtf.paragraphs[0]
    rr = rp.add_run()
    rr.text = (
        "References (selected): Smart recruitment / resume NLP literature (2020–2024); "
        "FastAPI, React, SQLAlchemy documentation; project open-source libraries used for parsing and evaluation."
    )
    set_run(rr, 12, False, DARK)

    prs.save(OUT_PPTX)
    print(f"Wrote {OUT_PPTX} with {len(prs.slides)} slides")


if __name__ == "__main__":
    build_txt()
    build_pptx()
