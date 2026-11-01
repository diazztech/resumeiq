"""
pages_ui/analyze.py
-------------------
Analysis input form page for ResumeIQ.
Provides candidate name input, PDF file uploader, job description text area,
validation safeguards, 1-click sample data loader, and triggers the
real analysis engine.
"""

import io
from pathlib import Path
import streamlit as st

from modules.pdf_extractor import (
    extract_text_from_pdf,
    EmptyPDFError,
    CorruptPDFError,
    ScannedPDFError,
    PDFExtractionError
)
from modules.skill_matcher import extract_skills, compare_skills
from modules.suggestions import generate_suggestions
from modules.report_generator import generate_pdf_report
from modules.history_manager import save_analysis

SAMPLE_DATA_DIR = Path(__file__).resolve().parent.parent / "sample_data"


def render_analyze_page():
    """Renders the resume upload and job description submission form."""
    st.markdown("## 🔍 Analyze Your Resume")
    st.markdown(
        "<p style='color: #64748B; margin-bottom: 20px;'>"
        "Enter your details, upload your PDF resume, and paste the target job description to run an in-depth audit."
        "</p>",
        unsafe_allow_html=True
    )

    # Pre-populate state containers if not set
    if "form_name" not in st.session_state:
        st.session_state.form_name = ""
    if "form_job_desc" not in st.session_state:
        st.session_state.form_job_desc = ""
    if "use_sample_pdf" not in st.session_state:
        st.session_state.use_sample_pdf = False

    # Quick demo / sample data loader banner
    with st.expander("⚡ Quick Demo / Examiner Shortcut: Load Sample Data", expanded=False):
        st.markdown(
            "Want to test without preparing files? Click below to populate the form with a realistic "
            "Full-Stack Python Developer job description and pre-load Aarav Sharma's resume PDF."
        )
        if st.button("📋 Populate Form with Sample Data", key="load_sample_btn"):
            sample_jd_path = SAMPLE_DATA_DIR / "sample_job_description.txt"
            if sample_jd_path.exists():
                with open(sample_jd_path, "r", encoding="utf-8") as f:
                    st.session_state.form_job_desc = f.read()
            st.session_state.form_name = "Aarav Sharma"
            st.session_state.use_sample_pdf = True
            st.success("Sample data loaded! Review the form below and click 'Analyze Resume'.")
            st.rerun()

    # Form layout
    with st.container():
        st.markdown("<div style='background: white; border: 1px solid #E2E8F0; border-radius: 16px; padding: 28px; box-shadow: 0 4px 15px -2px rgba(0,0,0,0.04);'>", unsafe_allow_html=True)

        candidate_name = st.text_input(
            "1. Candidate Full Name *",
            value=st.session_state.form_name,
            placeholder="e.g. Aarav Sharma or Jane Doe",
            help="Your name will appear on the audit report and history log."
        )

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("##### 2. Upload Resume (PDF Only) *")

        if st.session_state.use_sample_pdf:
            st.info("ℹ️ Using bundled sample resume: `sample_data/sample_resume.pdf` (Aarav Sharma). You can also upload a different file below to override.")

        uploaded_pdf = st.file_uploader(
            "Choose a PDF resume",
            type=["pdf"],
            accept_multiple_files=False,
            help="Upload a text-based PDF (scanned image-only PDFs are not supported)."
        )

        st.markdown("<br>", unsafe_allow_html=True)
        job_description = st.text_area(
            "3. Target Job Description *",
            value=st.session_state.form_job_desc,
            height=200,
            placeholder="Paste the target job description or internship requirements here...\n(Include responsibilities, required technical skills, and tools)",
            help="ResumeIQ uses boundary-safe keyword matching against our 200+ skills taxonomy."
        )

        st.markdown("<br>", unsafe_allow_html=True)
        analyze_btn = st.button("🚀 Analyze Resume", type="primary", use_container_width=True)

        st.markdown("</div>", unsafe_allow_html=True)

    # Handle Analysis Execution
    if analyze_btn:
        # 1. Validation: Candidate Name
        clean_name = candidate_name.strip()
        if not clean_name:
            st.error("⚠️ Please enter candidate name before running the analysis.")
            return

        # 2. Validation: PDF file present
        pdf_bytes = None
        pdf_filename = ""
        if uploaded_pdf is not None:
            # Check file size limit (10 MB)
            max_bytes = 10 * 1024 * 1024
            if uploaded_pdf.size > max_bytes:
                st.error("⚠️ The uploaded PDF is too large (>10MB). Please upload a standard resume under 10MB.")
                return
            pdf_bytes = uploaded_pdf.read()
            pdf_filename = uploaded_pdf.name
        elif st.session_state.use_sample_pdf:
            sample_pdf_path = SAMPLE_DATA_DIR / "sample_resume.pdf"
            if sample_pdf_path.exists():
                with open(sample_pdf_path, "rb") as f:
                    pdf_bytes = f.read()
                pdf_filename = "sample_resume.pdf"
            else:
                st.error("⚠️ Sample resume file could not be found.")
                return
        else:
            st.error("⚠️ Please upload a PDF resume or click 'Populate Form with Sample Data'.")
            return

        # 3. Validation: Job description not empty
        clean_jd = job_description.strip()
        if not clean_jd:
            st.error("⚠️ Please paste the target job description to compare against.")
            return

        # Warn if job description is very short
        if len(clean_jd.split()) < 15:
            st.warning("⚠️ The job description you entered is very short (<15 words). For accurate skill matching, paste the complete requirements.")

        # Execute extraction and matching with friendly error handling
        with st.spinner("Extracting resume text, parsing keywords, and auditing skill alignment..."):
            try:
                # Step A: PDF Text Extraction
                pdf_info = extract_text_from_pdf(pdf_bytes)
                resume_text = pdf_info["text"]
                page_count = pdf_info["page_count"]
                word_count = pdf_info["word_count"]

            except ScannedPDFError as spe:
                st.error(f"📄 **Scanned Image PDF Detected:** {spe}")
                return
            except EmptyPDFError as epe:
                st.error(f"📄 **Empty Document:** {epe}")
                return
            except CorruptPDFError as cpe:
                st.error(f"⚠️ **Corrupted File:** {cpe}")
                return
            except PDFExtractionError as pe:
                st.error(f"⚠️ **Extraction Error:** {pe}")
                return
            except Exception as e:
                st.error(f"⚠️ An unexpected error occurred while reading the PDF: {e}")
                return

            # Step B: Keyword & Skill Extraction
            resume_skills = extract_skills(resume_text)
            job_skills = extract_skills(clean_jd)

            # Step C: Match Calculation
            match_result = compare_skills(resume_skills, job_skills)

            # Step D: Suggestions Engine
            suggestions = generate_suggestions(resume_text, match_result, word_count)

            # Step E: Generate PDF Report
            try:
                report_filepath = generate_pdf_report(
                    candidate_name=clean_name,
                    resume_filename=pdf_filename,
                    match_result=match_result,
                    suggestions=suggestions
                )
            except Exception as e:
                report_filepath = None
                st.warning(f"Note: PDF report generation encountered a minor issue: {e}")

            # Step F: Save Record to Persistent History
            entry_id = save_analysis(
                candidate_name=clean_name,
                filename=pdf_filename,
                match_result=match_result,
                suggestions=suggestions,
                word_count=word_count,
                page_count=page_count,
                report_filename=report_filepath
            )

            # Step G: Save to Session State and Navigate to Results
            st.session_state.current_result = {
                "id": entry_id,
                "candidate_name": clean_name,
                "resume_filename": pdf_filename,
                "resume_text": resume_text,
                "job_description": clean_jd,
                "match_result": match_result,
                "suggestions": suggestions,
                "word_count": word_count,
                "page_count": page_count,
                "report_filepath": report_filepath
            }

            st.session_state.current_page = "results"
            st.rerun()
