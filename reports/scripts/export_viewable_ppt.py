#!/usr/bin/env python3
"""Export Project_Report_PPT to HTML, Markdown, and PDF (viewable formats)."""

from __future__ import annotations

import base64
import html
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    Image,
    KeepTogether,
    ListFlowable,
    ListItem,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
)

ROOT = Path(__file__).resolve().parents[1]  # reports/
OUT_HTML = ROOT / "Project_Report_PPT.html"
OUT_MD = ROOT / "Project_Report_PPT.md"
OUT_PDF = ROOT / "Project_Report_PPT.pdf"
OUT_TXT = ROOT / "Project_Report_PPT_Content.txt"

# Slide content aligned with pptx + content txt
SLIDES: list[dict] = [
    {
        "num": 1,
        "title": "AI-Powered Interview Evaluation & Resume Analysis System",
        "kind": "title",
        "lines": [
            "Project Phase II Presentation",
            "Department of Information Science and Engineering",
            "Project Associates  •  Under the Guidance of Project Guide",
            "Program Coordinator: Dr. Vinutha H P",
            "Project Coordinators: Dr. Arun Kumar G H, Prof. Santhosh T",
        ],
    },
    {
        "num": 2,
        "title": "Contents",
        "bullets": [
            "Abstract",
            "Introduction & Problem Statement",
            "Objectives",
            "Existing vs Proposed System",
            "System Architecture",
            "System Modules",
            "Candidate Workflow",
            "Technology Stack",
            "Scoring Model",
            "Use Case / Data Flow",
            "Screenshots (Home, Login, Verification)",
            "Testing",
            "Results & Advantages",
            "Conclusion & Future Work",
            "References / Thank You",
        ],
    },
    {
        "num": 3,
        "title": "Abstract",
        "paragraphs": [
            "This project is an AI-powered recruitment support system that helps reduce recruiter workload by automating resume screening, interview assessment, and final candidate evaluation.",
            "It extracts skill, education, and experience details from resumes, compares them with job requirements, and calculates a job-match score. Identity verification uses ID upload and face matching. A structured interview includes MCQ, theory, and coding questions.",
            "The final output is a generated report that helps recruiters make faster, fairer, and more informed decisions.",
        ],
    },
    {
        "num": 4,
        "title": "Introduction",
        "bullets": [
            "Makes hiring smarter by combining resume analysis, verification, and interview evaluation",
            "Many companies still rely on manual screening — slow and sometimes biased",
            "Uses AI-based logic and structured evaluation to improve speed and reliability",
            "Supports multiple job roles and generates role-based interview questions",
            "Provides clear scores and recommendations for decision-making",
            "Suitable for companies, recruitment teams, and academic assessment systems",
        ],
    },
    {
        "num": 5,
        "title": "Problem Statement",
        "paragraphs": [
            "The recruitment process is often slow, inconsistent, and manual. Recruiters must read large numbers of resumes, compare candidate skills with job requirements, and evaluate technical ability through interviews.",
            "In many cases this makes the process inefficient and unfair. There is also a risk of fake candidates attempting to attend interviews without proper identity verification.",
            "This project addresses these issues by building an AI-powered system that automates resume analysis, candidate verification, interview evaluation, and report generation.",
        ],
    },
    {
        "num": 6,
        "title": "Objectives",
        "bullets": [
            "Design an intelligent system for candidate resume analysis",
            "Extract skills, education, and experience from resumes automatically",
            "Match candidate profiles with the required job description",
            "Verify candidate identity using ID upload and selfie comparison",
            "Generate role-based interview questions and evaluate responses",
            "Produce fair and structured candidate reports for recruiters",
            "Improve the speed, efficiency, and reliability of recruitment",
        ],
    },
    {
        "num": 7,
        "title": "Existing System vs Proposed System",
        "image": "hand_drawn_diagrams/existing_vs_proposed.png",
        "bullets": [
            "Existing: manual screening, inconsistent scoring, weak identity checks",
            "Proposed: auto parsing, structured scoring, ID+face verify, dashboard reports",
        ],
    },
    {
        "num": 8,
        "title": "System Architecture",
        "image": "hand_drawn_diagrams/architecture_diagram.png",
        "bullets": [
            "Presentation layer: React.js",
            "API layer: FastAPI",
            "Business logic + AI engine",
            "Data layer: SQLite / SQLAlchemy",
        ],
    },
    {
        "num": 9,
        "title": "System Modules",
        "image": "hand_drawn_diagrams/system_modules.png",
        "bullets": [
            "User module",
            "Resume analysis module",
            "Verification module",
            "Interview module",
            "Scoring module",
            "Reporting module",
        ],
    },
    {
        "num": 10,
        "title": "Candidate Workflow",
        "image": "hand_drawn_diagrams/candidate_workflow.png",
        "bullets": [
            "Login → Upload Resume → Identity Verification → Interview → Score & Report",
        ],
    },
    {
        "num": 11,
        "title": "Technology Stack",
        "image": "hand_drawn_diagrams/tech_stack.png",
        "bullets": [
            "Frontend: React.js",
            "Backend: FastAPI",
            "Database: SQLite / SQLAlchemy",
            "AI/NLP: rule-based (+ optional Ollama)",
            "Tools: VS Code, Git, Postman",
        ],
    },
    {
        "num": 12,
        "title": "Scoring Model",
        "image": "hand_drawn_diagrams/scoring_model.png",
        "bullets": [
            "Resume match: 30%",
            "MCQ: 25%",
            "Theory: 25%",
            "Coding: 20%",
            "Output: Final score (0–100) + recommendation",
        ],
    },
    {
        "num": 13,
        "title": "Use Case / Data Flow",
        "image": "hand_drawn_diagrams/use_case_diagram.png",
        "image2": "hand_drawn_diagrams/data_flow_diagram.png",
        "bullets": [
            "Actors: Candidate, Recruiter",
            "Core use cases: login, upload resume, verify identity, interview, report",
        ],
    },
    {
        "num": 14,
        "title": "Screenshot: Home Page",
        "image": "project_images/home.png",
        "bullets": [
            "Landing page with navigation to Identity Check and Resume Analysis",
        ],
    },
    {
        "num": 15,
        "title": "Screenshot: Candidate Login",
        "image": "project_images/candidate_login.png",
        "bullets": [
            "Role-based login for candidates (demo credentials supported)",
        ],
    },
    {
        "num": 16,
        "title": "Screenshot: Identity Verification",
        "image": "project_images/verification.png",
        "bullets": [
            "Steps: ID upload → Selfie capture → Access unlock",
        ],
    },
    {
        "num": 17,
        "title": "Testing",
        "sections": [
            {
                "heading": "Testing Strategies",
                "bullets": [
                    "Unit Testing – parsing, scoring, validation",
                    "Integration Testing – frontend, backend, DB",
                    "System Testing – full login-to-report flow",
                    "Acceptance Testing – meets project requirements",
                ],
            },
            {
                "heading": "Sample Test Cases (Pass)",
                "bullets": [
                    "TC01 Valid candidate login",
                    "TC03 Resume upload",
                    "TC05 Identity verification pass",
                    "TC07 Interview generation",
                    "TC08 Score calculation",
                    "TC09 Report PDF generation",
                ],
            },
        ],
        "note": "Tools: Manual testing, browser testing, Postman",
    },
    {
        "num": 18,
        "title": "Results & Advantages",
        "sections": [
            {
                "heading": "Results",
                "bullets": [
                    "Resume details extracted with job-match score",
                    "Identity verification blocks invalid attempts",
                    "Role-based MCQ, theory, coding evaluation works",
                    "Dashboard shows rankings and summary metrics",
                    "PDF reports generated for recruiters",
                ],
            },
            {
                "heading": "Advantages",
                "bullets": [
                    "Saves time in screening",
                    "Improves evaluation consistency",
                    "Adds identity security layer",
                    "Supports role-based assessments",
                    "Enables better candidate comparison",
                ],
            },
        ],
        "note": "Limitations: complex answer scoring and resume formatting edge cases",
    },
    {
        "num": 19,
        "title": "Conclusion & Future Enhancements",
        "paragraphs": [
            "Conclusion: The project successfully demonstrates how AI can improve recruitment by combining resume analysis, identity verification, role-based interview evaluation, and report generation into one practical system. It reduces manual effort and helps recruiters make better decisions.",
        ],
        "sections": [
            {
                "heading": "Future Enhancements",
                "bullets": [
                    "Voice / video interview analysis and stronger biometric verification",
                    "Advanced LLM-based scoring and multilingual interfaces",
                    "Cloud hosting, recruiter notifications, and mobile support",
                ],
            },
        ],
    },
    {
        "num": 20,
        "title": "Thank You…!",
        "kind": "closing",
        "lines": [
            "Questions & Discussion",
            "References (selected): Smart recruitment / resume NLP literature (2020–2024); FastAPI, React, SQLAlchemy documentation; project open-source libraries used for parsing and evaluation.",
        ],
    },
]


def file_to_data_uri(rel: str) -> str | None:
    path = ROOT / rel
    if not path.exists():
        return None
    mime = "image/png" if path.suffix.lower() == ".png" else "image/jpeg"
    data = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{data}"


def esc(s: str) -> str:
    return html.escape(s)


def render_slide_html(slide: dict) -> str:
    n = slide["num"]
    title = esc(slide["title"])
    parts: list[str] = [
        f'<section class="slide" id="slide-{n}" data-slide="{n}">',
        f'<div class="slide-inner">',
        f'<header class="slide-header"><span class="slide-num">{n} / 20</span>',
        f'<h1 class="slide-title">{title}</h1></header>',
        '<div class="slide-body">',
    ]

    if slide.get("kind") == "title":
        parts.append('<div class="title-block">')
        for line in slide.get("lines", []):
            parts.append(f'<p class="title-line">{esc(line)}</p>')
        parts.append("</div>")
    elif slide.get("kind") == "closing":
        parts.append('<div class="closing-block">')
        for line in slide.get("lines", []):
            parts.append(f'<p>{esc(line)}</p>')
        parts.append("</div>")
    else:
        for p in slide.get("paragraphs", []):
            parts.append(f'<p class="para">{esc(p)}</p>')

        for sec in slide.get("sections", []):
            parts.append(f'<h2 class="section-h">{esc(sec["heading"])}</h2>')
            parts.append("<ul>")
            for b in sec.get("bullets", []):
                parts.append(f"<li>{esc(b)}</li>")
            parts.append("</ul>")

        if slide.get("bullets") and not slide.get("sections"):
            parts.append("<ul>")
            for b in slide["bullets"]:
                parts.append(f"<li>{esc(b)}</li>")
            parts.append("</ul>")

        if slide.get("note"):
            parts.append(f'<p class="note">{esc(slide["note"])}</p>')

        imgs = []
        if slide.get("image"):
            imgs.append(slide["image"])
        if slide.get("image2"):
            imgs.append(slide["image2"])
        if imgs:
            parts.append('<div class="images">')
            for rel in imgs:
                uri = file_to_data_uri(rel) or rel
                parts.append(
                    f'<figure><img src="{uri}" alt="{esc(Path(rel).stem)}" />'
                    f'<figcaption>{esc(rel)}</figcaption></figure>'
                )
            parts.append("</div>")

    parts.extend(["</div>", "</div>", "</section>"])
    return "\n".join(parts)


def build_html() -> None:
    slides_html = "\n".join(render_slide_html(s) for s in SLIDES)
    doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>AI-Powered Interview Evaluation &amp; Resume Analysis System — Project Report PPT</title>
<style>
  :root {{
    --bg: #f4f6f8;
    --slide-bg: #ffffff;
    --ink: #1a2332;
    --muted: #5a6a7a;
    --accent: #0d6e6e;
    --accent-soft: #e6f3f3;
    --border: #d5dde5;
    --shadow: 0 8px 28px rgba(26, 35, 50, 0.08);
  }}
  * {{ box-sizing: border-box; }}
  html {{ scroll-behavior: smooth; }}
  body {{
    margin: 0;
    font-family: "Segoe UI", "Helvetica Neue", Arial, sans-serif;
    color: var(--ink);
    background: linear-gradient(160deg, #e8eef2 0%, #f7f9fb 40%, #eef4f4 100%);
    line-height: 1.45;
  }}
  .toolbar {{
    position: sticky;
    top: 0;
    z-index: 20;
    display: flex;
    gap: 0.75rem;
    align-items: center;
    justify-content: space-between;
    padding: 0.65rem 1.25rem;
    background: rgba(255,255,255,0.92);
    backdrop-filter: blur(8px);
    border-bottom: 1px solid var(--border);
  }}
  .toolbar h2 {{
    margin: 0;
    font-size: 0.95rem;
    font-weight: 600;
    color: var(--accent);
  }}
  .nav {{
    display: flex;
    gap: 0.5rem;
    align-items: center;
  }}
  .nav button, .nav a.print {{
    appearance: none;
    border: 1px solid var(--border);
    background: #fff;
    color: var(--ink);
    padding: 0.4rem 0.85rem;
    border-radius: 6px;
    cursor: pointer;
    font-size: 0.875rem;
    text-decoration: none;
  }}
  .nav button:hover, .nav a.print:hover {{
    border-color: var(--accent);
    background: var(--accent-soft);
  }}
  #slide-indicator {{
    font-size: 0.85rem;
    color: var(--muted);
    min-width: 4.5rem;
    text-align: center;
  }}
  .deck {{
    max-width: 960px;
    margin: 1.25rem auto 3rem;
    padding: 0 1rem;
    display: flex;
    flex-direction: column;
    gap: 1.25rem;
  }}
  .slide {{
    background: var(--slide-bg);
    border: 1px solid var(--border);
    border-radius: 10px;
    box-shadow: var(--shadow);
    min-height: 70vh;
    page-break-after: always;
    break-after: page;
  }}
  .slide-inner {{
    padding: 1.5rem 1.75rem 1.75rem;
    display: flex;
    flex-direction: column;
    min-height: 70vh;
  }}
  .slide-header {{
    border-bottom: 3px solid var(--accent);
    padding-bottom: 0.75rem;
    margin-bottom: 1.1rem;
  }}
  .slide-num {{
    display: block;
    font-size: 0.75rem;
    letter-spacing: 0.04em;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 0.35rem;
  }}
  .slide-title {{
    margin: 0;
    font-size: 1.55rem;
    font-weight: 700;
    color: var(--ink);
    line-height: 1.25;
  }}
  .slide-body {{
    flex: 1;
  }}
  .slide-body ul {{
    margin: 0.4rem 0 1rem;
    padding-left: 1.25rem;
  }}
  .slide-body li {{
    margin: 0.35rem 0;
  }}
  .para {{
    margin: 0 0 0.85rem;
    font-size: 1.02rem;
  }}
  .section-h {{
    margin: 0.9rem 0 0.35rem;
    font-size: 1.05rem;
    color: var(--accent);
  }}
  .note {{
    margin-top: 0.75rem;
    font-size: 0.92rem;
    color: var(--muted);
    font-style: italic;
  }}
  .title-block, .closing-block {{
    margin-top: 1.5rem;
    text-align: center;
  }}
  .title-line {{
    margin: 0.55rem 0;
    font-size: 1.05rem;
    color: var(--muted);
  }}
  .closing-block p {{
    margin: 0.75rem 0;
    font-size: 1.05rem;
  }}
  .images {{
    display: flex;
    flex-wrap: wrap;
    gap: 1rem;
    margin-top: 1rem;
    justify-content: center;
  }}
  .images figure {{
    margin: 0;
    max-width: 100%;
    text-align: center;
  }}
  .images img {{
    max-width: 100%;
    max-height: 48vh;
    width: auto;
    height: auto;
    border: 1px solid var(--border);
    border-radius: 6px;
    background: #fafbfc;
  }}
  .images figcaption {{
    font-size: 0.75rem;
    color: var(--muted);
    margin-top: 0.35rem;
  }}
  @media print {{
    .toolbar {{ display: none; }}
    body {{ background: #fff; }}
    .deck {{ max-width: none; margin: 0; padding: 0; gap: 0; }}
    .slide {{
      box-shadow: none;
      border: none;
      border-radius: 0;
      min-height: auto;
      page-break-after: always;
    }}
    .slide-inner {{ min-height: auto; padding: 0.5in; }}
    .images img {{ max-height: 5.5in; }}
  }}
</style>
</head>
<body>
  <div class="toolbar">
    <h2>Project Report Presentation</h2>
    <div class="nav">
      <button type="button" id="btn-prev" aria-label="Previous slide">← Prev</button>
      <span id="slide-indicator">1 / 20</span>
      <button type="button" id="btn-next" aria-label="Next slide">Next →</button>
      <a class="print" href="#" id="btn-print">Print / PDF</a>
    </div>
  </div>
  <main class="deck" id="deck">
{slides_html}
  </main>
<script>
(function () {{
  const slides = Array.from(document.querySelectorAll(".slide"));
  let idx = 0;
  const indicator = document.getElementById("slide-indicator");
  function go(i) {{
    idx = Math.max(0, Math.min(slides.length - 1, i));
    slides[idx].scrollIntoView({{ behavior: "smooth", block: "start" }});
    indicator.textContent = (idx + 1) + " / " + slides.length;
  }}
  document.getElementById("btn-prev").addEventListener("click", () => go(idx - 1));
  document.getElementById("btn-next").addEventListener("click", () => go(idx + 1));
  document.getElementById("btn-print").addEventListener("click", (e) => {{
    e.preventDefault();
    window.print();
  }});
  document.addEventListener("keydown", (e) => {{
    if (e.key === "ArrowRight" || e.key === "PageDown" || e.key === " ") {{
      e.preventDefault(); go(idx + 1);
    }} else if (e.key === "ArrowLeft" || e.key === "PageUp") {{
      e.preventDefault(); go(idx - 1);
    }} else if (e.key === "Home") {{ go(0); }}
      else if (e.key === "End") {{ go(slides.length - 1); }}
  }});
  const observer = new IntersectionObserver((entries) => {{
    const visible = entries
      .filter(en => en.isIntersecting)
      .sort((a, b) => b.intersectionRatio - a.intersectionRatio)[0];
    if (visible) {{
      idx = slides.indexOf(visible.target);
      indicator.textContent = (idx + 1) + " / " + slides.length;
    }}
  }}, {{ threshold: [0.4, 0.6] }});
  slides.forEach(s => observer.observe(s));
}})();
</script>
</body>
</html>
"""
    OUT_HTML.write_text(doc, encoding="utf-8")
    print(f"Wrote {OUT_HTML}")


def build_markdown() -> None:
    lines: list[str] = [
        "# AI-Powered Interview Evaluation & Resume Analysis System",
        "",
        "**Project Phase II Presentation** — Department of Information Science and Engineering",
        "",
        "> Viewable Markdown export of `Project_Report_PPT.pptx` (~20 slides). Images use relative paths so Cursor can preview them.",
        "",
        "---",
        "",
    ]
    for slide in SLIDES:
        n = slide["num"]
        lines.append(f"## Slide {n}: {slide['title']}")
        lines.append("")
        if slide.get("kind") in ("title", "closing"):
            for line in slide.get("lines", []):
                lines.append(f"*{line}*")
                lines.append("")
        for p in slide.get("paragraphs", []):
            lines.append(p)
            lines.append("")
        for sec in slide.get("sections", []):
            lines.append(f"### {sec['heading']}")
            lines.append("")
            for b in sec.get("bullets", []):
                lines.append(f"- {b}")
            lines.append("")
        if slide.get("bullets") and not slide.get("sections"):
            for b in slide["bullets"]:
                lines.append(f"- {b}")
            lines.append("")
        if slide.get("note"):
            lines.append(f"*{slide['note']}*")
            lines.append("")
        for key in ("image", "image2"):
            rel = slide.get(key)
            if rel:
                caption = Path(rel).stem.replace("_", " ").title()
                lines.append(f"![{caption}]({rel})")
                lines.append("")
                lines.append(f"`{rel}`")
                lines.append("")
        lines.append("---")
        lines.append("")
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {OUT_MD}")


def build_pdf() -> None:
    page = landscape(A4)
    doc = SimpleDocTemplate(
        str(OUT_PDF),
        pagesize=page,
        leftMargin=0.6 * inch,
        rightMargin=0.6 * inch,
        topMargin=0.45 * inch,
        bottomMargin=0.45 * inch,
    )
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "SlideTitle",
        parent=styles["Heading1"],
        fontSize=20,
        textColor=colors.HexColor("#0d6e6e"),
        spaceAfter=10,
        leading=24,
    )
    body = ParagraphStyle(
        "Body",
        parent=styles["Normal"],
        fontSize=11,
        leading=15,
        textColor=colors.HexColor("#1a2332"),
        spaceAfter=8,
    )
    section_h = ParagraphStyle(
        "SecH",
        parent=styles["Heading2"],
        fontSize=13,
        textColor=colors.HexColor("#0d6e6e"),
        spaceBefore=6,
        spaceAfter=4,
    )
    muted = ParagraphStyle(
        "Muted",
        parent=styles["Normal"],
        fontSize=10,
        textColor=colors.HexColor("#5a6a7a"),
        alignment=TA_CENTER,
        spaceAfter=6,
    )
    center = ParagraphStyle(
        "Center",
        parent=body,
        alignment=TA_CENTER,
        fontSize=12,
    )
    num_style = ParagraphStyle(
        "Num",
        parent=styles["Normal"],
        fontSize=9,
        textColor=colors.HexColor("#5a6a7a"),
        spaceAfter=4,
    )

    story: list = []
    max_w = page[0] - 1.2 * inch
    max_h = page[1] - 1.8 * inch

    for i, slide in enumerate(SLIDES):
        block: list = []
        block.append(Paragraph(f"Slide {slide['num']} / 20", num_style))
        block.append(Paragraph(esc(slide["title"]), title_style))

        if slide.get("kind") in ("title", "closing"):
            for line in slide.get("lines", []):
                block.append(Paragraph(esc(line), center if slide["kind"] == "title" else muted))
        for p in slide.get("paragraphs", []):
            block.append(Paragraph(esc(p), body))
        for sec in slide.get("sections", []):
            block.append(Paragraph(esc(sec["heading"]), section_h))
            items = [ListItem(Paragraph(esc(b), body), leftIndent=12) for b in sec.get("bullets", [])]
            if items:
                block.append(ListFlowable(items, bulletType="bullet", start="•"))
        if slide.get("bullets") and not slide.get("sections"):
            items = [ListItem(Paragraph(esc(b), body), leftIndent=12) for b in slide["bullets"]]
            block.append(ListFlowable(items, bulletType="bullet", start="•"))
        if slide.get("note"):
            block.append(Paragraph(f"<i>{esc(slide['note'])}</i>", muted))

        imgs = [slide[k] for k in ("image", "image2") if slide.get(k)]
        for rel in imgs:
            path = ROOT / rel
            if path.exists():
                img = Image(str(path))
                iw, ih = img.imageWidth, img.imageHeight
                scale = min(max_w / iw, (max_h * 0.72) / ih, 1.0)
                img.drawWidth = iw * scale
                img.drawHeight = ih * scale
                block.append(Spacer(1, 8))
                block.append(img)

        story.append(KeepTogether(block))
        if i < len(SLIDES) - 1:
            story.append(PageBreak())

    doc.build(story)
    print(f"Wrote {OUT_PDF}")


def refresh_content_txt() -> None:
    """Keep Content.txt readable and aligned with exports."""
    lines = [
        "AI-Powered Interview Evaluation & Resume Analysis System",
        "Project Report – PowerPoint Content (~20 slides)",
        "================================================",
        "",
        "Also available as viewable files:",
        "  - Project_Report_PPT.html  (open in any browser)",
        "  - Project_Report_PPT.md    (preview in Cursor)",
        "  - Project_Report_PPT.pdf   (exported slides)",
        "",
    ]
    for slide in SLIDES:
        lines.append(f"SLIDE {slide['num']} – {slide['title']}")
        lines.append("-" * max(20, len(f"SLIDE {slide['num']} – {slide['title']}")))
        if slide.get("kind") in ("title", "closing"):
            for line in slide.get("lines", []):
                lines.append(line)
        for p in slide.get("paragraphs", []):
            lines.append(p)
            lines.append("")
        for sec in slide.get("sections", []):
            lines.append(sec["heading"] + ":")
            for b in sec.get("bullets", []):
                lines.append(f"• {b}")
            lines.append("")
        if slide.get("bullets") and not slide.get("sections"):
            for b in slide["bullets"]:
                lines.append(f"• {b}")
        if slide.get("note"):
            lines.append(slide["note"])
        for key in ("image", "image2"):
            if slide.get(key):
                lines.append(f"[Image: {slide[key]}]")
        lines.append("")
    OUT_TXT.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    print(f"Wrote {OUT_TXT}")


if __name__ == "__main__":
    build_html()
    build_markdown()
    build_pdf()
    refresh_content_txt()
    print("Done.")
