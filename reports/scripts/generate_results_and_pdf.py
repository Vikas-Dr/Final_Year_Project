#!/usr/bin/env python3
"""
Generate Results Section Output Image (6 screenshots with captions),
Complete Presentation PDF with all slide contents, and PPTX presentation.
"""

from pathlib import Path
import os
from PIL import Image as PILImage, ImageDraw, ImageFont, ImageFilter

ROOT = Path("/Users/viki/Final_Year_Project/reports")
IMG_DIR = ROOT / "project_images"
OUT_IMG_DIR = ROOT / "results_images"
OUT_IMG_DIR.mkdir(exist_ok=True, parents=True)

# 1. 6 Key result screenshots specification
RESULTS_ITEMS = [
    {
        "file": "home.png",
        "out_name": "result_1_home_landing.png",
        "title": "1. Portal Landing Page",
        "caption": "Candidate & Recruiter portal entry with feature overview and role navigation.",
    },
    {
        "file": "resume_analysis.png",
        "out_name": "result_2_resume_analysis.png",
        "title": "2. Resume Analysis & Skill Extraction",
        "caption": "Automated text parsing, skill detection, and job-match score calculation.",
    },
    {
        "file": "verification.png",
        "out_name": "result_3_identity_verification.png",
        "title": "3. Biometric ID Verification",
        "caption": "Candidate ID document upload and live selfie facial comparison.",
    },
    {
        "file": "interview.png",
        "out_name": "result_4_interview_evaluation.png",
        "title": "4. AI Interactive Interview",
        "caption": "Real-time technical MCQ, conceptual theory, and code evaluation interface.",
    },
    {
        "file": "recruiter_dashboard.png",
        "out_name": "result_5_recruiter_dashboard.png",
        "title": "5. Recruiter Analytics Dashboard",
        "caption": "Candidate performance rankings, analytics metrics, and leaderboard.",
    },
    {
        "file": "reports.png",
        "out_name": "result_6_evaluation_reports.png",
        "title": "6. AI Evaluation Report",
        "caption": "Multi-dimensional score breakdown, structured hiring insights, and PDF export.",
    },
]

def generate_individual_and_composite_results():
    print("Generating Individual Result Images & Composite Results Section Slide...")
    
    # Load fonts
    font_bold_title = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 46)
    font_sub = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 26)
    font_card_title = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 24)
    font_caption = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 18)
    
    # Canvas for 16:9 high-res slide (2400 x 1350)
    canvas_w, canvas_h = 2400, 1350
    slide = PILImage.new("RGB", (canvas_w, canvas_h), "#0f172a") # Elegant Dark Slate Navy
    draw = ImageDraw.Draw(slide)
    
    # Top Header Banner
    draw.rectangle([0, 0, canvas_w, 140], fill="#1e293b")
    draw.rectangle([0, 136, canvas_w, 140], fill="#3b82f6") # Blue accent line
    
    draw.text((60, 28), "Results and Discussion", font=font_bold_title, fill="#ffffff")
    draw.text((60, 88), "Key System Snapshots: Working Interface, AI Output & Evaluation Reports", font=font_sub, fill="#94a3b8")
    
    # 3 columns x 2 rows
    cols = 3
    rows = 2
    
    margin_x = 60
    margin_top = 170
    gap_x = 40
    gap_y = 35
    
    card_w = (canvas_w - (2 * margin_x) - ((cols - 1) * gap_x)) // cols  # ~733 px
    card_h = (canvas_h - margin_top - 40 - ((rows - 1) * gap_y)) // rows # ~552 px
    
    for i, item in enumerate(RESULTS_ITEMS):
        c = i % cols
        r = i // cols
        
        x = margin_x + c * (card_w + gap_x)
        y = margin_top + r * (card_h + gap_y)
        
        # Load source screenshot
        src_path = IMG_DIR / item["file"]
        if src_path.exists():
            orig_img = PILImage.open(src_path)
            
            # Save individual processed image with nice styling
            indiv_w, indiv_h = 1600, 1000
            indiv = PILImage.new("RGB", (indiv_w, indiv_h), "#ffffff")
            indiv_draw = ImageDraw.Draw(indiv)
            
            # Header on individual image
            indiv_draw.rectangle([0, 0, indiv_w, 80], fill="#1e293b")
            f_indiv_title = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 32)
            f_indiv_sub = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 22)
            indiv_draw.text((30, 24), item["title"], font=f_indiv_title, fill="#ffffff")
            
            # Fit image into indiv
            img_area_h = indiv_h - 140
            orig_aspect = orig_img.width / orig_img.height
            target_aspect = indiv_w / img_area_h
            
            if orig_aspect > target_aspect:
                scaled_w = indiv_w - 40
                scaled_h = int(scaled_w / orig_aspect)
            else:
                scaled_h = img_area_h - 20
                scaled_w = int(scaled_h * orig_aspect)
            
            resized_indiv = orig_img.resize((scaled_w, scaled_h), PILImage.Resampling.LANCZOS)
            paste_x = (indiv_w - scaled_w) // 2
            paste_y = 80 + (img_area_h - scaled_h) // 2
            indiv.paste(resized_indiv, (paste_x, paste_y))
            
            # Caption on indiv bottom
            indiv_draw.rectangle([0, indiv_h - 60, indiv_w, indiv_h], fill="#f8fafc")
            indiv_draw.line([0, indiv_h - 60, indiv_w, indiv_h - 60], fill="#e2e8f0", width=2)
            indiv_draw.text((30, indiv_h - 42), item["caption"], font=f_indiv_sub, fill="#334155")
            
            indiv.save(OUT_IMG_DIR / item["out_name"])
            
            # Prepare card for composite slide
            # Card background
            draw.rounded_rectangle([x, y, x + card_w, y + card_h], radius=14, fill="#1e293b", outline="#334155", width=2)
            
            # Card Title Header
            draw.rectangle([x, y, x + card_w, y + 48], fill="#0f172a")
            draw.text((x + 16, y + 12), item["title"], font=font_card_title, fill="#38bdf8")
            
            # Image area
            img_box_h = card_h - 110
            img_box_w = card_w - 20
            
            # Fit screenshot inside card
            orig_crop = orig_img
            # For home page (which is very tall 5116px), crop upper impactful section
            if item["file"] == "home.png":
                crop_h = int(orig_img.width * (10 / 16))
                orig_crop = orig_img.crop((0, 0, orig_img.width, min(crop_h + 300, orig_img.height)))
            
            c_aspect = orig_crop.width / orig_crop.height
            box_aspect = img_box_w / img_box_h
            
            if c_aspect > box_aspect:
                target_w = img_box_w
                target_h = int(img_box_w / c_aspect)
            else:
                target_h = img_box_h
                target_w = int(img_box_h * c_aspect)
            
            scaled_card_img = orig_crop.resize((target_w, target_h), PILImage.Resampling.LANCZOS)
            img_x = x + (card_w - target_w) // 2
            img_y = y + 54 + (img_box_h - target_h) // 2
            
            slide.paste(scaled_card_img, (img_x, img_y))
            # Border around screenshot inside card
            draw.rectangle([img_x, img_y, img_x + target_w, img_y + target_h], outline="#475569", width=1)
            
            # Caption bottom
            caption_y = y + card_h - 52
            draw.rectangle([x, caption_y, x + card_w, y + card_h], fill="#0f172a")
            draw.text((x + 14, caption_y + 14), item["caption"], font=font_caption, fill="#cbd5e1")

    # Save high-res composite slide images
    out_composite_path = ROOT / "results_section_output.png"
    out_slide_path = ROOT / "results_section_slide.png"
    slide.save(out_composite_path, quality=95)
    slide.save(out_slide_path, quality=95)
    print(f"Saved Results Section Output to: {out_composite_path}")

if __name__ == "__main__":
    generate_individual_and_composite_results()
