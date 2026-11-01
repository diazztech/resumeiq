"""
report_generator.py
-------------------
Generates clean, branded, multi-page PDF reports using ReportLab.

Includes candidate info, Skill Coverage Score, mandatory honesty disclaimer,
matched and missing skills tables with automatic text wrapping, category
breakdown, prioritized improvement suggestions, and page numbering.
"""

import os
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    HRFlowable,
    KeepTogether
)
from reportlab.pdfgen import canvas

# Ensure reports directory exists
REPORTS_DIR = Path(__file__).resolve().parent.parent / "reports"
REPORTS_DIR.mkdir(parents=True, exist_ok=True)


class NumberedCanvas(canvas.Canvas):
    """
    Two-pass canvas to dynamically compute and print 'Page X of Y'
    along with running header and footer on all pages.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_header_footer(num_pages)
            super().showPage()
        super().save()

    def draw_header_footer(self, total_pages: int):
        self.saveState()
        self.setFont("Helvetica", 9)
        self.setFillColor(colors.HexColor("#64748B"))

        # Running header (on pages 2 and later)
        if self._pageNumber > 1:
            self.drawString(54, 11 * inch - 36, "ResumeIQ Analysis Report")
            self.drawRightString(8.5 * inch - 54, 11 * inch - 36, "Confidential Candidate Audit")
            self.setStrokeColor(colors.HexColor("#E2E8F0"))
            self.setLineWidth(0.5)
            self.line(54, 11 * inch - 42, 8.5 * inch - 54, 11 * inch - 42)

        # Running footer (all pages)
        footer_y = 36
        self.setStrokeColor(colors.HexColor("#E2E8F0"))
        self.setLineWidth(0.5)
        self.line(54, footer_y + 12, 8.5 * inch - 54, footer_y + 12)

        footer_text = "ResumeIQ – Rule-Based Skill Coverage & Resume Matching System"
        page_str = f"Page {self._pageNumber} of {total_pages}"

        self.drawString(54, footer_y, footer_text)
        self.drawRightString(8.5 * inch - 54, footer_y, page_str)
        self.restoreState()


def generate_pdf_report(
    candidate_name: str,
    resume_filename: str,
    match_result: Dict[str, Any],
    suggestions: List[Dict[str, str]],
    output_filename: str = None
) -> str:
    """
    Builds a professional, beautifully styled PDF analysis report.

    Args:
        candidate_name: Candidate's name.
        resume_filename: Original file name of uploaded resume.
        match_result: Result dict from skill_matcher.compare_skills.
        suggestions: List of recommendation dicts from suggestions.py.
        output_filename: Optional custom target path/filename.

    Returns:
        Absolute filepath to the generated PDF report.
    """
    if not output_filename:
        timestamp_slug = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_name = "".join(c for c in candidate_name if c.isalnum() or c in ("-", "_")).strip() or "Candidate"
        output_filename = str(REPORTS_DIR / f"ResumeIQ_{safe_name}_{timestamp_slug}.pdf")

    # Target PDF document setup
    doc = SimpleDocTemplate(
        output_filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Custom typography styles
    title_style = ParagraphStyle(
        "DocTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=24,
        leading=28,
        textColor=colors.HexColor("#1E3A8A")
    )

    subtitle_style = ParagraphStyle(
        "DocSubtitle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#64748B")
    )

    h2_style = ParagraphStyle(
        "Heading2Custom",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=13,
        leading=17,
        textColor=colors.HexColor("#0F172A"),
        spaceBefore=10,
        spaceAfter=6
    )

    body_style = ParagraphStyle(
        "BodyCustom",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9.5,
        leading=14,
        textColor=colors.HexColor("#334155")
    )

    table_header_style = ParagraphStyle(
        "TableHeader",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=9,
        leading=12,
        textColor=colors.white
    )

    table_cell_style = ParagraphStyle(
        "TableCell",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor("#1E293B")
    )

    disclaimer_style = ParagraphStyle(
        "DisclaimerText",
        parent=styles["Normal"],
        fontName="Helvetica-Oblique",
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor("#6B7280")
    )

    story = []

    # 1. Header Banner
    story.append(Paragraph("ResumeIQ Analysis Report", title_style))
    story.append(Paragraph("Intelligent Rule-Based Resume & Job Description Keyword Matcher", subtitle_style))
    story.append(Spacer(1, 12))

    # 2. Candidate & Job Metadata Card
    cur_date = datetime.now().strftime("%B %d, %Y - %I:%M %p")
    meta_data = [
        [
            Paragraph(f"<b>Candidate:</b> {candidate_name}", body_style),
            Paragraph(f"<b>Audit Date:</b> {cur_date}", body_style)
        ],
        [
            Paragraph(f"<b>Resume File:</b> {resume_filename}", body_style),
            Paragraph(f"<b>Evaluation Engine:</b> Deterministic Keyword Matcher v1.0", body_style)
        ]
    ]
    meta_table = Table(meta_data, colWidths=[250, 254])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#F8FAFC")),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#E2E8F0")),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#F1F5F9")),
        ('PADDING', (0, 0), (-1, -1), 6),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 14))

    # 3. Overall Skill Coverage Score Visual Box
    score = match_result.get("match_score", 0)
    matched_count = len(match_result.get("matched", []))
    missing_count = len(match_result.get("missing", []))
    total_job_skills = match_result.get("total_job_skills", 0)

    # Determine theme color based on score
    if score >= 70:
        score_color = colors.HexColor("#059669")
        badge_bg = colors.HexColor("#ECFDF5")
        verdict = "Strong Skill Alignment: Your resume reflects most required competencies."
    elif score >= 40:
        score_color = colors.HexColor("#D97706")
        badge_bg = colors.HexColor("#FFFBEB")
        verdict = "Moderate Alignment: Notable core skills present, but key gaps exist."
    else:
        score_color = colors.HexColor("#DC2626")
        badge_bg = colors.HexColor("#FEF2F2")
        verdict = "Low Alignment: Substantial skill gaps identified against this posting."

    score_card_style = ParagraphStyle(
        "ScoreNumber",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=28,
        leading=32,
        alignment=1,  # Center
        textColor=score_color
    )

    score_label_style = ParagraphStyle(
        "ScoreLabel",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=12,
        leading=16,
        alignment=1,
        textColor=colors.HexColor("#1F2937")
    )

    verdict_style = ParagraphStyle(
        "VerdictText",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9.5,
        leading=13,
        alignment=1,
        textColor=colors.HexColor("#374151")
    )

    score_content = [
        [Paragraph(f"{score}%", score_card_style)],
        [Paragraph("Skill Coverage Score", score_label_style)],
        [Paragraph(verdict, verdict_style)],
        [Spacer(1, 4)],
        [Paragraph(
            "<b>HONESTY NOTE:</b> This percentage shows how many of the job's required skills "
            "were found in your resume using keyword matching. It is not a real ATS score or a hiring prediction.",
            disclaimer_style
        )]
    ]
    score_table = Table(score_content, colWidths=[504])
    score_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), badge_bg),
        ('BOX', (0, 0), (-1, -1), 1.5, score_color),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('PADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(score_table)
    story.append(Spacer(1, 14))

    # 4. Summary Key Metrics Table
    summary_data = [
        [
            Paragraph("<b>Total Job Skills</b>", table_header_style),
            Paragraph("<b>Matched Skills</b>", table_header_style),
            Paragraph("<b>Missing Skills</b>", table_header_style),
            Paragraph("<b>Extra Resume Skills</b>", table_header_style),
        ],
        [
            Paragraph(f"<font size=14><b>{total_job_skills}</b></font>", table_cell_style),
            Paragraph(f"<font size=14 color='#059669'><b>{matched_count}</b></font>", table_cell_style),
            Paragraph(f"<font size=14 color='#DC2626'><b>{missing_count}</b></font>", table_cell_style),
            Paragraph(f"<font size=14 color='#4F46E5'><b>{len(match_result.get('extra', []))}</b></font>", table_cell_style),
        ]
    ]
    summary_table = Table(summary_data, colWidths=[126, 126, 126, 126])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1E3A8A")),
        ('BACKGROUND', (0, 1), (-1, 1), colors.HexColor("#F8FAFC")),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#CBD5E1")),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('PADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(summary_table)
    story.append(Spacer(1, 16))

    # 5. Matched Skills Section
    story.append(Paragraph("Matched Skills (Found in Both Resume and Job)", h2_style))
    matched_skills = match_result.get("matched", [])
    if matched_skills:
        # Build 3-column table of badges/pills
        matched_rows = []
        row_temp = []
        for s in matched_skills:
            row_temp.append(Paragraph(f"<b>✓ {s}</b>", table_cell_style))
            if len(row_temp) == 3:
                matched_rows.append(row_temp)
                row_temp = []
        if row_temp:
            while len(row_temp) < 3:
                row_temp.append(Paragraph("", table_cell_style))
            matched_rows.append(row_temp)

        matched_tbl = Table(matched_rows, colWidths=[168, 168, 168])
        matched_tbl.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#F0FDF4")),
            ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#BBF7D0")),
            ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#DCFCE7")),
            ('PADDING', (0, 0), (-1, -1), 5),
        ]))
        story.append(matched_tbl)
    else:
        story.append(Paragraph("<i>No overlapping skills were detected between your resume and the job description.</i>", body_style))
    story.append(Spacer(1, 14))

    # 6. Missing Skills Section
    story.append(Paragraph("Missing Skills (Required by Job, Missing in Resume)", h2_style))
    missing_skills = match_result.get("missing", [])
    if missing_skills:
        missing_rows = []
        row_temp = []
        for s in missing_skills:
            row_temp.append(Paragraph(f"<b>✗ {s}</b>", table_cell_style))
            if len(row_temp) == 3:
                missing_rows.append(row_temp)
                row_temp = []
        if row_temp:
            while len(row_temp) < 3:
                row_temp.append(Paragraph("", table_cell_style))
            missing_rows.append(row_temp)

        missing_tbl = Table(missing_rows, colWidths=[168, 168, 168])
        missing_tbl.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#FEF2F2")),
            ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#FECACA")),
            ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#FEE2E2")),
            ('PADDING', (0, 0), (-1, -1), 5),
        ]))
        story.append(missing_tbl)
    else:
        story.append(Paragraph("<i>Outstanding! 100% of the job description's recognized skills are in your resume.</i>", body_style))
    story.append(Spacer(1, 16))

    # 7. Category Breakdown Table
    cat_breakdown = match_result.get("category_breakdown", {})
    if cat_breakdown:
        story.append(Paragraph("Skill Category Breakdown", h2_style))
        cat_rows = [
            [
                Paragraph("<b>Category</b>", table_header_style),
                Paragraph("<b>Required</b>", table_header_style),
                Paragraph("<b>Matched</b>", table_header_style),
                Paragraph("<b>Coverage</b>", table_header_style),
            ]
        ]
        for cat_name, cdata in cat_breakdown.items():
            job_cnt = cdata.get("job_count", 0)
            mat_cnt = cdata.get("match_count", 0)
            cov_pct = cdata.get("coverage_pct", 0)
            cov_color = "#059669" if cov_pct >= 70 else ("#D97706" if cov_pct >= 40 else "#DC2626")

            cat_rows.append([
                Paragraph(f"<b>{cat_name}</b>", table_cell_style),
                Paragraph(str(job_cnt), table_cell_style),
                Paragraph(str(mat_cnt), table_cell_style),
                Paragraph(f"<font color='{cov_color}'><b>{cov_pct}%</b></font>", table_cell_style)
            ])

        cat_tbl = Table(cat_rows, colWidths=[204, 100, 100, 100])
        cat_tbl.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#334155")),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor("#FFFFFF")),
            ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#CBD5E1")),
            ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
            ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
            ('PADDING', (0, 0), (-1, -1), 5),
        ]))
        story.append(cat_tbl)
        story.append(Spacer(1, 16))

    # 8. Improvement Suggestions Section
    if suggestions:
        story.append(Paragraph("Actionable Improvement Recommendations", h2_style))
        for sug in suggestions:
            prio = sug.get("priority", "Medium")
            prio_color = "#DC2626" if prio == "High" else ("#D97706" if prio == "Medium" else "#2563EB")
            title = sug.get("title", "")
            desc = sug.get("description", "")

            sug_cell = [
                [Paragraph(f"<font color='{prio_color}'><b>[{prio.upper()} PRIORITY]</b></font> <b>{title}</b>", body_style)],
                [Paragraph(desc, table_cell_style)]
            ]
            sug_table = Table(sug_cell, colWidths=[504])
            sug_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#F8FAFC")),
                ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
                ('PADDING', (0, 0), (-1, -1), 5),
            ]))
            story.append(sug_table)
            story.append(Spacer(1, 6))

    # Build the PDF using our custom dynamic NumberedCanvas
    doc.build(story, canvasmaker=NumberedCanvas)
    return output_filename
