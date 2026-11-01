"""
pages_ui/home.py
----------------
Landing page for ResumeIQ.
Features a hero banner with inline SVG illustration, quick CTA button,
4 feature highlight cards, 3-step workflow guide, and footer.
"""

import streamlit as st


def render_home_page():
    """Renders the ResumeIQ landing / home page."""

    # --- Hero Section ---
    col_left, col_right = st.columns([1.2, 0.8], vertical_alignment="center")

    with col_left:
        st.markdown("""
        <div class="hero-title">Make Your Resume Job-Ready with ResumeIQ</div>
        <div class="hero-subtitle">
            Analyze your resume, discover missing skills, and improve your chances of matching
            your dream job. Built with deterministic keyword intelligence for transparent results.
        </div>
        """, unsafe_allow_html=True)

        # Primary Call to Action
        if st.button("🚀 Analyze My Resume", key="hero_cta_btn", type="primary", use_container_width=False):
            st.session_state.current_page = "analyze"
            st.rerun()

    with col_right:
        # Crisp inline SVG career / resume audit illustration (no external dependencies)
        st.markdown("""
        <div style="text-align: center; padding: 10px;">
            <svg width="280" height="230" viewBox="0 0 320 260" fill="none" xmlns="http://www.w3.org/2000/svg" style="max-width: 100%; height: auto;">
                <defs>
                    <linearGradient id="gradCard" x1="0%" y1="0%" x2="100%" y2="100%">
                        <stop offset="0%" stop-color="#4F46E5" />
                        <stop offset="100%" stop-color="#2563EB" />
                    </linearGradient>
                    <linearGradient id="gradDoc" x1="0%" y1="0%" x2="100%" y2="100%">
                        <stop offset="0%" stop-color="#FFFFFF" />
                        <stop offset="100%" stop-color="#F1F5F9" />
                    </linearGradient>
                    <filter id="shadow" x="-10%" y="-10%" width="130%" height="130%">
                        <feDropShadow dx="0" dy="10" stdDeviation="12" flood-color="#4F46E5" flood-opacity="0.18"/>
                    </filter>
                </defs>
                
                <!-- Background Blob -->
                <circle cx="160" cy="130" r="105" fill="#EEF2FF" />
                <circle cx="250" cy="70" r="35" fill="#E0E7FF" opacity="0.6" />

                <!-- Resume Sheet Base -->
                <rect x="70" y="30" width="160" height="200" rx="14" fill="url(#gradDoc)" stroke="#CBD5E1" stroke-width="2" filter="url(#shadow)" />
                
                <!-- Resume Header Lines -->
                <rect x="90" y="52" width="55" height="10" rx="5" fill="#4F46E5" />
                <rect x="90" y="70" width="120" height="4" rx="2" fill="#94A3B8" />
                <rect x="90" y="80" width="100" height="4" rx="2" fill="#CBD5E1" />

                <!-- Section: Skills -->
                <rect x="90" y="102" width="70" height="7" rx="3.5" fill="#1E3A8A" />
                
                <!-- Skill Pills inside illustration -->
                <rect x="90" y="120" width="46" height="14" rx="7" fill="#DCFCE7" stroke="#86EFAC" />
                <text x="113" y="131" font-size="8" font-weight="bold" fill="#166534" text-anchor="middle">Python</text>

                <rect x="142" y="120" width="40" height="14" rx="7" fill="#DCFCE7" stroke="#86EFAC" />
                <text x="162" y="131" font-size="8" font-weight="bold" fill="#166534" text-anchor="middle">SQL</text>

                <rect x="90" y="142" width="48" height="14" rx="7" fill="#FEE2E2" stroke="#FCA5A5" />
                <text x="114" y="153" font-size="8" font-weight="bold" fill="#991B1B" text-anchor="middle">Docker</text>

                <rect x="144" y="142" width="42" height="14" rx="7" fill="#DCFCE7" stroke="#86EFAC" />
                <text x="165" y="153" font-size="8" font-weight="bold" fill="#166534" text-anchor="middle">Git</text>

                <!-- Experience Lines -->
                <rect x="90" y="172" width="120" height="4" rx="2" fill="#94A3B8" />
                <rect x="90" y="182" width="105" height="4" rx="2" fill="#CBD5E1" />
                <rect x="90" y="192" width="85" height="4" rx="2" fill="#E2E8F0" />

                <!-- Floating Score Badge -->
                <g filter="url(#shadow)">
                    <rect x="195" y="145" width="85" height="65" rx="12" fill="url(#gradCard)" />
                    <text x="237" y="172" font-size="10" font-weight="bold" fill="#E0E7FF" text-anchor="middle">MATCH</text>
                    <text x="237" y="196" font-size="19" font-weight="800" fill="#FFFFFF" text-anchor="middle">85%</text>
                </g>

                <!-- Checkmark Icon Circle -->
                <circle cx="82" cy="40" r="14" fill="#10B981" />
                <path d="M76 40 L80 44 L88 36" stroke="white" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<hr style='border: none; border-top: 1px solid #E2E8F0; margin: 36px 0 28px 0;'>", unsafe_allow_html=True)

    # --- 4 Feature Cards Section ---
    st.markdown("### Why Choose ResumeIQ?")
    st.markdown("<p style='color: #64748B; margin-bottom: 24px;'>Comprehensive rule-based audit designed for students and job seekers.</p>", unsafe_allow_html=True)

    fc1, fc2, fc3, fc4 = st.columns(4)

    with fc1:
        st.markdown("""
        <div class="custom-card">
            <div class="card-icon" style="background: #EFF6FF; color: #2563EB;">📄</div>
            <div class="card-title">Resume Skill Analysis</div>
            <div class="card-desc">
                Extracts raw text seamlessly from PDF files and detects technical and soft skills against a 200+ master taxonomy.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with fc2:
        st.markdown("""
        <div class="custom-card">
            <div class="card-icon" style="background: #EEF2FF; color: #4F46E5;">🎯</div>
            <div class="card-title">Job Matching</div>
            <div class="card-desc">
                Directly compares candidate skills against specific job requirements using boundary-safe keyword intelligence.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with fc3:
        st.markdown("""
        <div class="custom-card">
            <div class="card-icon" style="background: #FEF2F2; color: #DC2626;">🔍</div>
            <div class="card-title">Missing Skills Gap</div>
            <div class="card-desc">
                Instantly highlights which critical languages, frameworks, databases, or cloud tools are absent from your resume.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with fc4:
        st.markdown("""
        <div class="custom-card">
            <div class="card-icon" style="background: #ECFDF5; color: #059669;">📥</div>
            <div class="card-title">PDF Audit Reports</div>
            <div class="card-desc">
                Download a clean, multi-page ReportLab PDF report containing full audit stats, breakdowns, and suggestions.
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<hr style='border: none; border-top: 1px solid #E2E8F0; margin: 36px 0 28px 0;'>", unsafe_allow_html=True)

    # --- How It Works 3-Step Section ---
    st.markdown("### How It Works in 3 Simple Steps")
    st.markdown("<p style='color: #64748B; margin-bottom: 24px;'>Fast, deterministic, and privacy-respecting local matching pipeline.</p>", unsafe_allow_html=True)

    s1, s2, s3 = st.columns(3)

    with s1:
        st.markdown("""
        <div class="custom-card">
            <div class="step-number">1</div>
            <div class="card-title">Upload Your Resume</div>
            <div class="card-desc">
                Select your text-based PDF resume. PyMuPDF extracts and normalizes the text directly in memory.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with s2:
        st.markdown("""
        <div class="custom-card">
            <div class="step-number">2</div>
            <div class="card-title">Enter Job Description</div>
            <div class="card-desc">
                Paste the target job posting or internship description you wish to tailor your resume for.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with s3:
        st.markdown("""
        <div class="custom-card">
            <div class="step-number">3</div>
            <div class="card-title">Get Actionable Insights</div>
            <div class="card-desc">
                Review your Skill Coverage Score, inspect matched/missing skills, follow tips, and download your PDF audit.
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Bottom CTA banner
    st.markdown("<br>", unsafe_allow_html=True)
    cta_card = st.container()
    with cta_card:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%); border-radius: 16px; padding: 28px; text-align: center; color: white; margin-top: 10px;">
            <h3 style="color: white; margin-bottom: 8px;">Ready to optimize your resume for your dream job?</h3>
            <p style="color: #DBEAFE; font-size: 0.95rem; margin-bottom: 18px;">
                Takes under 5 seconds. Completely local and private.
            </p>
        </div>
        """, unsafe_allow_html=True)

        btn_c1, btn_c2, btn_c3 = st.columns([1, 1, 1])
        with btn_c2:
            if st.button("⚡ Get Started Now", key="bottom_cta_btn", type="primary", use_container_width=True):
                st.session_state.current_page = "analyze"
                st.rerun()

    # --- Footer ---
    st.markdown("""
    <div class="footer-wrapper">
        <p><b>ResumeIQ</b> – AI-Based Resume Analyzer & Job Matching System</p>
        <p style="font-size: 0.8rem; color: #94A3B8;">
            Academic Capstone Project &bull; Built with Python, Streamlit, PyMuPDF, ReportLab &bull; © 2026 ResumeIQ
        </p>
    </div>
    """, unsafe_allow_html=True)
