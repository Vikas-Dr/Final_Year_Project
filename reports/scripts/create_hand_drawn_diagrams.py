#!/usr/bin/env python3
"""Create simple college-report style diagrams with Pillow (no AI image gen)."""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).resolve().parents[1] / "hand_drawn_diagrams"
GEN = Path(__file__).resolve().parents[1] / "generated_images"
OUT.mkdir(parents=True, exist_ok=True)
GEN.mkdir(parents=True, exist_ok=True)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_BLUE = (20, 50, 110)
BLUE = (40, 90, 160)
FILL = (230, 240, 255)
LIGHT_GRAY = (245, 245, 245)
RED_SOFT = (255, 235, 235)
GREEN_SOFT = (230, 245, 230)
BORDER_RED = (140, 40, 40)
BORDER_GREEN = (30, 100, 50)

FONT = "/System/Library/Fonts/Supplemental/Arial.ttf"
FONT_BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
HANDWRITTEN_FONTS = [
    "/System/Library/Fonts/MarkerFelt.ttc",
    "/System/Library/Fonts/Noteworthy.ttc",
    "/System/Library/Fonts/Supplemental/Arial.ttf",
]


def font(size, bold=False, handwritten=False):
    if handwritten:
        for path in HANDWRITTEN_FONTS:
            try:
                return ImageFont.truetype(path, size)
            except OSError:
                continue
    path = FONT_BOLD if bold else FONT
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()


def new_canvas(w, h):
    img = Image.new("RGB", (w, h), WHITE)
    return img, ImageDraw.Draw(img)


def text_size(draw, text, fnt):
    bbox = draw.textbbox((0, 0), text, font=fnt)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]


def center_text(draw, x, y, w, h, text, fnt, fill=BLACK):
    tw, th = text_size(draw, text, fnt)
    draw.text((x + (w - tw) / 2, y + (h - th) / 2), text, font=fnt, fill=fill)


def multiline_center(draw, x, y, w, h, lines, fnt, fill=BLACK, gap=4):
    sizes = [text_size(draw, line, fnt) for line in lines]
    total_h = sum(s[1] for s in sizes) + gap * (len(lines) - 1)
    cy = y + (h - total_h) / 2
    for line, (tw, th) in zip(lines, sizes):
        draw.text((x + (w - tw) / 2, cy), line, font=fnt, fill=fill)
        cy += th + gap


def rect(draw, box, fill=FILL, outline=DARK_BLUE, width=2):
    draw.rectangle(box, fill=fill, outline=outline, width=width)


def rounded_rect(draw, box, radius=8, fill=FILL, outline=DARK_BLUE, width=2):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def oval(draw, box, fill=FILL, outline=DARK_BLUE, width=2):
    draw.ellipse(box, fill=fill, outline=outline, width=width)


def arrow_down(draw, x, y1, y2, color=BLACK, width=2):
    draw.line((x, y1, x, y2 - 8), fill=color, width=width)
    draw.polygon([(x, y2), (x - 6, y2 - 10), (x + 6, y2 - 10)], fill=color)


def arrow_right(draw, x1, y, x2, color=BLACK, width=2):
    draw.line((x1, y, x2 - 8, y), fill=color, width=width)
    draw.polygon([(x2, y), (x2 - 10, y - 6), (x2 - 10, y + 6)], fill=color)


def arrow_left(draw, x1, y, x2, color=BLACK, width=2):
    # from x1 to x2 (x2 < x1)
    draw.line((x1, y, x2 + 8, y), fill=color, width=width)
    draw.polygon([(x2, y), (x2 + 10, y - 6), (x2 + 10, y + 6)], fill=color)


def title(draw, w, text, y=18, handwritten=False):
    f = font(22, bold=True, handwritten=handwritten)
    tw, _ = text_size(draw, text, f)
    draw.text(((w - tw) / 2, y), text, font=f, fill=BLACK)


def save(img, name):
    path = OUT / name
    img.save(path, "PNG")
    # also replace generated_images with same student-style diagrams
    img.save(GEN / name, "PNG")
    print(f"saved {path}")


# ---------- Diagrams ----------

def system_architecture_clean():
    W, H = 1100, 760
    img = Image.new("RGB", (W, H), (248, 243, 235))
    d = ImageDraw.Draw(img)

    for y in range(0, H, 22):
        d.line((0, y, W, y), fill=(223, 211, 198), width=1)

    title(d, W, "System Architecture", y=26, handwritten=True)

    paper = (248, 243, 235)
    stroke = (86, 63, 54)
    blue = (96, 121, 148)
    green = (110, 148, 116)
    amber = (176, 129, 82)
    rose = (173, 126, 133)

    def hand_box(x1, y1, x2, y2, fill, title_text, lines):
        rounded_rect(d, (x1, y1, x2, y2), radius=18, fill=fill, outline=stroke, width=2)
        d.line((x1 + 18, y1 + 36, x2 - 18, y1 + 36), fill=stroke, width=1)
        center_text(d, x1, y1 + 8, x2 - x1, 28, title_text, font(20, handwritten=True), stroke)
        multiline_center(d, x1 + 18, y1 + 44, x2 - x1 - 36, y2 - y1 - 54, lines, font(14, handwritten=True), stroke, gap=5)

    hand_box(100, 90, 1000, 176, (235, 244, 245), "Presentation Layer",
             ["React.js SPA", "Candidate UI / Recruiter UI"])

    hand_box(100, 210, 1000, 298, (228, 239, 234), "API Layer",
             ["FastAPI REST", "JWT Auth / CORS / Routes"])

    hand_box(100, 338, 520, 490, (232, 240, 216), "Business Logic",
             ["Resume parser", "Identity verification", "Interview engine", "Scoring & report logic"])

    hand_box(580, 338, 1000, 490, (243, 232, 218), "AI Engine",
             ["Rule-based NLP", "Skill extraction", "Optional Ollama LLM"])

    hand_box(100, 540, 1000, 660, (239, 230, 215), "Data Layer",
             ["SQLite / MySQL", "MongoDB (optional)", "Local document storage"])

    arrow_down(d, 550, 176, 210)
    arrow_down(d, 310, 298, 338)
    arrow_down(d, 790, 298, 338)
    arrow_down(d, 550, 490, 540)

    left_label = "Candidate / Recruiter"
    d.text((105, 690), left_label, font=font(15, handwritten=True), fill=blue)
    d.text((430, 690), "Browser", font=font(15, handwritten=True), fill=amber)
    d.text((640, 690), "Presentation", font=font(15, handwritten=True), fill=green)

    d.text((100, 714), "Users interact through the interface, which calls the API and submits data to the AI and storage layers.",
           font=font(13, handwritten=True), fill=(82, 74, 68))

    save(img, "architecture_diagram.png")


def candidate_workflow():
    W, H = 1300, 420
    img, d = new_canvas(W, H)
    title(d, W, "Figure: Candidate Workflow")

    steps = [
        "Login",
        "Upload\nResume",
        "Identity\nVerification",
        "Take\nInterview",
        "Get Score\n& Report",
    ]
    box_w, box_h = 160, 90
    start_x, y = 60, 160
    gap = 70
    centers = []
    for i, label in enumerate(steps):
        x = start_x + i * (box_w + gap)
        rounded_rect(d, (x, y, x + box_w, y + box_h), radius=6)
        lines = label.split("\n")
        multiline_center(d, x, y, box_w, box_h, lines, font(16, True))
        centers.append(x + box_w // 2)
        if i < len(steps) - 1:
            arrow_right(d, x + box_w, y + box_h // 2, x + box_w + gap)

    # Start/End markers
    d.ellipse((30, y + 30, 55, y + 55), fill=BLACK)
    arrow_right(d, 55, y + 42, start_x)

    end_x = start_x + 4 * (box_w + gap) + box_w
    d.ellipse((end_x + 20, y + 28, end_x + 48, y + 56), outline=BLACK, width=3)
    d.ellipse((end_x + 26, y + 34, end_x + 42, y + 50), fill=BLACK)
    arrow_right(d, end_x, y + 42, end_x + 20)

    d.text((60, 290), "Flow: Candidate logs in → uploads resume → verifies ID + selfie → attends interview → receives score/report", font=font(14), fill=DARK_BLUE)
    save(img, "candidate_workflow.png")


def existing_vs_proposed():
    W, H = 1200, 720
    img, d = new_canvas(W, H)
    title(d, W, "Figure: Existing System vs Proposed System")

    # Existing column
    rect(d, (60, 70, 560, 120), fill=RED_SOFT, outline=BORDER_RED)
    center_text(d, 60, 70, 500, 50, "Existing System (Manual)", font(20, True), BORDER_RED)

    existing = [
        "Manual resume screening",
        "Human-dependent interview scoring",
        "Weak / missing identity checks",
        "Slow for large applicant volume",
        "Inconsistent reports",
    ]
    y = 150
    for item in existing:
        rect(d, (80, y, 540, y + 70), fill=WHITE, outline=BORDER_RED)
        center_text(d, 80, y, 460, 70, item, font(16))
        y += 90

    # Proposed column
    rect(d, (640, 70, 1140, 120), fill=GREEN_SOFT, outline=BORDER_GREEN)
    center_text(d, 640, 70, 500, 50, "Proposed System (AI-Powered)", font(20, True), BORDER_GREEN)

    proposed = [
        "Automatic resume parsing & match score",
        "Structured MCQ / theory / coding scoring",
        "ID upload + face matching verification",
        "Faster screening and evaluation",
        "Dashboard + PDF report generation",
    ]
    y = 150
    for item in proposed:
        rect(d, (660, y, 1120, y + 70), fill=WHITE, outline=BORDER_GREEN)
        center_text(d, 660, y, 460, 70, item, font(16))
        y += 90

    # Arrow in middle
    arrow_right(d, 560, 400, 640)
    d.text((555, 410), "Improve", font=font(12, True), fill=BLACK)
    save(img, "existing_vs_proposed.png")


def scoring_model():
    W, H = 1200, 700
    img, d = new_canvas(W, H)
    title(d, W, "Figure: Scoring Model")

    # Inputs
    inputs = [
        (80, 120, "Resume\nMatch Score"),
        (80, 280, "Interview\nMCQ Score"),
        (80, 440, "Theory &\nCoding Score"),
    ]
    for x, y, label in inputs:
        oval(d, (x, y, x + 180, y + 100))
        multiline_center(d, x, y, 180, 100, label.split("\n"), font(15, True))
        arrow_right(d, x + 180, y + 50, 360)

    # Process box
    rect(d, (360, 200, 720, 420))
    multiline_center(d, 360, 200, 360, 220, [
        "Weighted Scoring Engine",
        "",
        "Resume  :  30%",
        "MCQ     :  25%",
        "Theory  :  25%",
        "Coding  :  20%",
    ], font(16, True))

    arrow_right(d, 720, 310, 820)

    # Output
    rect(d, (820, 180, 1120, 300), fill=GREEN_SOFT, outline=BORDER_GREEN)
    multiline_center(d, 820, 180, 300, 120, ["Final Score", "(0 - 100)"], font(18, True), BORDER_GREEN)

    rect(d, (820, 340, 1120, 460), fill=FILL, outline=DARK_BLUE)
    multiline_center(d, 820, 340, 300, 120, ["Recommendation", "Shortlist / Review / Reject"], font(16, True))

    arrow_down(d, 970, 300, 340)

    d.text((80, 600), "Note: Weights can be adjusted per job role. Recruiter views final score on dashboard.", font=font(14), fill=DARK_BLUE)
    save(img, "scoring_model.png")


def tech_stack():
    W, H = 1100, 640
    img, d = new_canvas(W, H)
    title(d, W, "Figure: Technology Stack")

    boxes = [
        (80, 90, 340, 220, "Frontend", ["React.js", "HTML / CSS", "Fetch API"]),
        (400, 90, 660, 220, "Backend", ["Python", "FastAPI", "JWT Auth"]),
        (720, 90, 1020, 220, "Database", ["SQLite", "SQLAlchemy", "Optional MySQL"]),
        (80, 300, 340, 430, "AI / NLP", ["Rule-based NLP", "Keyword match", "Optional Ollama"]),
        (400, 300, 660, 430, "File Handling", ["PDF parsing", "DOCX parsing", "Image upload"]),
        (720, 300, 1020, 430, "Tools", ["VS Code", "Git", "Postman"]),
    ]
    for x1, y1, x2, y2, head, lines in boxes:
        rect(d, (x1, y1, x2, y2))
        # header bar
        d.rectangle((x1, y1, x2, y1 + 36), fill=DARK_BLUE)
        center_text(d, x1, y1, x2 - x1, 36, head, font(16, True), WHITE)
        multiline_center(d, x1, y1 + 36, x2 - x1, y2 - y1 - 36, lines, font(15))

    d.text((80, 480), "Architecture style: Modular client-server web application", font=font(15, True), fill=DARK_BLUE)
    d.text((80, 520), "Deployment target: Local / college lab server (extendable to cloud)", font=font(14), fill=BLACK)
    save(img, "tech_stack.png")


def system_modules():
    W, H = 1200, 680
    img, d = new_canvas(W, H)
    title(d, W, "Figure: System Modules")

    # Center system
    rect(d, (420, 280, 780, 400))
    multiline_center(d, 420, 280, 360, 120, ["AI Interview &\nResume Analysis\nSystem"], font(17, True))

    modules = [
        (80, 80, "User Module", "Login / Roles"),
        (480, 80, "Resume Module", "Parse & Match"),
        (880, 80, "Verification", "ID + Selfie"),
        (80, 480, "Interview Module", "MCQ/Theory/Code"),
        (480, 480, "Scoring Module", "Weighted Score"),
        (880, 480, "Reporting Module", "PDF / Dashboard"),
    ]
    for x, y, h1, h2 in modules:
        oval(d, (x, y, x + 220, y + 100))
        multiline_center(d, x, y, 220, 100, [h1, h2], font(14, True))
        # connector to center
        cx, cy = x + 110, y + 50
        sx, sy = 600, 340
        d.line((cx, cy, sx, sy), fill=BLACK, width=2)

    save(img, "system_modules.png")


def use_case_diagram():
    W, H = 1000, 1100
    img, d = new_canvas(W, H)
    title(d, W, "Figure: Use Case Diagram")

    # system boundary
    rect(d, (220, 80, 780, 980), fill=WHITE, outline=BLACK, width=2)
    center_text(d, 220, 90, 560, 30, "AI Interview Evaluation System", font(16, True))

    use_cases = [
        "Login",
        "Upload Resume",
        "Verify Identity",
        "Take Interview",
        "View Score",
        "View Dashboard",
        "Generate Report",
        "Manage Candidates",
    ]
    y = 140
    for uc in use_cases:
        oval(d, (340, y, 660, y + 70), fill=WHITE, outline=BLACK)
        center_text(d, 340, y, 320, 70, uc, font(14, True))
        y += 95

    # Actors
    def stick(x, y, label):
        d.ellipse((x - 12, y, x + 12, y + 24), outline=BLACK, width=2)
        d.line((x, y + 24, x, y + 60), fill=BLACK, width=2)
        d.line((x - 20, y + 40, x + 20, y + 40), fill=BLACK, width=2)
        d.line((x, y + 60, x - 15, y + 90), fill=BLACK, width=2)
        d.line((x, y + 60, x + 15, y + 90), fill=BLACK, width=2)
        tw, _ = text_size(d, label, font(14, True))
        d.text((x - tw / 2, y + 100), label, font=font(14, True), fill=BLACK)

    stick(90, 300, "Candidate")
    stick(910, 450, "Recruiter")

    # associations candidate
    for yy in [175, 270, 365, 460, 555]:
        d.line((110, 380, 340, yy), fill=BLACK, width=1)
    # recruiter
    for yy in [555, 650, 745, 840]:
        d.line((890, 520, 660, yy), fill=BLACK, width=1)

    save(img, "use_case_diagram.png")


def data_flow_diagram():
    W, H = 1100, 700
    img = Image.new("RGB", (W, H), (248, 243, 235))
    d = ImageDraw.Draw(img)

    for y in range(0, H, 22):
        d.line((0, y, W, y), fill=(223, 211, 198), width=1)

    title(d, W, "Figure: Data Flow Diagram (Level 0)", handwritten=True)

    # left/right boxes
    rounded_rect(d, (90, 260, 300, 360), radius=12, fill=(226, 236, 244), outline=(60, 80, 125), width=2)
    center_text(d, 90, 260, 210, 100, "Candidate", font(20, handwritten=True), (20, 20, 20))

    rounded_rect(d, (800, 260, 1010, 360), radius=12, fill=(226, 236, 244), outline=(60, 80, 125), width=2)
    center_text(d, 800, 260, 210, 100, "Recruiter", font(20, handwritten=True), (20, 20, 20))

    # central oval
    d.ellipse((300, 170, 800, 470), outline=(60, 80, 125), width=2, fill=(208, 224, 238))
    multiline_center(d, 300, 180, 500, 220, ["AI Interview &", "Resume Analysis", "System"], font(24, handwritten=True), (20, 20, 20), gap=6)

    # arrows between process and boxes
    arrow_right(d, 300, 310, 390)
    d.text((395, 280), "Resume / Answers", font=font(14, handwritten=True), fill=(20, 20, 20))

    arrow_left(d, 700, 350, 800)
    d.text((548, 322), "Score / Status", font=font(14, handwritten=True), fill=(20, 20, 20))

    arrow_right(d, 700, 310, 800)
    d.text((720, 280), "Reports / Ranks", font=font(14, handwritten=True), fill=(20, 20, 20))

    arrow_left(d, 800, 350, 700)
    d.text((548, 352), "Review Actions", font=font(14, handwritten=True), fill=(20, 20, 20))

    # db below
    rounded_rect(d, (410, 520, 690, 610), radius=12, fill=(235, 232, 212), outline=(60, 80, 125), width=2)
    center_text(d, 410, 520, 280, 90, "D1: Candidate DB", font(18, handwritten=True), (20, 20, 20))
    arrow_down(d, 550, 470, 520)
    d.text((520, 495), "Store / Query", font=font(14, handwritten=True), fill=(20, 20, 20))

    save(img, "data_flow_diagram.png")


def activity_diagram():
    W, H = 700, 1100
    img, d = new_canvas(W, H)
    title(d, W, "Figure: Activity Diagram")

    # start
    d.ellipse((330, 60, 370, 100), fill=BLACK)
    arrow_down(d, 350, 100, 130)

    steps = [
        (130, "Login as Candidate"),
        (220, "Upload Resume"),
        (310, "Verify Identity"),
        (400, "Generate Interview"),
        (490, "Submit Answers"),
        (580, "Calculate Scores"),
        (670, "Generate Report"),
    ]
    for y, label in steps:
        rounded_rect(d, (200, y, 500, y + 60), radius=8, fill=WHITE, outline=BLACK)
        center_text(d, 200, y, 300, 60, label, font(15, True))
        arrow_down(d, 350, y + 60, y + 90)

    # decision
    diamond_y = 760
    pts = [(350, diamond_y), (430, diamond_y + 50), (350, diamond_y + 100), (270, diamond_y + 50)]
    d.polygon(pts, outline=BLACK, fill=WHITE, width=2)
    center_text(d, 300, diamond_y + 30, 100, 40, "Pass?", font(13, True))

    # Yes / No
    arrow_down(d, 350, diamond_y + 100, 900)
    d.text((360, 880), "Yes", font=font(12), fill=BLACK)
    rounded_rect(d, (220, 900, 480, 960), radius=8, fill=WHITE, outline=BLACK)
    center_text(d, 220, 900, 260, 60, "Show Recommendation", font(14, True))
    arrow_down(d, 350, 960, 1000)

    # end
    d.ellipse((330, 1000, 370, 1040), outline=BLACK, width=3)
    d.ellipse((338, 1008, 362, 1032), fill=BLACK)

    # No branch
    d.line((270, diamond_y + 50, 120, diamond_y + 50), fill=BLACK, width=2)
    d.line((120, diamond_y + 50, 120, 340), fill=BLACK, width=2)
    arrow_right(d, 120, 340, 200)
    d.text((130, diamond_y + 20), "No / Retry", font=font(12), fill=BLACK)

    save(img, "activity_diagram.png")


def sequence_diagram():
    W, H = 1100, 720
    img, d = new_canvas(W, H)
    title(d, W, "Figure: Sequence Diagram – Interview Flow")

    actors = ["Candidate", "Frontend", "Backend API", "Database", "AI Engine"]
    xs = [100, 320, 540, 760, 960]
    for x, name in zip(xs, actors):
        rect(d, (x - 70, 70, x + 70, 120), fill=FILL, outline=BLACK)
        center_text(d, x - 70, 70, 140, 50, name, font(13, True))
        # lifeline
        for yy in range(120, 650, 12):
            d.line((x, yy, x, yy + 6), fill=(120, 120, 120), width=1)

    messages = [
        (0, 1, 160, "Login()", True),
        (1, 2, 210, "authenticate()", True),
        (2, 3, 260, "check_user()", True),
        (3, 2, 300, "status", False),
        (0, 1, 350, "upload_resume()", True),
        (1, 2, 400, "parse_resume()", True),
        (2, 4, 450, "extract_skills()", True),
        (4, 2, 490, "match_score", False),
        (0, 1, 540, "submit_answers()", True),
        (1, 2, 580, "evaluate()", True),
        (2, 1, 620, "final_report", False),
    ]
    for a, b, y, label, solid in messages:
        x1, x2 = xs[a], xs[b]
        if x2 > x1:
            if solid:
                arrow_right(d, x1, y, x2)
            else:
                # dashed
                for xx in range(x1, x2 - 10, 10):
                    d.line((xx, y, xx + 5, y), fill=BLACK, width=1)
                d.polygon([(x2, y), (x2 - 10, y - 5), (x2 - 10, y + 5)], fill=BLACK)
        else:
            if solid:
                arrow_left(d, x1, y, x2)
            else:
                for xx in range(x1, x2 + 10, -10):
                    d.line((xx, y, xx - 5, y), fill=BLACK, width=1)
                d.polygon([(x2, y), (x2 + 10, y - 5), (x2 + 10, y + 5)], fill=BLACK)
        mid = (x1 + x2) / 2
        tw, _ = text_size(d, label, font(11))
        d.text((mid - tw / 2, y - 18), label, font=font(11), fill=BLACK)

    save(img, "sequence_diagram.png")


def main():
    system_architecture_clean()
    candidate_workflow()
    existing_vs_proposed()
    scoring_model()
    tech_stack()
    system_modules()
    use_case_diagram()
    data_flow_diagram()
    activity_diagram()
    sequence_diagram()
    print("All diagrams created.")


if __name__ == "__main__":
    main()
