from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image, Spacer
from bs4 import BeautifulSoup
import os
import markdown

# Define base directory
BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "sessions")
)

def save_report(session_id: str):
    session_dir = os.path.join(BASE_DIR, session_id)
    md_path = os.path.join(session_dir, "insight.md")
    plots_dir = os.path.join(session_dir, "plots")
    pdf_path = os.path.join(session_dir, "report.pdf")

    if not os.path.exists(md_path):
        return None

    # Read markdown
    with open(md_path, 'r', encoding='utf-8') as f:
        markdown_text = f.read()

    # ---- Styles ----
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "Title",
        parent=styles["Title"],
        fontSize=22,
        spaceAfter=20,
        textColor=colors.black
    )

    heading_style = ParagraphStyle(
        "Heading",
        parent=styles["Heading2"],
        fontSize=14,
        spaceBefore=12,
        spaceAfter=2,
        textColor=colors.darkblue
    )

    body_style = ParagraphStyle(
        "Body",
        parent=styles["BodyText"],
        fontSize=10.5,
        leading=14,
        spaceAfter=8
    )

    caption_style = ParagraphStyle(
        "Caption",
        parent=styles["Italic"],
        fontSize=9,
        alignment=1,  # center
        textColor=colors.grey
    )

    # ---- Document ----
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=A4,
        rightMargin=50,
        leftMargin=50,
        topMargin=50,
        bottomMargin=40
    )

    story = []

    # ---- Title ----
    story.append(Paragraph("Analysis Report", title_style))
    story.append(Spacer(1, 12))

    # Convert markdown → HTML
    html = markdown.markdown(markdown_text)

    # Split into blocks (very important)
    soup = BeautifulSoup(html, "html.parser")

    for element in soup.children:
        if element.name == "h1":
            story.append(Paragraph(element.text, title_style))

        elif element.name == "h2":
            story.append(Paragraph(element.text, heading_style))

        elif element.name == "ul":
            for li in element.find_all("li"):
                story.append(Paragraph(f"• {li.text}", body_style))

        elif element.name == "p":
            story.append(Paragraph(str(element), body_style))

        story.append(Spacer(1, 6))

    # ---- Plots Section ----
    if os.path.exists(plots_dir):
        story.append(Paragraph("Visualizations", heading_style))
        story.append(Spacer(1, 10))

        for i, plot in enumerate(sorted(os.listdir(plots_dir))):
            img_path = os.path.join(plots_dir, plot)

            # Scale image nicely
            img = Image(img_path)
            img.drawHeight = 3.5 * inch
            img.drawWidth = 6 * inch

            story.append(img)
            story.append(Spacer(1, 6))
            story.append(Paragraph(f"Figure {i+1}", caption_style))
            story.append(Spacer(1, 16))

    # ---- Build ----
    doc.build(story)

    return pdf_path