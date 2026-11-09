#!/usr/bin/env python3
"""
Embed the 7 exact figures into the main project report docx file.
"""

from pathlib import Path
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

ROOT = Path("/Users/viki/Final_Year_Project/reports")
REPORT_PATH = ROOT / "AI_Interview_Final_Project_Report.docx"
OUT_IMG_DIR = ROOT / "results_images"

FIG_MAP = {
    "Figure 7.1": "Figure_7_1_Home_Page.png",
    "Figure 7.2": "Figure_7_2_Candidate_Login.png",
    "Figure 7.3": "Figure_7_3_Identity_Verification.png",
    "Figure 7.4": "Figure_7_4_Resume_Analysis.png",
    "Figure 7.5": "Figure_7_5_Interview_Page.png",
    "Figure 7.6": "Figure_7_6_Recruiter_Dashboard.png",
    "Figure 7.7": "Figure_7_7_Reports_Page.png",
}

def embed_figures():
    doc = docx.Document(str(REPORT_PATH))
    print(f"Loaded {REPORT_PATH} with {len(doc.paragraphs)} paragraphs.")
    
    # Iterate through paragraphs looking for figure captions
    for i, p in enumerate(doc.paragraphs):
        text = p.text.strip()
        for fig_key, img_file in FIG_MAP.items():
            if text.startswith(fig_key):
                img_path = OUT_IMG_DIR / img_file
                if img_path.exists():
                    print(f"Found match: '{text}' -> inserting {img_file}")
                    # Insert image before or after caption
                    # Clear run and add picture above caption
                    new_p = p.insert_paragraph_before()
                    new_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    new_p.paragraph_format.space_before = Pt(8)
                    new_p.paragraph_format.space_after = Pt(4)
                    new_p.add_run().add_picture(str(img_path), width=Inches(6.0))
                    
                    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    p.paragraph_format.space_after = Pt(14)
                    
    doc.save(str(REPORT_PATH))
    print(f"Saved updated report to: {REPORT_PATH}")

if __name__ == "__main__":
    embed_figures()
