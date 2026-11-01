"""
pages_ui/how_it_works.py
------------------------
Explains the internal architecture, algorithms, and matching pipeline of ResumeIQ.
Written in clear, beginner-friendly language ideal for college viva presentations,
with an honest section outlining the limitations of rule-based keyword matching.
"""

import streamlit as st


def render_how_it_works_page():
    """Renders the architecture walkthrough and algorithmic pipeline."""
    st.markdown("## ⚙️ How ResumeIQ Works")
    st.markdown(
        "<p style='color: #64748B; margin-bottom: 24px;'>"
        "An end-to-end breakdown of our deterministic, rule-based text processing and job matching pipeline."
        "</p>",
        unsafe_allow_html=True
    )

    # Architectural Overview Card
    st.markdown("""
    <div style="background: white; border-radius: 16px; border: 1px solid #E2E8F0; padding: 24px; margin-bottom: 24px; box-shadow: 0 4px 12px rgba(0,0,0,0.03);">
        <h4 style="color: #1E3A8A; margin-bottom: 8px;">Deterministic Pipeline Architecture</h4>
        <p style="color: #475569; font-size: 0.95rem; line-height: 1.6;">
            Unlike opaque deep-learning models or paid third-party AI APIs that hallucinate or act as black boxes,
            <b>ResumeIQ</b> is 100% deterministic, explainable, and local. Every score, matched skill, and
            recommendation can be mathematically verified and explained step-by-step.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # --- 8 Step Pipeline Walkthrough ---
    steps = [
        {
            "num": "01",
            "title": "PDF Ingestion & Text Extraction (PyMuPDF)",
            "desc": (
                "The user's PDF resume is read as an in-memory byte buffer by PyMuPDF (fitz). "
                "The engine iterates across all document pages, extracting raw text streams. "
                "If the document has 0 pages, is password-protected, corrupt, or contains no selectable text "
                "(such as a scanned image or screenshot), specific custom exceptions (`ScannedPDFError`, `CorruptPDFError`) "
                "are intercepted with user-friendly corrective messages."
            )
        },
        {
            "num": "02",
            "title": "Text Cleaning & Normalization",
            "desc": (
                "Raw extracted text often contains odd unicode characters, null bytes, non-breaking spaces, "
                "or chaotic carriage returns (`\\r\\n`). Our cleaning routine normalizes whitespace, "
                "collapses excessive blank lines, removes control characters, and prepares uniform text for matching."
            )
        },
        {
            "num": "03",
            "title": "Master Skills Database & Taxonomy",
            "desc": (
                "ResumeIQ contains an curated database of over 200+ skills grouped into 7 domains: "
                "Programming Languages, Web Development, Databases, Data Science & ML, Cloud & DevOps, "
                "Developer Tools, and Soft Skills. Each skill entry includes aliases (e.g. 'js' and 'javascript', "
                "'k8s' and 'kubernetes', 'ci/cd' and 'continuous integration') to recognize common industry variations."
            )
        },
        {
            "num": "04",
            "title": "Boundary-Safe Regular Expression Matching",
            "desc": (
                "Standard regex `\\b` word boundaries fail on special characters like `C++`, `C#`, or `.NET`, "
                "and naive substring matching causes false positives (e.g., 'Java' matching inside 'JavaScript'). "
                "ResumeIQ uses pre-compiled negative lookarounds: <code>(?&lt;![a-zA-Z0-9_])alias(?![a-zA-Z0-9_])</code> "
                "with case-insensitivity to guarantee exact, boundary-safe detection."
            )
        },
        {
            "num": "05",
            "title": "Mathematical Skill Coverage Scoring",
            "desc": (
                "The engine computes the mathematical intersection between the set of recognized skills in the resume "
                "and the set required by the job posting:<br>"
                "<div style='background: #F1F5F9; padding: 10px 16px; border-radius: 8px; font-family: monospace; margin: 8px 0; font-weight: bold; color: #1E3A8A;'>"
                "Skill Coverage Score = (Matched Job Skills / Total Unique Job Skills) × 100"
                "</div>"
                "If the job description mentions 10 skills and your resume includes 7 of them, your score is exactly 70%."
            )
        },
        {
            "num": "06",
            "title": "Rule-Based Improvement Suggestions",
            "desc": (
                "The suggestions engine evaluates 8 distinct structural and qualitative heuristics: "
                "(1) Missing skills grouped by category, (2) Presence of a dedicated 'Projects' section, "
                "(3) Quantified metrics with numbers and percentages, (4) Explicit 'Technical Skills' section, "
                "(5) Contact information (email, phone, LinkedIn/GitHub links), (6) Education section, "
                "(7) Practical experience / internships, and (8) Word count and resume brevity."
            )
        },
        {
            "num": "07",
            "title": "Multi-Page PDF Report Generation (ReportLab)",
            "desc": (
                "Using ReportLab Platypus, ResumeIQ constructs a publication-quality PDF audit document. "
                "A custom two-pass <code>NumberedCanvas</code> calculates total pages dynamically for 'Page X of Y' "
                "running footers, and table cells utilize auto-wrapping Flowables to prevent text clipping."
            )
        },
        {
            "num": "08",
            "title": "Persistent JSON History & Crash Recovery",
            "desc": (
                "Every analysis is recorded in <code>data/history.json</code> with a unique UUID. "
                "The history manager features atomic writes via temporary files and automatic corrupted JSON backup "
                "and recovery, ensuring zero runtime crashes."
            )
        }
    ]

    for s in steps:
        st.markdown(f"""
        <div style="background: white; border: 1px solid #E2E8F0; border-radius: 14px; padding: 20px; margin-bottom: 14px; box-shadow: 0 2px 6px rgba(0,0,0,0.02);">
            <div style="display: flex; align-items: baseline; gap: 12px; margin-bottom: 6px;">
                <span style="font-family: 'Poppins', sans-serif; font-size: 1.1rem; font-weight: 800; color: #4F46E5;">{s['num']}</span>
                <span style="font-family: 'Poppins', sans-serif; font-size: 1.05rem; font-weight: 700; color: #0F172A;">{s['title']}</span>
            </div>
            <div style="color: #475569; font-size: 0.92rem; line-height: 1.55; padding-left: 32px;">
                {s['desc']}
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<hr style='border: none; border-top: 1px solid #E2E8F0; margin: 32px 0 24px 0;'>", unsafe_allow_html=True)

    # --- Limitations of Keyword Matching (Honesty Section) ---
    st.markdown("### ⚠️ Honest Limitations of Keyword Matching")
    st.markdown(
        "<p style='color: #64748B; margin-bottom: 16px;'>"
        "Why our score is called a <b>Skill Coverage Score</b> and NOT an 'ATS Score' or 'Hiring Prediction':"
        "</p>",
        unsafe_allow_html=True
    )

    l1, l2, l3 = st.columns(3)
    with l1:
        st.markdown("""
        <div class="custom-card">
            <div style="font-size: 1.3rem; margin-bottom: 8px;">📖</div>
            <div class="card-title">Keyword Frequency ≠ Mastery</div>
            <div class="card-desc">
                Mentioning "Python" once in a resume is counted the same as having 5 years of production experience.
                Keyword matching cannot gauge depth of expertise.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with l2:
        st.markdown("""
        <div class="custom-card">
            <div style="font-size: 1.3rem; margin-bottom: 8px;">🧠</div>
            <div class="card-title">Contextual Nuance</div>
            <div class="card-desc">
                If an applicant writes "Interested in learning Docker in the future", a keyword matcher flags Docker
                even though the candidate hasn't worked with it yet.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with l3:
        st.markdown("""
        <div class="custom-card">
            <div style="font-size: 1.3rem; margin-bottom: 8px;">🏢</div>
            <div class="card-title">Proprietary ATS Systems</div>
            <div class="card-desc">
                Commercial enterprise ATS platforms (Workday, Greenhouse, Taleo) do not share their proprietary ranking
                algorithms. Claiming any tool produces a "real ATS score" is dishonest.
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🚀 Try an Analysis Now", key="how_cta_btn", type="primary"):
        st.session_state.current_page = "analyze"
        st.rerun()
