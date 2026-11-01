"""
pages_ui/about.py
-----------------
About page for ResumeIQ.
Contains all project information, purpose, tech stack, and a convenient top config
block where students can easily edit their team names, roll numbers, college, and
guide information for their viva examinations.
"""

import streamlit as st

# =============================================================================
# STUDENT & COLLEGE VIVA CONFIGURATION
# (Edit the values below to customize for your college project viva presentation)
# =============================================================================
ABOUT_CONFIG = {
    "project_name": "ResumeIQ",
    "project_subtitle": "AI-Based Resume Analyzer and Job Matching System",
    "college_name": "Department of Computer Science & Engineering",
    "university": "State Technological University",
    "academic_year": "2025 – 2026",
    "degree_course": "Bachelor of Technology (B.Tech) / B.E. in Computer Science",
    "team_members": [
        {"name": "Student Developer", "roll_no": "CS-2022-01", "role": "Full-Stack System Architecture & UI/UX"}
    ],
    "project_guide": "Dr. Academic Guide, Professor & Research Lead",
    "head_of_department": "Dr. Department Head, Professor & HOD",
    "version": "1.0.0 (Production Ready)"
}


def render_about_page():
    """Renders the About Us and viva documentation page."""
    st.markdown(f"## ℹ️ About {ABOUT_CONFIG['project_name']}")
    st.markdown(
        f"<p style='color: #64748B; margin-top: -6px; font-size: 1.05rem;'>"
        f"{ABOUT_CONFIG['project_subtitle']}"
        f"</p>",
        unsafe_allow_html=True
    )

    # --- Academic Capstone Project Card ---
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #F8FAFC 0%, #EEF2FF 100%); border: 1px solid #C7D2FE; border-radius: 16px; padding: 24px; margin-bottom: 24px;">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 10px;">
            <div>
                <span style="background: #4F46E5; color: white; font-size: 0.75rem; font-weight: 700; padding: 3px 10px; border-radius: 6px; text-transform: uppercase;">
                    College Capstone Project
                </span>
                <h3 style="color: #1E1B4B; margin: 8px 0 4px 0; font-size: 1.35rem;">
                    {ABOUT_CONFIG['college_name']}
                </h3>
                <div style="color: #4338CA; font-weight: 600; font-size: 0.95rem;">
                    {ABOUT_CONFIG['university']} &bull; Academic Year {ABOUT_CONFIG['academic_year']}
                </div>
            </div>
            <div style="text-align: right;">
                <div style="font-size: 0.85rem; color: #64748B;">Degree Program:</div>
                <div style="font-size: 0.95rem; font-weight: 600; color: #0F172A;">{ABOUT_CONFIG['degree_course']}</div>
            </div>
        </div>
        <hr style="border: none; border-top: 1px solid #E0E7FF; margin: 16px 0;">
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px;">
            <div>
                <div style="font-size: 0.8rem; font-weight: 700; color: #64748B; text-transform: uppercase;">Project Guide</div>
                <div style="font-size: 0.95rem; font-weight: 600; color: #1E293B;">{ABOUT_CONFIG['project_guide']}</div>
            </div>
            <div>
                <div style="font-size: 0.8rem; font-weight: 700; color: #64748B; text-transform: uppercase;">Head of Department</div>
                <div style="font-size: 0.95rem; font-weight: 600; color: #1E293B;">{ABOUT_CONFIG['head_of_department']}</div>
            </div>
            <div>
                <div style="font-size: 0.8rem; font-weight: 700; color: #64748B; text-transform: uppercase;">Team Members</div>
                {"".join([f"<div style='font-size: 0.92rem; font-weight: 600; color: #1E293B;'>{m['name']} ({m['roll_no']})</div>" for m in ABOUT_CONFIG['team_members']])}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # --- Project Motivation & Purpose ---
    st.markdown("### 🎯 Purpose & Motivation")
    st.markdown("""
    Every year, thousands of college graduates submit resumes for software engineering roles without knowing whether
    their resumes reflect the explicit technical competencies required by the hiring team.
    
    Commercial "ATS checker" tools on the internet often use misleading marketing terminology—promising false
    "hiring probability percentages" while acting as unexplainable black boxes that upload sensitive student data to
    remote cloud servers.
    
    **ResumeIQ** was built to solve this challenge with **complete transparency, privacy, and mathematical determinism**:
    - **100% Local & Privacy-Preserving:** No resume data ever leaves your computer.
    - **Deterministic Scoring:** The calculation is pure arithmetic based on recognized skill keywords.
    - **No Hallucinations:** Unlike generative LLM wrappers, ResumeIQ never invents false feedback or unpredictable scores.
    """)

    st.markdown("<hr style='border: none; border-top: 1px solid #E2E8F0; margin: 28px 0 20px 0;'>", unsafe_allow_html=True)

    # --- Technologies Used ---
    st.markdown("### 💻 Technology Stack")
    st.markdown("<p style='color: #64748B;'>Zero heavy neural networks, zero paid APIs, 100% robust pure Python engineering.</p>", unsafe_allow_html=True)

    t1, t2, t3 = st.columns(3)
    with t1:
        st.markdown("""
        <div class="custom-card">
            <div style="font-size: 1.4rem; margin-bottom: 6px;">🐍</div>
            <div class="card-title">Python 3.10+</div>
            <div class="card-desc">
                Core programming language powering the entire backend, regular expression engine, and data models.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with t2:
        st.markdown("""
        <div class="custom-card">
            <div style="font-size: 1.4rem; margin-bottom: 6px;">⚡</div>
            <div class="card-title">Streamlit</div>
            <div class="card-desc">
                Modern reactive web application framework powering our multi-page state routing and SaaS design.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with t3:
        st.markdown("""
        <div class="custom-card">
            <div style="font-size: 1.4rem; margin-bottom: 6px;">📑</div>
            <div class="card-title">PyMuPDF (fitz)</div>
            <div class="card-desc">
                Ultra-fast, industrial-grade PDF parsing library for text extraction and document inspection.
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

    t4, t5, t6 = st.columns(3)
    with t4:
        st.markdown("""
        <div class="custom-card">
            <div style="font-size: 1.4rem; margin-bottom: 6px;">📄</div>
            <div class="card-title">ReportLab</div>
            <div class="card-desc">
                Enterprise-grade PDF rendering engine used to dynamically build multi-page, branded audit reports.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with t5:
        st.markdown("""
        <div class="custom-card">
            <div style="font-size: 1.4rem; margin-bottom: 6px;">📊</div>
            <div class="card-title">Matplotlib</div>
            <div class="card-desc">
                Data visualization toolkit generating high-definition category coverage bar charts.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with t6:
        st.markdown("""
        <div class="custom-card">
            <div style="font-size: 1.4rem; margin-bottom: 6px;">💾</div>
            <div class="card-title">JSON Persistence</div>
            <div class="card-desc">
                Atomic local storage with crash-safe recovery for maintaining historical evaluation records.
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<hr style='border: none; border-top: 1px solid #E2E8F0; margin: 28px 0 20px 0;'>", unsafe_allow_html=True)

    # --- Honesty & Ethics ---
    st.markdown("### 🛡️ Ethical AI & Transparency Pledge")
    st.markdown("""
    <div class="honesty-banner" style="font-size: 0.95rem; padding: 18px;">
        <b>HONESTY COMMITMENT:</b> Everywhere in ResumeIQ, our percentage match is strictly designated as a
        <b>Skill Coverage Score</b>. It reflects the mathematical proportion of required job skills present in the resume.
        It is <b>NOT</b> a real ATS score or a hiring prediction.
    </div>
    """, unsafe_allow_html=True)
