"""
create_sample_resumes.py
------------------------
Utility script to generate sample PDF resumes for testing and demonstrations:
1. sample_resume.pdf: A realistic college graduate / junior software engineer resume.
2. scanned_or_empty_sample.pdf: A PDF with drawn shapes but zero extractable text.
3. corrupt_sample.pdf: A corrupted file disguised as a PDF.
"""

from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.pdfgen import canvas

SAMPLE_DIR = Path(__file__).resolve().parent
SAMPLE_DIR.mkdir(parents=True, exist_ok=True)


def create_realistic_resume():
    """Generates sample_resume.pdf for Aarav Sharma."""
    pdf_path = SAMPLE_DIR / "sample_resume.pdf"
    doc = SimpleDocTemplate(
        str(pdf_path),
        pagesize=letter,
        leftMargin=40,
        rightMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()

    # Custom styles
    name_style = ParagraphStyle(
        "ResumeName",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=20,
        leading=24,
        textColor=colors.HexColor("#0F172A")
    )
    contact_style = ParagraphStyle(
        "ResumeContact",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#475569")
    )
    section_title = ParagraphStyle(
        "ResumeSection",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#1E40AF"),
        spaceBefore=8,
        spaceAfter=4
    )
    item_title = ParagraphStyle(
        "ItemTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=10,
        leading=13,
        textColor=colors.HexColor("#1E293B")
    )
    body_text = ParagraphStyle(
        "ResumeBody",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#334155")
    )

    story = []

    # Header
    story.append(Paragraph("Aarav Sharma", name_style))
    story.append(Paragraph(
        "Bengaluru, India | +91 98765 43210 | aarav.sharma@example.com | "
        "github.com/aaravsharma | linkedin.com/in/aaravsharma",
        contact_style
    ))
    story.append(Spacer(1, 10))

    # Summary
    story.append(Paragraph("PROFESSIONAL SUMMARY", section_title))
    story.append(Paragraph(
        "Energetic and detail-oriented Computer Science graduate with strong foundation in "
        "Python, REST API development, SQL databases, and modern web technologies. "
        "Passionate about solving real-world challenges with clean code, scalable architecture, "
        "and collaborative teamwork.",
        body_text
    ))
    story.append(Spacer(1, 8))

    # Education
    story.append(Paragraph("EDUCATION", section_title))
    edu_data = [
        [
            Paragraph("<b>B.Tech in Computer Science & Engineering</b>", item_title),
            Paragraph("2021 – 2025", contact_style)
        ],
        [
            Paragraph("National Institute of Technology | CGPA: 8.7 / 10.0", body_text),
            Paragraph("Bengaluru, India", contact_style)
        ]
    ]
    edu_table = Table(edu_data, colWidths=[380, 150])
    edu_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
    ]))
    story.append(edu_table)
    story.append(Spacer(1, 8))

    # Technical Skills
    story.append(Paragraph("TECHNICAL SKILLS", section_title))
    skills_data = [
        [Paragraph("<b>Programming Languages:</b>", item_title), Paragraph("Python, JavaScript, SQL, C++, HTML5, CSS3", body_text)],
        [Paragraph("<b>Frameworks & Web:</b>", item_title), Paragraph("Django, FastAPI, React, REST API, Streamlit, Bootstrap", body_text)],
        [Paragraph("<b>Databases:</b>", item_title), Paragraph("PostgreSQL, SQLite, Redis, MongoDB", body_text)],
        [Paragraph("<b>Cloud & DevOps:</b>", item_title), Paragraph("Docker, Git, GitHub, Linux, Bash, CI/CD", body_text)],
        [Paragraph("<b>Soft Skills:</b>", item_title), Paragraph("Problem Solving, Teamwork & Collaboration, Communication, Time Management", body_text)]
    ]
    skills_table = Table(skills_data, colWidths=[160, 370])
    skills_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    story.append(skills_table)
    story.append(Spacer(1, 8))

    # Experience
    story.append(Paragraph("INTERNSHIP EXPERIENCE", section_title))
    story.append(Paragraph("<b>Software Engineering Intern</b> – CloudSphere Solutions", item_title))
    story.append(Paragraph("<i>June 2024 – August 2024 | Bengaluru, India</i>", contact_style))
    story.append(Paragraph("• Built and optimized 12+ REST API endpoints using Python, FastAPI, and PostgreSQL.", body_text))
    story.append(Paragraph("• Improved API query response times by 35% through indexing and Redis caching.", body_text))
    story.append(Paragraph("• Containerized microservices using Docker and integrated automated GitHub Actions CI/CD workflows.", body_text))
    story.append(Paragraph("• Collaborated with a team of 5 senior engineers in bi-weekly Agile/Scrum sprints.", body_text))
    story.append(Spacer(1, 8))

    # Projects
    story.append(Paragraph("KEY ACADEMIC PROJECTS", section_title))
    story.append(Paragraph("<b>EduPortal – Campus Learning & Exam Management System</b>", item_title))
    story.append(Paragraph("<i>Technologies: Python, Django, PostgreSQL, HTML5, Bootstrap, Git</i>", contact_style))
    story.append(Paragraph("• Developed full-stack web application serving 450+ active college students and faculty.", body_text))
    story.append(Paragraph("• Implemented secure JWT role-based authentication and automated PDF report generation.", body_text))
    story.append(Paragraph("• Reduced manual grade processing duration by 60% for academic coordinators.", body_text))
    story.append(Spacer(1, 6))

    story.append(Paragraph("<b>StockTrend – Financial Sentiment & Analytics Visualizer</b>", item_title))
    story.append(Paragraph("<i>Technologies: Python, Pandas, Matplotlib, Streamlit, REST API</i>", contact_style))
    story.append(Paragraph("• Built interactive real-time dashboard analyzing financial market trends and news tickers.", body_text))
    story.append(Paragraph("• Processed over 10,000+ financial articles to extract sentiment indicators with 84% accuracy.", body_text))
    story.append(Spacer(1, 8))

    # Achievements & Extracurriculars
    story.append(Paragraph("ACHIEVEMENTS & CERTIFICATIONS", section_title))
    story.append(Paragraph("• Winner, Smart India Internal College Hackathon (2024) among 45 participating teams.", body_text))
    story.append(Paragraph("• Certified Python Professional & PostgreSQL Developer (HackerRank, 2024).", body_text))

    doc.build(story)
    print(f"Generated realistic resume at: {pdf_path}")


def create_scanned_image_pdf():
    """Generates scanned_or_empty_sample.pdf (PDF with only visual rectangle, no text)."""
    pdf_path = SAMPLE_DIR / "scanned_or_empty_sample.pdf"
    c = canvas.Canvas(str(pdf_path), pagesize=letter)
    # Draw gray graphic shapes simulating a scanned page image
    c.setStrokeColor(colors.gray)
    c.setFillColor(colors.lightgrey)
    c.rect(50, 50, 500, 700, fill=1, stroke=1)
    c.showPage()
    c.save()
    print(f"Generated scanned/empty test PDF at: {pdf_path}")


def create_corrupt_pdf():
    """Generates corrupt_sample.pdf containing invalid non-PDF binary data."""
    pdf_path = SAMPLE_DIR / "corrupt_sample.pdf"
    with open(pdf_path, "wb") as f:
        f.write(b"%PDF-1.4\nGARBLED_CORRUPT_BYTES_NOT_A_REAL_PDF_EOF_INVALID")
    print(f"Generated corrupt test PDF at: {pdf_path}")


if __name__ == "__main__":
    create_realistic_resume()
    create_scanned_image_pdf()
    create_corrupt_pdf()
