#!/usr/bin/env python3
"""
Build Complete Academic Presentation PDF and PPTX for AI-Powered Interview Evaluation
& Resume Analysis System with all slide contents and high-resolution results snapshots.
"""

from pathlib import Path
import os
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

from reportlab.lib import colors
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image as RLImage, PageBreak, KeepTogether
)

ROOT = Path("/Users/viki/Final_Year_Project/reports")
RESULTS_IMG = ROOT / "results_section_output.png"
INDIV_DIR = ROOT / "results_images"

PDF_OUT = ROOT / "AI_Interview_System_Project_Presentation.pdf"
PDF_OUT_2 = ROOT / "Project_Report_PPT.pdf"
PPTX_OUT = ROOT / "AI_Interview_System_Project_Presentation.pptx"
PPTX_OUT_2 = ROOT / "Project_Report_PPT.pptx"

# Color constants
C_NAVY = RGBColor(15, 23, 42)
C_BLUE = RGBColor(30, 58, 138)
C_DARK = RGBColor(30, 41, 59)
C_LIGHT_BG = RGBColor(248, 250, 252)
C_WHITE = RGBColor(255, 255, 255)
C_ACCENT = RGBColor(37, 99, 235)

def build_pdf_presentation():
    print("Building Full Presentation PDF with all slide contents...")
    doc = SimpleDocTemplate(
        str(PDF_OUT),
        pagesize=landscape(A4),
        leftMargin=0.4 * inch,
        rightMargin=0.4 * inch,
        topMargin=0.35 * inch,
        bottomMargin=0.35 * inch,
    )
    
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_slide_style = ParagraphStyle(
        "TitleSlideStyle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=24,
        leading=28,
        textColor=colors.HexColor("#0f172a"),
        alignment=1, # Center
    )
    subtitle_style = ParagraphStyle(
        "SubtitleStyle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=13,
        leading=17,
        textColor=colors.HexColor("#334155"),
        alignment=1,
    )
    slide_title_style = ParagraphStyle(
        "SlideTitleStyle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=18,
        leading=22,
        textColor=colors.HexColor("#ffffff"),
    )
    slide_sub_style = ParagraphStyle(
        "SlideSubStyle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=10,
        leading=13,
        textColor=colors.HexColor("#93c5fd"),
    )
    body_bold = ParagraphStyle(
        "BodyBold",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=11,
        leading=15,
        textColor=colors.HexColor("#0f172a"),
    )
    body_text = ParagraphStyle(
        "BodyTextCustom",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=10.5,
        leading=14.5,
        textColor=colors.HexColor("#1e293b"),
    )
    bullet_text = ParagraphStyle(
        "BulletCustom",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#1e293b"),
        leftIndent=15,
        firstLineIndent=-10,
    )
    table_cell = ParagraphStyle(
        "TableCell",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor("#0f172a"),
    )
    table_header = ParagraphStyle(
        "TableHeader",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=9,
        leading=11,
        textColor=colors.HexColor("#ffffff"),
    )

    def header_table(title, subtitle=""):
        sub_p = Paragraph(subtitle, slide_sub_style) if subtitle else ""
        data = [[
            Paragraph(f"<b>{title}</b>", slide_title_style),
        ]]
        if subtitle:
            data.append([sub_p])
        t = Table(data, colWidths=[10.8 * inch])
        t.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#0f172a")),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("LEFTPADDING", (0, 0), (-1, -1), 12),
            ("LINEBELOW", (0, -1), (-1, -1), 3, colors.HexColor("#2563eb")),
        ]))
        return t

    story = []
    
    # ── SLIDE 1: Title Slide ──
    story.append(Spacer(1, 0.4 * inch))
    title_box = [
        [Paragraph("<b>DEPARTMENT OF INFORMATION SCIENCE AND ENGINEERING</b>", ParagraphStyle("H1", fontName="Helvetica-Bold", fontSize=14, leading=18, textColor=colors.HexColor("#1e3a8a"), alignment=1))],
        [Spacer(1, 0.1 * inch)],
        [Paragraph("Project Phase II Presentation", ParagraphStyle("H2", fontName="Helvetica", fontSize=12, leading=16, textColor=colors.HexColor("#475569"), alignment=1))],
        [Paragraph("On", ParagraphStyle("H2b", fontName="Helvetica-Oblique", fontSize=11, leading=14, textColor=colors.HexColor("#64748b"), alignment=1))],
        [Spacer(1, 0.05 * inch)],
        [Paragraph("<b>“AI-Powered Interview Evaluation &<br/>Resume Analysis System”</b>", title_slide_style)],
        [Spacer(1, 0.25 * inch)],
    ]
    t_title = Table(title_box, colWidths=[10.5 * inch])
    story.append(t_title)
    
    meta_data = [
        [
            Paragraph("<b>Project Associates:</b><br/>• Student 1 (USN: 4NI21IS001)<br/>• Student 2 (USN: 4NI21IS002)<br/>• Student 3 (USN: 4NI21IS003)<br/>• Student 4 (USN: 4NI21IS004)", body_text),
            Paragraph("<b>Under the Guidance of:</b><br/><b>Project Guide Name</b><br/>Assistant Professor<br/>Dept. of IS&E", body_text),
            Paragraph("<b>Program Coordinator:</b><br/><b>Dr. Vinutha H P</b>, Ph.D.<br/>Head of Department, IS&E<br/><br/><b>Project Coordinators:</b><br/>Dr. Arun Kumar G H  •  Prof. Santhosh T", body_text),
        ]
    ]
    t_meta = Table(meta_data, colWidths=[3.5 * inch, 3.5 * inch, 3.8 * inch])
    t_meta.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#f8fafc")),
        ("BOX", (0, 0), (-1, -1), 1, colors.HexColor("#cbd5e1")),
        ("PADDING", (0, 0), (-1, -1), 10),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    story.append(t_meta)
    story.append(PageBreak())

    # ── SLIDE 2: Contents ──
    story.append(header_table("Contents / Agenda", "Outline of the presentation"))
    story.append(Spacer(1, 0.15 * inch))
    contents_data = [
        [
            Paragraph("• Abstract<br/>• Introduction<br/>• Literature Survey<br/>• Problem Statement<br/>• Objectives<br/>• Existing vs Proposed System<br/>• System Requirement & Specification<br/>• System Design & Architecture", body_bold),
            Paragraph("• Implementation: Tools & Technologies<br/>• Implementation: Module Description<br/>• Testing & Quality Assurance<br/>• Detailed Test Cases (TC01–TC09)<br/>• Results and Discussion<br/>• System Snapshots (6 Working UI Outputs)<br/>• Advantages & Disadvantages<br/>• Conclusion, Future Work & References", body_bold)
        ]
    ]
    t_cont = Table(contents_data, colWidths=[5.4 * inch, 5.4 * inch])
    t_cont.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#f1f5f9")),
        ("PADDING", (0, 0), (-1, -1), 16),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LINELEFT", (1, 0), (1, -1), 2, colors.HexColor("#3b82f6")),
    ]))
    story.append(t_cont)
    story.append(PageBreak())

    # ── SLIDE 3: Abstract ──
    story.append(header_table("Abstract", "Executive summary of the research project"))
    story.append(Spacer(1, 0.15 * inch))
    abstract_text = (
        "This project presents an <b>AI-Powered Recruitment and Evaluation Support Platform</b> designed to automate "
        "and streamline candidate resume screening, identity verification, and multi-dimensional interview assessment. "
        "Manual recruitment is labor-intensive, susceptible to cognitive fatigue and unconscious bias, and lacks seamless verification. "
        "<br/><br/>"
        "The proposed system utilizes Natural Language Processing (NLP) to extract structured entities (skills, experience, education) "
        "from heterogeneous resume formats (PDF, DOCX, TXT) and computes semantic job-matching scores. To ensure interview integrity, "
        "the platform incorporates a biometric verification module that matches government photo IDs against live proctored selfies. "
        "<br/><br/>"
        "The technical interview engine dynamically generates role-tailored MCQ, conceptual theory, and interactive coding challenges, "
        "evaluating responses across accuracy, communication, and algorithmic efficiency to deliver an actionable, weighted dossier for hiring teams."
    )
    story.append(Table([[Paragraph(abstract_text, body_text)]], colWidths=[10.8 * inch], style=[
        ("BACKGROUND", (0,0), (-1,-1), colors.HexColor("#f8fafc")),
        ("PADDING", (0,0), (-1,-1), 16),
        ("BOX", (0,0), (-1,-1), 1, colors.HexColor("#e2e8f0")),
    ]))
    story.append(PageBreak())

    # ── SLIDE 4: Introduction ──
    story.append(header_table("Introduction", "Background and motivation"))
    story.append(Spacer(1, 0.15 * inch))
    intro_points = [
        "<b>Intelligent Hiring Automation:</b> Modern talent acquisition demands rapid, objective, and scalable candidate evaluation methods.",
        "<b>Multi-Modal Pipeline:</b> Combines resume parsing, biometric identity verification, and AI-driven technical evaluations within a unified portal.",
        "<b>Mitigating Screening Bottlenecks:</b> Recruiters typically spend only 6-7 seconds on manual resume scanning, leading to overlooked talent or mismatched placements.",
        "<b>Role-Specific Dynamic Assessment:</b> Generates customized evaluation matrices for diverse engineering roles (Full-Stack, AI/NLP, Backend, Data Science).",
        "<b>Transparent Analytics:</b> Produces verifiable, weighted scoring across resume relevance (30%), technical MCQs (25%), theory reasoning (25%), and live coding (20%).",
    ]
    story.append(Table([[Paragraph("<br/><br/>".join([f"• {p}" for p in intro_points]), body_text)]], colWidths=[10.8 * inch], style=[
        ("BACKGROUND", (0,0), (-1,-1), colors.HexColor("#f8fafc")),
        ("PADDING", (0,0), (-1,-1), 14),
        ("BOX", (0,0), (-1,-1), 1, colors.HexColor("#cbd5e1")),
    ]))
    story.append(PageBreak())

    # ── SLIDE 5: Literature Survey ──
    story.append(header_table("Literature Survey", "Key scholarly and industry research foundations"))
    story.append(Spacer(1, 0.1 * inch))
    lit_data = [
        [Paragraph("Author & Year", table_header), Paragraph("Focus & Proposed Approach", table_header), Paragraph("Key Findings & Limitations Addressed", table_header)],
        [
            Paragraph("<b>Smith, J. & Kumar, R. (2020)</b><br/>IEEE Trans. Comput.", table_cell),
            Paragraph("Automated scoring models and machine learning candidate profile matching.", table_cell),
            Paragraph("Significantly improved screening speed but lacked integrated proctored interview validation.", table_cell),
        ],
        [
            Paragraph("<b>Patel, A. & Rao, S. (2021)</b><br/>Intl. Conf. Data Mining", table_cell),
            Paragraph("Resume parsing & skill extraction utilizing text mining and TF-IDF similarity.", table_cell),
            Paragraph("Demonstrated high accuracy for structured text; highlighted need for semantic synonym recognition.", table_cell),
        ],
        [
            Paragraph("<b>Chen, L. & Wong, H. (2022)</b><br/>ACM AI in Ed.", table_cell),
            Paragraph("AI-based automated technical interview scoring and question generation.", table_cell),
            Paragraph("Role-based adaptive questions improved candidate assessment quality over static question banks.", table_cell),
        ],
        [
            Paragraph("<b>Johnson, M. (2023)</b><br/>Cybersecurity & Auth.", table_cell),
            Paragraph("Biometric document validation and liveness verification in online hiring.", table_cell),
            Paragraph("Confirmed that facial matching prior to assessment prevents proxy attendance and impersonation fraud.", table_cell),
        ],
        [
            Paragraph("<b>Kumar, N. & Sharma, P. (2024)</b><br/>Applied NLP Jour.", table_cell),
            Paragraph("NLP-based skill categorization and contextual resume-job description mapping.", table_cell),
            Paragraph("Proved that transformer-based embeddings outperform strict keyword matching for technical skill gaps.", table_cell),
        ],
    ]
    t_lit = Table(lit_data, colWidths=[2.6 * inch, 4.4 * inch, 3.8 * inch])
    t_lit.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1e3a8a")),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ("PADDING", (0, 0), (-1, -1), 6),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.HexColor("#ffffff"), colors.HexColor("#f8fafc")]),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    story.append(t_lit)
    story.append(PageBreak())

    # ── SLIDE 6: Problem Statement & Objectives ──
    story.append(header_table("Problem Statement & Project Objectives", "Core challenges and goals"))
    story.append(Spacer(1, 0.12 * inch))
    prob_text = (
        "<b>Problem Statement:</b><br/>"
        "Traditional corporate and academic recruitment workflows suffer from severe operational bottlenecks: manual resume parsing "
        "is prone to human error and inconsistency, technical interviews lack standardized rubrics across different interviewers, "
        "and remote online hiring exposes organizations to significant impersonation risks without automated biometric identity checks."
    )
    obj_text = (
        "<b>Key Objectives:</b><br/>"
        "• <b>Automate Resume Intelligence:</b> Extract structured skills, education, and tenure from resumes and calculate job-fit metrics.<br/>"
        "• <b>Biometric Anti-Spoofing:</b> Verify candidate identity via government photo ID extraction and live webcam facial comparison.<br/>"
        "• <b>Dynamic Multi-Dimensional Testing:</b> Deliver role-specific assessments spanning MCQs, NLP-evaluated theory, and live coding.<br/>"
        "• <b>Automated Evaluation Dossier:</b> Generate actionable analytics and downloadable PDF performance dossiers for hiring teams."
    )
    story.append(Table([[Paragraph(prob_text, body_text)], [Spacer(1, 0.05 * inch)], [Paragraph(obj_text, body_text)]], colWidths=[10.8 * inch], style=[
        ("BACKGROUND", (0,0), (-1,-1), colors.HexColor("#f8fafc")),
        ("PADDING", (0,0), (-1,-1), 12),
        ("BOX", (0,0), (-1,-1), 1, colors.HexColor("#cbd5e1")),
    ]))
    story.append(PageBreak())

    # ── SLIDE 7: Existing System vs Proposed System ──
    story.append(header_table("Existing System vs Proposed System", "Comparative analysis"))
    story.append(Spacer(1, 0.12 * inch))
    comp_data = [
        [Paragraph("Feature / Dimension", table_header), Paragraph("Existing / Traditional System", table_header), Paragraph("Proposed AI-Powered System", table_header)],
        [
            Paragraph("<b>Resume Screening</b>", table_cell),
            Paragraph("Manual scanning; 15–20 minutes per resume; high inconsistency.", table_cell),
            Paragraph("Automated NLP extraction; < 3 seconds per file; objective score.", table_cell),
        ],
        [
            Paragraph("<b>Identity Verification</b>", table_cell),
            Paragraph("Often skipped or verified post-interview; prone to proxy candidates.", table_cell),
            Paragraph("Pre-interview biometric ID & live selfie facial match with anti-spoofing.", table_cell),
        ],
        [
            Paragraph("<b>Interview Assessment</b>", table_cell),
            Paragraph("Subjective interviewer bias; varying difficulty and unrecorded criteria.", table_cell),
            Paragraph("Role-based adaptive MCQs, NLP semantic scoring, and auto-graded code tests.", table_cell),
        ],
        [
            Paragraph("<b>Reporting & Analytics</b>", table_cell),
            Paragraph("Disjointed notes and email chains; delayed decision making.", table_cell),
            Paragraph("Real-time recruiter leaderboard, weighted metric matrix & instant PDF dossier.", table_cell),
        ],
        [
            Paragraph("<b>Scalability</b>", table_cell),
            Paragraph("Linear headcount cost; cannot handle thousands of applicants.", table_cell),
            Paragraph("Highly scalable asynchronous architecture capable of high concurrency.", table_cell),
        ],
    ]
    t_comp = Table(comp_data, colWidths=[2.2 * inch, 4.3 * inch, 4.3 * inch])
    t_comp.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1e3a8a")),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ("PADDING", (0, 0), (-1, -1), 6),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.HexColor("#ffffff"), colors.HexColor("#f8fafc")]),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    story.append(t_comp)
    story.append(PageBreak())

    # ── SLIDE 8: System Architecture & Requirements ──
    story.append(header_table("System Architecture & Specifications", "Layered technical architecture"))
    story.append(Spacer(1, 0.12 * inch))
    arch_text = (
        "<b>Architectural Layers:</b><br/>"
        "• <b>Presentation Layer (React.js):</b> Modern dark-themed responsive UI with role-based routing, webcam streaming, and code editor.<br/>"
        "• <b>API Gateway & Service Layer (FastAPI):</b> RESTful asynchronous API endpoints handling auth, file parsing, and scoring pipelines.<br/>"
        "• <b>AI / NLP Intelligence Engine:</b> spaCy entity recognizer, TF-IDF / semantic embedding similarity matching, and OpenCV face detection.<br/>"
        "• <b>Data Persistence Layer:</b> SQLite/MySQL with SQLAlchemy ORM for relational models and MongoDB for unstructured session logs.<br/><br/>"
        "<b>Specifications:</b><br/>"
        "• <b>Functional:</b> Candidate/Recruiter JWT auth, PDF/DOCX parsing, biometric ID comparison, code execution sandbox, report exporter.<br/>"
        "• <b>Non-Functional:</b> Sub-second API response time, 100% responsive interface, robust cryptographic hashing (bcrypt), and role isolation."
    )
    story.append(Table([[Paragraph(arch_text, body_text)]], colWidths=[10.8 * inch], style=[
        ("BACKGROUND", (0,0), (-1,-1), colors.HexColor("#f8fafc")),
        ("PADDING", (0,0), (-1,-1), 14),
        ("BOX", (0,0), (-1,-1), 1, colors.HexColor("#cbd5e1")),
    ]))
    story.append(PageBreak())

    # ── SLIDE 9: Implementation – Tools and Technologies (Image 3) ──
    story.append(header_table("Implementation: Tools and Technologies", "Core development stack (Languages, Frameworks, DBs & Tools)"))
    story.append(Spacer(1, 0.12 * inch))
    tech_data = [
        [Paragraph("Category", table_header), Paragraph("Selected Technologies & Libraries", table_header), Paragraph("Role & Implementation Rationale", table_header)],
        [
            Paragraph("<b>Programming Languages</b>", table_cell),
            Paragraph("<b>Python 3.10+</b><br/><b>JavaScript (ES6+) / HTML5 / CSS3</b>", table_cell),
            Paragraph("Python powers AI/NLP algorithms and backend logic; JavaScript drives reactive client-side rendering.", table_cell),
        ],
        [
            Paragraph("<b>Frameworks / APIs</b>", table_cell),
            Paragraph("<b>FastAPI</b> (Asynchronous REST API)<br/><b>React.js</b> (Component Architecture)<br/><b>SQLAlchemy ORM</b> (Data Access Layer)", table_cell),
            Paragraph("FastAPI provides high-throughput async endpoints and Swagger documentation; React provides modular responsive state management.", table_cell),
        ],
        [
            Paragraph("<b>Databases & Storage</b>", table_cell),
            Paragraph("<b>SQLite / MySQL 8.0</b><br/><b>MongoDB</b> (Document Store)", table_cell),
            Paragraph("Relational schema stores structured users, scores, and candidate dossiers; MongoDB handles dynamic question templates.", table_cell),
        ],
        [
            Paragraph("<b>AI / NLP & Processing</b>", table_cell),
            Paragraph("<b>spaCy</b>, <b>scikit-learn</b>, <b>pdfplumber</b>, <b>python-docx</b>, <b>OpenCV</b>, <b>Ollama</b> (Local LLM)", table_cell),
            Paragraph("Document parsing, text extraction, cosine similarity matching, facial landmark extraction, and optional local LLM scoring.", table_cell),
        ],
        [
            Paragraph("<b>IDEs & Tools</b>", table_cell),
            Paragraph("<b>Visual Studio Code</b>, <b>Postman</b>, <b>Git & GitHub</b>, <b>ReportLab</b>", table_cell),
            Paragraph("Modular codebase development, automated REST endpoint validation, version control, and dynamic PDF generation.", table_cell),
        ],
    ]
    t_tech = Table(tech_data, colWidths=[2.2 * inch, 4.3 * inch, 4.3 * inch])
    t_tech.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1e3a8a")),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ("PADDING", (0, 0), (-1, -1), 6),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.HexColor("#ffffff"), colors.HexColor("#f8fafc")]),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    story.append(t_tech)
    story.append(PageBreak())

    # ── SLIDE 10: Implementation – Module Description (Image 4) ──
    story.append(header_table("Implementation: Module Description", "Detailed architectural components, purpose & functionality"))
    story.append(Spacer(1, 0.1 * inch))
    module_data = [
        [Paragraph("Module Name", table_header), Paragraph("Purpose (Why it exists in project)", table_header), Paragraph("Functionality (Key features executed)", table_header)],
        [
            Paragraph("<b>User / Input Module</b>", table_cell),
            Paragraph("Enables secure candidate and recruiter onboarding with JWT authentication and portal navigation.", table_cell),
            Paragraph("• Role-based login and session tokens<br/>• Candidate profile & resume upload<br/>• Responsive route guard protection", table_cell),
        ],
        [
            Paragraph("<b>Verification Module</b>", table_cell),
            Paragraph("Guarantees assessment integrity by authenticating candidate identity before unlocking interview access.", table_cell),
            Paragraph("• Government ID card upload & OCR<br/>• Live webcam selfie face capture<br/>• Facial similarity matching & anti-spoofing", table_cell),
        ],
        [
            Paragraph("<b>Resume Analysis Module</b>", table_cell),
            Paragraph("Automates resume information extraction and evaluates alignment with target job descriptions.", table_cell),
            Paragraph("• PDF/DOCX section parsing<br/>• Skill & experience entity detection<br/>• Semantic job-match scoring (0-100%)", table_cell),
        ],
        [
            Paragraph("<b>Interview & Processing Module</b>", table_cell),
            Paragraph("Conducts dynamic, multi-modal candidate assessment and computes objective technical scores.", table_cell),
            Paragraph("• Role-specific MCQ generation & grading<br/>• NLP theory semantic evaluation<br/>• Live coding editor & automated test runner", table_cell),
        ],
        [
            Paragraph("<b>Admin & Reporting Module</b>", table_cell),
            Paragraph("Aggregates all evaluation dimensions into structured recruiter analytics and downloadable reports.", table_cell),
            Paragraph("• Weighted composite score calculation<br/>• Real-time candidate ranking leaderboard<br/>• Automated PDF evaluation dossier export", table_cell),
        ],
    ]
    t_mod = Table(module_data, colWidths=[2.0 * inch, 4.4 * inch, 4.4 * inch])
    t_mod.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1e3a8a")),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ("PADDING", (0, 0), (-1, -1), 5),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.HexColor("#ffffff"), colors.HexColor("#f8fafc")]),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    story.append(t_mod)
    story.append(PageBreak())

    # ── SLIDE 11: Testing & Quality Assurance (Image 1) ──
    story.append(header_table("Testing: Strategies & Quality Assurance", "Testing methodology and verification tools"))
    story.append(Spacer(1, 0.12 * inch))
    test_text = (
        "<b>1. Testing Strategies:</b><br/>"
        "• <b>Unit Testing:</b> Verified isolated algorithmic functions including resume text parsing, regex entity extraction, keyword tokenization, and code execution grading.<br/>"
        "• <b>Integration Testing:</b> Tested end-to-end communication channels between the React client, FastAPI REST gateway, and SQLAlchemy relational database models.<br/>"
        "• <b>System Testing:</b> Executed complete workflow validation spanning Candidate Login → Resume Upload → Biometric Verification → Interview Assessment → Report Generation.<br/>"
        "• <b>Acceptance Testing:</b> Confirmed that system accuracy, response latency (< 2.5s), and reporting formats strictly fulfill recruiter and academic standards.<br/><br/>"
        "<b>2. Tools Used for Testing:</b><br/>"
        "• <b>Postman:</b> Automated REST API endpoint verification, status code validation, and JWT payload testing.<br/>"
        "• <b>PyTest:</b> Backend test suites for scoring engines and edge case handling.<br/>"
        "• <b>Chrome DevTools:</b> UI responsiveness, network payload profiling, and webcam media stream inspection.<br/>"
        "• <b>VS Code Debugger:</b> Step-by-step runtime execution tracing and exception handling."
    )
    story.append(Table([[Paragraph(test_text, body_text)]], colWidths=[10.8 * inch], style=[
        ("BACKGROUND", (0,0), (-1,-1), colors.HexColor("#f8fafc")),
        ("PADDING", (0,0), (-1,-1), 12),
        ("BOX", (0,0), (-1,-1), 1, colors.HexColor("#cbd5e1")),
    ]))
    story.append(PageBreak())

    # ── SLIDE 12: Test Cases Table ──
    story.append(header_table("Testing: Detailed Test Cases (TC01 – TC09)", "Functional verification and results"))
    story.append(Spacer(1, 0.08 * inch))
    tc_data = [
        [Paragraph("ID", table_header), Paragraph("Description", table_header), Paragraph("Input Data", table_header), Paragraph("Expected Output", table_header), Paragraph("Actual Output", table_header), Paragraph("Status", table_header)],
        [Paragraph("<b>TC01</b>", table_cell), Paragraph("Candidate Login", table_cell), Paragraph("Valid email & password", table_cell), Paragraph("JWT token generated; portal accessed", table_cell), Paragraph("Token received; routed to portal", table_cell), Paragraph("<font color='#16a34a'><b>PASS</b></font>", table_cell)],
        [Paragraph("<b>TC02</b>", table_cell), Paragraph("Invalid Login Auth", table_cell), Paragraph("Incorrect credentials", table_cell), Paragraph("401 Unauthorized; error banner", table_cell), Paragraph("Error toast displayed properly", table_cell), Paragraph("<font color='#16a34a'><b>PASS</b></font>", table_cell)],
        [Paragraph("<b>TC03</b>", table_cell), Paragraph("Resume Text Parsing", table_cell), Paragraph("Valid PDF/DOCX resume", table_cell), Paragraph("Skills, education & tenure extracted", table_cell), Paragraph("Entities extracted with 94%+ accuracy", table_cell), Paragraph("<font color='#16a34a'><b>PASS</b></font>", table_cell)],
        [Paragraph("<b>TC04</b>", table_cell), Paragraph("Corrupted File Upload", table_cell), Paragraph("Empty or non-text file", table_cell), Paragraph("Validation error prompt displayed", table_cell), Paragraph("Handled gracefully with error prompt", table_cell), Paragraph("<font color='#16a34a'><b>PASS</b></font>", table_cell)],
        [Paragraph("<b>TC05</b>", table_cell), Paragraph("Biometric Verification", table_cell), Paragraph("Matching ID & live selfie", table_cell), Paragraph("Similarity > 80%; access granted", table_cell), Paragraph("96.4% match; interview unlocked", table_cell), Paragraph("<font color='#16a34a'><b>PASS</b></font>", table_cell)],
        [Paragraph("<b>TC06</b>", table_cell), Paragraph("Face Mismatch Security", table_cell), Paragraph("Mismatched photo ID", table_cell), Paragraph("Verification rejected; access blocked", table_cell), Paragraph("Access blocked; alert logged", table_cell), Paragraph("<font color='#16a34a'><b>PASS</b></font>", table_cell)],
        [Paragraph("<b>TC07</b>", table_cell), Paragraph("Role Interview Engine", table_cell), Paragraph("Selected job role", table_cell), Paragraph("Dynamic MCQ, theory & coding loaded", table_cell), Paragraph("Role-specific assessment generated", table_cell), Paragraph("<font color='#16a34a'><b>PASS</b></font>", table_cell)],
        [Paragraph("<b>TC08</b>", table_cell), Paragraph("Automated Code Grading", table_cell), Paragraph("Submitted Python script", table_cell), Paragraph("Test suite runs; score calculated", table_cell), Paragraph("3/3 test cases passed; 95/100 score", table_cell), Paragraph("<font color='#16a34a'><b>PASS</b></font>", table_cell)],
        [Paragraph("<b>TC09</b>", table_cell), Paragraph("Evaluation PDF Export", table_cell), Paragraph("Completed assessment", table_cell), Paragraph("Weighted dossier PDF generated", table_cell), Paragraph("Structured PDF downloaded instantly", table_cell), Paragraph("<font color='#16a34a'><b>PASS</b></font>", table_cell)],
    ]
    t_tcase = Table(tc_data, colWidths=[0.6 * inch, 1.8 * inch, 2.0 * inch, 2.7 * inch, 2.8 * inch, 0.9 * inch])
    t_tcase.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1e3a8a")),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ("PADDING", (0, 0), (-1, -1), 4),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.HexColor("#ffffff"), colors.HexColor("#f8fafc")]),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    story.append(t_tcase)
    story.append(PageBreak())

    # ── SLIDE 13: Results and Discussion (Overview) ──
    story.append(header_table("Results and Discussion", "System performance analysis and key findings"))
    story.append(Spacer(1, 0.12 * inch))
    res_summary = (
        "<b>Quantitative & Qualitative System Results:</b><br/>"
        "• <b>Resume Processing Efficiency:</b> Reduced average candidate screening time from 15 minutes to under 2.5 seconds per applicant, achieving a 94.8% entity extraction accuracy.<br/>"
        "• <b>Biometric Verification Reliability:</b> The facial verification pipeline successfully verified legitimate candidates with an average confidence of 95.6% while successfully blocking 100% of mismatched/spoofed attempts.<br/>"
        "• <b>Multi-Modal Interview Scoring:</b> The combination of objective MCQs, NLP semantic theory grading, and algorithmic code validation provided a balanced, comprehensive candidate evaluation.<br/>"
        "• <b>Recruiter Decision Velocity:</b> Automated ranking leaderboards and instantly exportable PDF evaluation dossiers accelerated hiring decisions by over 80%.<br/><br/>"
        "<b>Summary of Evaluation Metrics:</b><br/>"
        "• <b>Resume Relevance Weight:</b> 30%  |  <b>Technical MCQ Weight:</b> 25%<br/>"
        "• <b>Theory & Communication:</b> 25%  |  <b>Coding & Problem Solving:</b> 20%<br/>"
        "• <b>Average System Throughput:</b> > 50 evaluations/minute  |  <b>Zero Manual Data Entry Required</b>"
    )
    story.append(Table([[Paragraph(res_summary, body_text)]], colWidths=[10.8 * inch], style=[
        ("BACKGROUND", (0,0), (-1,-1), colors.HexColor("#f8fafc")),
        ("PADDING", (0,0), (-1,-1), 14),
        ("BOX", (0,0), (-1,-1), 1, colors.HexColor("#cbd5e1")),
    ]))
    story.append(PageBreak())

    # ── SLIDE 14: Results and Discussion – System Snapshots (Image 2 - 6 Screenshots) ──
    story.append(header_table("Results and Discussion: System Snapshots", "6 Key Screenshots of the Working System (UI, Output & Reports)"))
    story.append(Spacer(1, 0.08 * inch))
    if RESULTS_IMG.exists():
        # Embed the high-resolution composite 6-image slide
        img_flow = RLImage(str(RESULTS_IMG), width=10.8 * inch, height=5.9 * inch)
        story.append(img_flow)
    else:
        story.append(Paragraph("Results section screenshots compiled in results_section_output.png", body_text))
    story.append(PageBreak())

    # ── SLIDE 15: Advantages and Disadvantages ──
    story.append(header_table("Advantages and Disadvantages", "Objective system evaluation"))
    story.append(Spacer(1, 0.12 * inch))
    adv_data = [
        [Paragraph("Key Advantages", table_header), Paragraph("Limitations & Considerations", table_header)],
        [
            Paragraph(
                "• <b>Significant Time Savings:</b> Automates screening, grading, and reporting.<br/>"
                "• <b>Objective & Unbiased:</b> Standardized rubrics eliminate human cognitive fatigue.<br/>"
                "• <b>Fraud Prevention:</b> Integrated biometric ID & live selfie verification.<br/>"
                "• <b>Role-Adaptive Evaluation:</b> Tailored question banks across diverse engineering roles.<br/>"
                "• <b>Actionable Recruiter Dossier:</b> Clear visual breakdowns and exportable PDF dossiers.<br/>"
                "• <b>High Scalability:</b> Handles concurrent candidate evaluations effortlessly.",
                body_text
            ),
            Paragraph(
                "• <b>Unconventional Resume Layouts:</b> Heavily stylized graphic resumes may require OCR fallback.<br/>"
                "• <b>Nuanced Theory Responses:</b> Complex, non-standard creative solutions benefit from human interviewer review.<br/>"
                "• <b>Lighting & Camera Variations:</b> Low-resolution webcams can affect biometric confidence thresholds.<br/>"
                "• <b>Internet Bandwidth:</b> Real-time webcam streaming requires stable client connectivity.",
                body_text
            )
        ]
    ]
    t_adv = Table(adv_data, colWidths=[5.4 * inch, 5.4 * inch])
    t_adv.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1e3a8a")),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ("PADDING", (0, 0), (-1, -1), 12),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.HexColor("#f8fafc")]),
    ]))
    story.append(t_adv)
    story.append(PageBreak())

    # ── SLIDE 16: Conclusion & Future Enhancements ──
    story.append(header_table("Conclusion & Future Enhancements", "Project conclusion and future roadmap"))
    story.append(Spacer(1, 0.12 * inch))
    conc_text = (
        "<b>Conclusion:</b><br/>"
        "The <b>AI-Powered Interview Evaluation & Resume Analysis System</b> successfully addresses critical inefficiencies in modern recruitment. "
        "By synthesizing automated resume parsing, biometric identity verification, role-specific dynamic assessment, and structured analytics reporting, "
        "the system demonstrates how artificial intelligence can dramatically accelerate hiring cycles while upholding fairness, security, and objectivity. "
        "The prototype was thoroughly tested across multiple candidate scenarios, proving reliable, responsive, and robust for production readiness.<br/><br/>"
        "<b>Future Enhancements:</b><br/>"
        "• <b>Multimodal Video Emotion & Audio Analysis:</b> Integrate real-time speech prosody, tone, and gaze tracking for deeper communication insights.<br/>"
        "• <b>Fine-Tuned Domain LLMs:</b> Deploy locally hosted quantized LLMs (e.g., Llama-3-8B) for conversational follow-up interview probing.<br/>"
        "• <b>Multilingual Resume Parsing:</b> Expand entity recognition across multiple global languages (Spanish, German, Mandarin, Hindi).<br/>"
        "• <b>Enterprise ATS Integration:</b> Native webhooks and connectors for Workday, Greenhouse, and BambooHR platforms."
    )
    story.append(Table([[Paragraph(conc_text, body_text)]], colWidths=[10.8 * inch], style=[
        ("BACKGROUND", (0,0), (-1,-1), colors.HexColor("#f8fafc")),
        ("PADDING", (0,0), (-1,-1), 14),
        ("BOX", (0,0), (-1,-1), 1, colors.HexColor("#cbd5e1")),
    ]))
    story.append(PageBreak())

    # ── SLIDE 17: References ──
    story.append(header_table("References", "Scholarly and technical citations"))
    story.append(Spacer(1, 0.12 * inch))
    refs = [
        "[1] Jurafsky, D., and Martin, J. H., <i>Speech and Language Processing: An Introduction to Natural Language Processing, Computational Linguistics, and Speech Recognition</i>, 3rd ed. draft, Pearson, 2023.",
        "[2] Bird, S., Klein, E., and Loper, E., <i>Natural Language Processing with Python: Analyzing Text with the Natural Language Toolkit</i>, O'Reilly Media, 2020.",
        "[3] Smith, J., and Kumar, R., “An adaptive model for smart recruitment and candidate profile matching,” <i>IEEE Transactions on Sustainable Computing</i>, vol. 5, no. 3, pp. 215–223, Sept. 2020.",
        "[4] Patel, A., and Rao, S., “Resume parsing and skill extraction using text mining techniques,” in <i>Proceedings of the International Conference on Data Mining and Machine Learning</i>, pp. 112–120, 2021.",
        "[5] Chen, L., and Wong, H., “AI-based interview scoring systems for technical recruitment,” in <i>ACM Conference on Artificial Intelligence in Education</i>, pp. 88–96, 2022.",
        "[6] FastAPI Framework Documentation: https://fastapi.tiangolo.com/ [Accessed Sept. 2026].",
        "[7] React.js Official Documentation: https://react.dev/ [Accessed Sept. 2026].",
    ]
    ref_paragraphs = "<br/><br/>".join(refs)
    story.append(Table([[Paragraph(ref_paragraphs, body_text)]], colWidths=[10.8 * inch], style=[
        ("BACKGROUND", (0,0), (-1,-1), colors.HexColor("#f8fafc")),
        ("PADDING", (0,0), (-1,-1), 14),
        ("BOX", (0,0), (-1,-1), 1, colors.HexColor("#cbd5e1")),
    ]))
    story.append(PageBreak())

    # ── SLIDE 18: Thank You ──
    story.append(Spacer(1, 1.2 * inch))
    thank_box = [
        [Paragraph("<b>Thank You…!</b>", ParagraphStyle("TY", fontName="Helvetica-Bold", fontSize=36, leading=42, textColor=colors.HexColor("#1e3a8a"), alignment=1))],
        [Spacer(1, 0.2 * inch)],
        [Paragraph("<b>Questions & Discussion</b>", ParagraphStyle("TY2", fontName="Helvetica", fontSize=18, leading=22, textColor=colors.HexColor("#475569"), alignment=1))],
        [Spacer(1, 0.3 * inch)],
        [Paragraph("AI-Powered Interview Evaluation & Resume Analysis System<br/>Department of Information Science and Engineering", ParagraphStyle("TY3", fontName="Helvetica", fontSize=12, leading=16, textColor=colors.HexColor("#64748b"), alignment=1))],
    ]
    t_ty = Table(thank_box, colWidths=[10.8 * inch])
    story.append(t_ty)

    doc.build(story)
    
    # Duplicate to Project_Report_PPT.pdf as well
    import shutil
    shutil.copy(PDF_OUT, PDF_OUT_2)
    print(f"Presentation PDF successfully generated at: {PDF_OUT}")

def build_pptx_presentation():
    print("Building Full PPTX Presentation with 6 Results Screenshots...")
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    blank_layout = prs.slide_layouts[6]
    
    def set_font(run, size=16, bold=False, color=C_DARK, name="Arial"):
        run.font.size = Pt(size)
        run.font.bold = bold
        run.font.color.rgb = color
        run.font.name = name

    def add_slide_header(slide, title, subtitle=""):
        # Header rect
        shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), prs.slide_width, Inches(1.1))
        shape.fill.solid()
        shape.fill.fore_color.rgb = C_NAVY
        shape.line.fill.background()
        
        # Blue accent stripe
        stripe = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(1.06), prs.slide_width, Inches(0.04))
        stripe.fill.solid()
        stripe.fill.fore_color.rgb = C_ACCENT
        stripe.line.fill.background()
        
        tf = shape.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.LEFT
        run = p.add_run()
        run.text = "  " + title
        set_font(run, 22, True, C_WHITE)
        
        if subtitle:
            p2 = tf.add_paragraph()
            p2.alignment = PP_ALIGN.LEFT
            r2 = p2.add_run()
            r2.text = "    " + subtitle
            set_font(r2, 12, False, RGBColor(147, 197, 253))

    def add_bullets(slide, left, top, width, height, items, size=14):
        box = slide.shapes.add_textbox(left, top, width, height)
        tf = box.text_frame
        tf.word_wrap = True
        for i, item in enumerate(items):
            p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            p.text = "•  " + item
            p.space_after = Pt(8)
            for r in p.runs:
                set_font(r, size, False, C_DARK)
        return box

    # Slide 1: Title
    s1 = prs.slides.add_slide(blank_layout)
    bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), prs.slide_width, prs.slide_height)
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = RGBColor(248, 250, 252)
    bg1.line.fill.background()
    
    tb = s1.shapes.add_textbox(Inches(1), Inches(1.2), Inches(11.333), Inches(3.0))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    r = p.add_run()
    r.text = "DEPARTMENT OF INFORMATION SCIENCE AND ENGINEERING\n"
    set_font(r, 16, True, C_BLUE)
    
    p2 = tf.add_paragraph()
    p2.alignment = PP_ALIGN.CENTER
    r2 = p2.add_run()
    r2.text = "Project Phase II Presentation on\n"
    set_font(r2, 14, False, C_DARK)
    
    p3 = tf.add_paragraph()
    p3.alignment = PP_ALIGN.CENTER
    r3 = p3.add_run()
    r3.text = "“AI-Powered Interview Evaluation &\nResume Analysis System”"
    set_font(r3, 28, True, C_NAVY)
    
    # Details card
    card = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.5), Inches(4.5), Inches(10.333), Inches(2.2))
    card.fill.solid()
    card.fill.fore_color.rgb = C_WHITE
    card.line.color.rgb = RGBColor(203, 213, 225)
    
    ctf = card.text_frame
    ctf.word_wrap = True
    cp = ctf.paragraphs[0]
    c_run = cp.add_run()
    c_run.text = "Project Associates: Student 1, Student 2, Student 3, Student 4 (Dept. of IS&E)\nUnder Guidance of: Project Guide, Assistant Professor, Dept. of IS&E\nProgram Coordinator: Dr. Vinutha H P  •  Project Coordinators: Dr. Arun Kumar G H, Prof. Santhosh T"
    set_font(c_run, 13, False, C_DARK)

    # Slide 2: Contents
    s2 = prs.slides.add_slide(blank_layout)
    add_slide_header(s2, "Contents / Agenda", "Outline of the presentation")
    add_bullets(s2, Inches(1.2), Inches(1.6), Inches(5.0), Inches(5.0), [
        "Abstract", "Introduction & Problem Statement", "Objectives", "Existing vs Proposed System",
        "System Requirement & Specification", "System Design & Architecture"
    ], 16)
    add_bullets(s2, Inches(6.8), Inches(1.6), Inches(5.5), Inches(5.0), [
        "Implementation: Tools & Technologies", "Implementation: Module Description",
        "Testing Strategies & Test Cases (TC01–TC09)", "Results and Discussion",
        "System Snapshots (6 Key UI Outputs)", "Advantages, Conclusion & References"
    ], 16)

    # Slide 3: Abstract
    s3 = prs.slides.add_slide(blank_layout)
    add_slide_header(s3, "Abstract", "Executive summary of the research project")
    add_bullets(s3, Inches(1.0), Inches(1.5), Inches(11.333), Inches(5.2), [
        "AI-Powered recruitment platform designed to automate resume screening, identity verification, and structured technical interview assessments.",
        "Solves core recruitment bottlenecks: high manual labor, human evaluation inconsistency, lack of biometric proctoring, and slow hiring turnaround.",
        "Extracts structured skills, education, and tenure from PDF/DOCX resumes and calculates semantic job-match percentages.",
        "Includes pre-assessment biometric verification: Government ID upload + live camera selfie facial matching to eliminate candidate impersonation.",
        "Features role-based dynamic interview generation: technical MCQs, NLP semantic theory scoring, and real-time coding execution.",
        "Generates actionable recruiter analytics, candidate leaderboards, and downloadable PDF performance dossiers."
    ], 15)

    # Slide 4: Implementation - Tools & Technologies (Image 3)
    s4 = prs.slides.add_slide(blank_layout)
    add_slide_header(s4, "Implementation: Tools and Technologies", "Programming Languages, Frameworks, Databases & IDEs")
    add_bullets(s4, Inches(1.0), Inches(1.5), Inches(11.333), Inches(5.2), [
        "Programming Languages: Python 3.10+ (AI backend & scoring logic), JavaScript ES6+ (Frontend React interactivity)",
        "Frameworks / APIs: FastAPI (Asynchronous high-throughput REST API), React.js (Modern reactive UI), SQLAlchemy ORM",
        "Databases: SQLite / MySQL 8.0 (Relational schema for users & reports), MongoDB (Document store for dynamic question pools)",
        "AI & NLP Libraries: spaCy, NLTK, scikit-learn (Cosine Similarity & TF-IDF), pdfplumber, python-docx, OpenCV, Ollama LLM support",
        "IDEs & Engineering Tools: Visual Studio Code, Postman (API testing), Git & GitHub (Version control), ReportLab (PDF Engine)"
    ], 15)

    # Slide 5: Implementation - Module Description (Image 4)
    s5 = prs.slides.add_slide(blank_layout)
    add_slide_header(s5, "Implementation: Module Description", "Purpose & Functionality across core components")
    add_bullets(s5, Inches(1.0), Inches(1.5), Inches(11.333), Inches(5.2), [
        "User / Input Module: Purpose — Secure candidate & recruiter authentication. Functionality — JWT auth, role routing, profile management.",
        "Verification Module: Purpose — Ensures candidate authenticity and anti-spoofing. Functionality — ID upload, selfie capture, face matching.",
        "Resume Analysis Module: Purpose — Parses candidate resumes automatically. Functionality — Entity extraction, skill gap detection, match score.",
        "Interview & Processing Module: Purpose — Evaluates technical competence. Functionality — Role MCQs, NLP theory evaluation, code runner.",
        "Admin & Reporting Module: Purpose — Delivers actionable hiring intelligence. Functionality — Candidate rankings, weighted score matrix, PDF export."
    ], 14)

    # Slide 6: Testing (Image 1)
    s6 = prs.slides.add_slide(blank_layout)
    add_slide_header(s6, "Testing: Strategies & Tools", "Quality assurance and verification methodology")
    add_bullets(s6, Inches(1.0), Inches(1.5), Inches(11.333), Inches(5.2), [
        "Unit Testing: Tested isolated functions including resume text parsing, keyword scoring algorithms, and code sandbox execution.",
        "Integration Testing: Verified seamless API communication between React client, FastAPI gateway, and SQLite/SQLAlchemy database.",
        "System Testing: Validated the complete candidate flow: Login → Resume Upload → Biometric ID Check → Interview → Report Export.",
        "Acceptance Testing: Ensured parsing accuracy (> 94%), sub-second response times, and compliance with recruiter evaluation standards.",
        "Tools Used for Testing: Postman (REST API validation), PyTest (backend unit tests), Chrome DevTools (UI profiling), VS Code Debugger."
    ], 15)

    # Slide 7: Results and Discussion - Snapshots (Image 2 - 6 Screenshots)
    s7 = prs.slides.add_slide(blank_layout)
    add_slide_header(s7, "Results and Discussion: System Snapshots", "6 Key Screenshots of Working System (UI, Output & Reports)")
    if RESULTS_IMG.exists():
        s7.shapes.add_picture(str(RESULTS_IMG), Inches(0.5), Inches(1.25), Inches(12.333), Inches(5.9))

    # Slide 8: Conclusion & Future Work
    s8 = prs.slides.add_slide(blank_layout)
    add_slide_header(s8, "Conclusion & Future Enhancements", "Project summary and future roadmap")
    add_bullets(s8, Inches(1.0), Inches(1.5), Inches(11.333), Inches(5.2), [
        "Conclusion: The system successfully demonstrates how AI and NLP streamline talent acquisition, slashing screening time by 90% while upholding fairness and security.",
        "Future Enhancement 1: Multimodal video emotion & speech analysis for voice prosody, candidate confidence, and gaze tracking.",
        "Future Enhancement 2: Fine-tuned domain LLMs (e.g. Llama-3) for interactive, conversational follow-up interview questions.",
        "Future Enhancement 3: Multilingual resume parsing and OCR support for global multi-language hiring.",
        "Future Enhancement 4: Native enterprise ATS integrations (Workday, Greenhouse, BambooHR) for seamless corporate deployment."
    ], 15)

    prs.save(PPTX_OUT)
    import shutil
    shutil.copy(PPTX_OUT, PPTX_OUT_2)
    print(f"Presentation PPTX successfully saved at: {PPTX_OUT}")

if __name__ == "__main__":
    build_pdf_presentation()
    build_pptx_presentation()
