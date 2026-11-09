import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, fill_hex):
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)

def set_cell_margins(cell, top=140, bottom=140, left=180, right=180):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_table_borders(table, color="D3D3D3"):
    tblPr = table._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'  <w:top w:val="single" w:sz="6" w:space="0" w:color="{color}"/>'
        f'  <w:bottom w:val="single" w:sz="6" w:space="0" w:color="{color}"/>'
        f'  <w:insideH w:val="single" w:sz="4" w:space="0" w:color="{color}"/>'
        f'  <w:insideV w:val="single" w:sz="4" w:space="0" w:color="{color}"/>'
        f'  <w:left w:val="none"/>'
        f'  <w:right w:val="none"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(borders)

def build_presentation_content_docx(output_path: str):
    doc = docx.Document()

    # Portrait layout with clean 0.8 in margins
    for section in doc.sections:
        section.top_margin = Inches(0.8)
        section.bottom_margin = Inches(0.8)
        section.left_margin = Inches(0.8)
        section.right_margin = Inches(0.8)

    # Style definitions
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Calibri'
    normal_style.font.size = Pt(11)
    normal_style.font.color.rgb = RGBColor(30, 41, 59)

    # Main Header
    doc_title = doc.add_paragraph()
    r_doc_title = doc_title.add_run("Project Presentation Content: Implementation & Testing")
    r_doc_title.bold = True
    r_doc_title.font.size = Pt(18)
    r_doc_title.font.color.rgb = RGBColor(15, 23, 42)

    doc_sub = doc.add_paragraph()
    doc_sub.paragraph_format.space_after = Pt(18)
    r_sub = doc_sub.add_run("AI-Powered Interview Evaluation & Resume Analysis System | Clear, Simple 8th-Grade Language")
    r_sub.font.size = Pt(10.5)
    r_sub.font.color.rgb = RGBColor(100, 116, 139)

    # =========================================================================
    # SLIDE 1: IMPLEMENTATION - TOOLS AND TECHNOLOGIES
    # =========================================================================
    h1 = doc.add_paragraph()
    h1.paragraph_format.space_before = Pt(12)
    h1.paragraph_format.space_after = Pt(4)
    run_h1 = h1.add_run("Slide 1: Implementation — Tools and Technologies")
    run_h1.bold = True
    run_h1.font.size = Pt(14)
    run_h1.font.color.rgb = RGBColor(37, 99, 235)

    p_note1 = doc.add_paragraph()
    p_note1.paragraph_format.space_after = Pt(10)
    p_note1.add_run("(Copy this exact content onto the 'Tools and Technologies' slide)").italic = True

    # Table for Tools and Tech
    table1 = doc.add_table(rows=5, cols=3)
    table1.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(table1)

    t1_headers = ["Category", "Tools Used", "Simple Explanation (What it does)"]
    hdr1 = table1.rows[0]
    for i, h_text in enumerate(t1_headers):
        cell = hdr1.cells[i]
        cell.text = h_text
        set_cell_background(cell, "1E293B")
        set_cell_margins(cell, top=140, bottom=140, left=140, right=140)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        for r in p.runs:
            r.bold = True
            r.font.size = Pt(10)
            r.font.color.rgb = RGBColor(255, 255, 255)

    t1_data = [
        ("Programming Languages", "Python, JavaScript, HTML5, CSS3", "Python runs the brain and AI backend; JavaScript, HTML, and CSS create the website you see and click on."),
        ("Frameworks & APIs", "FastAPI, React.js, spaCy, scikit-learn", "React creates a fast user screen; FastAPI sends information back and forth; spaCy and scikit-learn read and understand text."),
        ("Databases", "SQLite / MySQL & MongoDB", "SQLite stores user accounts and logins safely; MongoDB saves candidate resumes, interview scores, and test details."),
        ("IDEs & Tools", "Visual Studio Code (VS Code), Postman, Git", "VS Code was used to write all the code; Postman helped test if the backend works; Git keeps versions of the code safe.")
    ]

    for row_idx, data in enumerate(t1_data):
        row = table1.rows[row_idx + 1]
        bg_col = "F8FAFC" if row_idx % 2 == 1 else "FFFFFF"
        for col_idx, cell_value in enumerate(data):
            cell = row.cells[col_idx]
            cell.text = cell_value
            set_cell_background(cell, bg_col)
            set_cell_margins(cell, top=100, bottom=100, left=120, right=120)
            p = cell.paragraphs[0]
            if col_idx == 0:
                p.runs[0].bold = True
                p.runs[0].font.size = Pt(9.5)
            else:
                p.runs[0].font.size = Pt(9.5)

    col_w1 = [Inches(1.8), Inches(2.2), Inches(3.0)]
    for r in table1.rows:
        for i, w in enumerate(col_w1):
            r.cells[i].width = w

    # Bullet points version for slide
    p_b1_title = doc.add_paragraph()
    p_b1_title.paragraph_format.space_before = Pt(12)
    p_b1_title.paragraph_format.space_after = Pt(4)
    run_b1_title = p_b1_title.add_run("Bullet Points Version (Easy to read directly on PPT):")
    run_b1_title.bold = True
    run_b1_title.font.size = Pt(10.5)

    bullets1 = [
        "Programming Languages: Python (for AI logic and backend), JavaScript, HTML5, and CSS3 (for interactive website design).",
        "Frameworks & APIs: FastAPI (high-speed REST API), React.js (modern front-end UI), and spaCy / scikit-learn (smart text analysis).",
        "Databases: SQLite / MySQL (stores logins and account roles) and MongoDB (stores flexible candidate profiles and evaluation data).",
        "IDEs & Simulation Tools: VS Code (code development), Postman (testing API connections), and Git/GitHub (code version tracking)."
    ]
    for b in bullets1:
        p_b = doc.add_paragraph(style='List Bullet')
        p_b.paragraph_format.space_after = Pt(3)
        p_b.add_run(b).font.size = Pt(10)

    # =========================================================================
    # SLIDE 2: IMPLEMENTATION - MODULE DESCRIPTION
    # =========================================================================
    doc.add_page_break()

    h2 = doc.add_paragraph()
    h2.paragraph_format.space_before = Pt(6)
    h2.paragraph_format.space_after = Pt(4)
    run_h2 = h2.add_run("Slide 2: Implementation — Module Description")
    run_h2.bold = True
    run_h2.font.size = Pt(14)
    run_h2.font.color.rgb = RGBColor(37, 99, 235)

    p_note2 = doc.add_paragraph()
    p_note2.paragraph_format.space_after = Pt(10)
    p_note2.add_run("Each module explains Why it exists (Purpose) and What it does (Functionality) in simple 8th-grade words:").italic = True

    modules = [
        {
            "name": "1. User & Authentication Module (User / Input Module)",
            "purpose": "Purpose: This module makes sure only authorized people can enter the system. It lets students sign in as candidates and hiring managers sign in as recruiters, giving each person the right dashboard and keeping private accounts secure.",
            "functionality": [
                "Lets users register and log in securely with email and password.",
                "Uses secure web tokens (JWT) so users do not have to re-enter passwords on every click.",
                "Directs candidates to test screens and recruiters to the management panel."
            ]
        },
        {
            "name": "2. Resume Analysis & Parsing Module (Processing Module)",
            "purpose": "Purpose: This module removes the need for humans to read hundreds of paper resumes one by one. It reads uploaded PDF or Word files in seconds and automatically checks how well the candidate matches the job.",
            "functionality": [
                "Extracts candidate name, email, phone number, and college details from PDF/DOCX files.",
                "Finds technical skills (like Python, React, SQL) and years of work experience.",
                "Calculates an instant Match Score (0% to 100%) showing how well the resume fits the job requirements."
            ]
        },
        {
            "name": "3. Biometric Identity Verification Module (Security Module)",
            "purpose": "Purpose: This module stops cheating and proxy test-takers. Before an interview begins, it verifies that the person sitting in front of the camera is the exact same person shown on their government ID card.",
            "functionality": [
                "Allows the candidate to upload a photo ID card (like a driver's license or college ID).",
                "Takes a live webcam picture of the candidate's face.",
                "Compares both photos using face-matching technology to approve or flag the candidate."
            ]
        },
        {
            "name": "4. AI Interview & Questioning Module (Core AI Module)",
            "purpose": "Purpose: This module tests the candidate automatically without waiting for an available human interviewer. It asks relevant questions and fairly grades both multiple-choice and written technical answers.",
            "functionality": [
                "Generates role-based questions (MCQs, conceptual theory, and short coding problems).",
                "Uses Natural Language Processing (NLP) to read student answers and grade technical accuracy.",
                "Calculates separate scores for technical knowledge, clarity, and communication."
            ]
        },
        {
            "name": "5. Dashboard & Report Generation Module (Output / Reporting Module)",
            "purpose": "Purpose: This module collects all scores into one easy-to-understand screen. It helps recruiters make fast, fair hiring decisions without guesswork.",
            "functionality": [
                "Displays a leaderboard that ranks candidates from highest to lowest score.",
                "Allows filtering by job role, passing score, or date.",
                "Generates and downloads a complete PDF performance report with charts and feedback."
            ]
        }
    ]

    for mod in modules:
        p_mname = doc.add_paragraph()
        p_mname.paragraph_format.space_before = Pt(8)
        p_mname.paragraph_format.space_after = Pt(2)
        r_mname = p_mname.add_run(mod["name"])
        r_mname.bold = True
        r_mname.font.size = Pt(11)
        r_mname.font.color.rgb = RGBColor(15, 23, 42)

        p_purp = doc.add_paragraph()
        p_purp.paragraph_format.space_after = Pt(3)
        p_purp.add_run(mod["purpose"]).font.size = Pt(10)

        p_f_hdr = doc.add_paragraph()
        p_f_hdr.paragraph_format.space_after = Pt(2)
        r_f_hdr = p_f_hdr.add_run("Key Functionalities:")
        r_f_hdr.bold = True
        r_f_hdr.font.size = Pt(9.5)

        for item in mod["functionality"]:
            p_f = doc.add_paragraph(style='List Bullet')
            p_f.paragraph_format.space_after = Pt(2)
            p_f.add_run(item).font.size = Pt(9.5)

    # =========================================================================
    # SLIDE 3: TESTING
    # =========================================================================
    doc.add_page_break()

    h3 = doc.add_paragraph()
    h3.paragraph_format.space_before = Pt(6)
    h3.paragraph_format.space_after = Pt(4)
    run_h3 = h3.add_run("Slide 3: Testing — Strategy and Tools")
    run_h3.bold = True
    run_h3.font.size = Pt(14)
    run_h3.font.color.rgb = RGBColor(37, 99, 235)

    p_note3 = doc.add_paragraph()
    p_note3.paragraph_format.space_after = Pt(10)
    p_note3.add_run("Testing ensures that every part of the software works reliably and handles errors gracefully:").italic = True

    # Part A: Testing Strategy
    p_strat = doc.add_paragraph()
    p_strat.paragraph_format.space_before = Pt(6)
    p_strat.paragraph_format.space_after = Pt(4)
    r_strat = p_strat.add_run("1. Testing Strategy (Four Levels of Testing):")
    r_strat.bold = True
    r_strat.font.size = Pt(11.5)
    r_strat.font.color.rgb = RGBColor(15, 23, 42)

    strategies = [
        ("Unit Testing", "Testing individual small functions by themselves. For example, testing if the resume text extractor can pull an email address correctly without needing the rest of the website."),
        ("Integration Testing", "Testing how different modules talk to each other. For example, verifying that when a candidate finishes answering questions in the frontend, the backend receives the answers, grades them with NLP, and saves the score to MongoDB."),
        ("System Testing", "Testing the entire project from start to finish as a complete package. For example, testing the whole journey: signing up -> verifying face ID -> uploading resume -> taking interview -> seeing score on recruiter leaderboard."),
        ("User Acceptance Testing (UAT)", "Testing from the point of view of real users (students and recruiters). We verified that the buttons are simple to click, screens load quickly, and reports are easy to read and understand.")
    ]

    for title, desc in strategies:
        p_s = doc.add_paragraph(style='List Bullet')
        p_s.paragraph_format.space_after = Pt(4)
        run_st = p_s.add_run(f"{title}: ")
        run_st.bold = True
        run_st.font.size = Pt(10)
        p_s.add_run(desc).font.size = Pt(10)

    # Part B: Tools Used for Testing
    p_tools_hdr = doc.add_paragraph()
    p_tools_hdr.paragraph_format.space_before = Pt(10)
    p_tools_hdr.paragraph_format.space_after = Pt(4)
    r_tools_hdr = p_tools_hdr.add_run("2. Tools Used for Testing:")
    r_tools_hdr.bold = True
    r_tools_hdr.font.size = Pt(11.5)
    r_tools_hdr.font.color.rgb = RGBColor(15, 23, 42)

    test_tools = [
        ("Postman", "Used to send test requests to backend API routes (like /api/login, /api/analyze-resume) and check if correct HTTP status codes (200 OK, 401 Unauthorized, 400 Bad Request) are returned."),
        ("Pytest / Python Unittest", "Used to run automated unit test scripts that verify AI scoring algorithms and data calculations without manual clicking."),
        ("Chrome DevTools", "Used to test website responsiveness on mobile and laptop screens, inspect console logs, and check network speed."),
        ("Manual Test Scenarios", "Executed pre-defined positive and negative test cases (such as uploading invalid file types or incorrect passwords) to confirm the system fails safely with helpful error messages.")
    ]

    for tool_name, tool_desc in test_tools:
        p_t = doc.add_paragraph(style='List Bullet')
        p_t.paragraph_format.space_after = Pt(4)
        run_tt = p_t.add_run(f"{tool_name}: ")
        run_tt.bold = True
        run_tt.font.size = Pt(10)
        p_t.add_run(tool_desc).font.size = Pt(10)

    doc.save(output_path)
    print(f"Successfully generated: {output_path}")

if __name__ == "__main__":
    out_file = "/Users/viki/Final_Year_Project/reports/AI_Interview_Implementation_and_Testing_Slides.docx"
    build_presentation_content_docx(out_file)
