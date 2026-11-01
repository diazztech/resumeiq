"""
pages_ui/results.py
-------------------
Results Dashboard for ResumeIQ.
Displays the circular Skill Coverage Score gauge, mandatory honesty disclaimer,
matched, missing, and extra skill badges, category breakdown bar chart,
rule-based improvement suggestions, and ReportLab PDF download.
"""

from pathlib import Path
import streamlit as st
import matplotlib.pyplot as plt

from modules.report_generator import generate_pdf_report


def render_circular_gauge(score: int) -> str:
    """
    Renders a high-resolution, color-coded SVG circular progress ring.

    Color coding rules:
    - >= 70%: Emerald Green (#10B981)
    - 40% - 69%: Amber / Orange (#F59E0B)
    - < 40%: Crimson Red (#EF4444)
    """
    if score >= 70:
        stroke_color = "#10B981"
        bg_tint = "#ECFDF5"
        verdict = "Strong Keyword Alignment"
    elif score >= 40:
        stroke_color = "#F59E0B"
        bg_tint = "#FFFBEB"
        verdict = "Moderate Alignment – Notable Skill Gaps"
    else:
        stroke_color = "#EF4444"
        bg_tint = "#FEF2F2"
        verdict = "Low Alignment – Critical Skills Missing"

    # SVG geometry parameters
    radius = 65
    circumference = 2 * 3.14159265 * radius
    offset = circumference * (1 - (score / 100))

    svg_html = f"""
    <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 24px; background: white; border-radius: 16px; border: 1px solid #E2E8F0; box-shadow: 0 4px 15px rgba(0,0,0,0.03);">
        <svg width="180" height="180" viewBox="0 0 160 160">
            <!-- Background Track -->
            <circle cx="80" cy="80" r="{radius}" fill="none" stroke="#F1F5F9" stroke-width="12" />
            <!-- Active Score Arc -->
            <circle cx="80" cy="80" r="{radius}" fill="none" stroke="{stroke_color}" stroke-width="12"
                stroke-dasharray="{circumference}" stroke-dashoffset="{offset}"
                stroke-linecap="round"
                transform="rotate(-90 80 80)"
                style="transition: stroke-dashoffset 1s ease-in-out;"
            />
            <!-- Center Score Content -->
            <text x="80" y="76" font-family="'Poppins', sans-serif" font-size="28" font-weight="800" fill="#0F172A" text-anchor="middle" dominant-baseline="middle">
                {score}%
            </text>
            <text x="80" y="100" font-family="'Inter', sans-serif" font-size="9" font-weight="700" fill="#64748B" text-anchor="middle" letter-spacing="0.5">
                MATCH
            </text>
        </svg>
        <div style="margin-top: 10px; font-weight: 700; font-size: 1.05rem; color: #0F172A;">
            Skill Coverage Score
        </div>
        <div style="font-size: 0.88rem; font-weight: 600; color: {stroke_color}; margin-top: 2px;">
            {verdict}
        </div>
    </div>
    """
    return svg_html


def render_category_barchart(category_breakdown: dict):
    """
    Generates a crisp horizontal bar chart using Matplotlib showing
    coverage percentage per skill category.
    """
    categories = []
    coverages = []
    counts_label = []

    for cat_name, cdata in category_breakdown.items():
        if cdata.get("job_count", 0) > 0:
            categories.append(cat_name)
            cov = cdata.get("coverage_pct", 0)
            coverages.append(cov)
            counts_label.append(f"{cdata.get('match_count', 0)}/{cdata.get('job_count', 0)}")

    if not categories:
        st.info("No skill categories found with job requirements.")
        return

    # Invert so top category appears on top
    categories.reverse()
    coverages.reverse()
    counts_label.reverse()

    # Determine bar colors
    bar_colors = [
        "#10B981" if c >= 70 else ("#F59E0B" if c >= 40 else "#EF4444")
        for c in coverages
    ]

    fig, ax = plt.subplots(figsize=(8, max(2.8, len(categories) * 0.45)))
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FFFFFF')

    y_pos = range(len(categories))
    bars = ax.barh(y_pos, coverages, color=bar_colors, height=0.55, edgecolor="none", zorder=3)

    # Style axes
    ax.set_yticks(y_pos)
    ax.set_yticklabels(categories, fontsize=9.5, fontweight='bold', color="#1E293B")
    ax.set_xlim(0, 115)
    ax.set_xlabel("Coverage Percentage (%)", fontsize=9, color="#64748B", labelpad=8)

    # Remove unneeded spines
    for spine in ['top', 'right', 'left', 'bottom']:
        ax.spines[spine].set_visible(False)

    ax.grid(axis='x', linestyle='--', alpha=0.35, color='#CBD5E1', zorder=0)
    ax.tick_params(left=False, bottom=False)

    # Value labels at end of bars
    for i, (bar, cov, cnt) in enumerate(zip(bars, coverages, counts_label)):
        ax.text(
            bar.get_width() + 2,
            bar.get_y() + bar.get_height() / 2,
            f"{cov}% ({cnt})",
            va='center',
            ha='left',
            fontsize=8.5,
            fontweight='bold',
            color='#334155'
        )

    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)


def render_results_page():
    """Renders the comprehensive results dashboard."""
    if "current_result" not in st.session_state or not st.session_state.current_result:
        st.warning("⚠️ No active analysis found. Please run an analysis first.")
        if st.button("⬅️ Go to Analyze Page"):
            st.session_state.current_page = "analyze"
            st.rerun()
        return

    result = st.session_state.current_result
    candidate_name = result.get("candidate_name", "Candidate")
    resume_filename = result.get("resume_filename", "resume.pdf")
    match_result = result.get("match_result", {})
    suggestions = result.get("suggestions", [])
    word_count = result.get("word_count", 0)
    report_filepath = result.get("report_filepath")

    score = match_result.get("match_score", 0)
    matched_skills = match_result.get("matched", [])
    missing_skills = match_result.get("missing", [])
    extra_skills = match_result.get("extra", [])
    total_job_skills = match_result.get("total_job_skills", 0)
    total_resume_skills = match_result.get("total_resume_skills", 0)
    cat_breakdown = match_result.get("category_breakdown", {})

    # Top title and candidate name
    st.markdown(f"## 📊 Results for {candidate_name}")
    st.markdown(
        f"<p style='color: #64748B; margin-top: -8px;'>Evaluated Resume: <b>{resume_filename}</b></p>",
        unsafe_allow_html=True
    )

    # --- TOP ROW: Score Gauge + Honesty Notice + Summary Stats ---
    col_gauge, col_stats = st.columns([0.9, 1.1], vertical_alignment="top")

    with col_gauge:
        st.markdown(render_circular_gauge(score), unsafe_allow_html=True)

        # Mandatory Honesty Note Banner
        st.markdown("""
        <div class="honesty-banner">
            <b>HONESTY NOTE:</b> This percentage shows how many of the job's required skills
            were found in your resume using keyword matching. It is not a real ATS score or a hiring prediction.
        </div>
        """, unsafe_allow_html=True)

    with col_stats:
        st.markdown("##### 📌 Key Audit Summary")
        sc1, sc2 = st.columns(2)
        with sc1:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-value" style="color: #2563EB;">{total_job_skills}</div>
                <div class="stat-title">Job Skills Required</div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-value" style="color: #059669;">{len(matched_skills)}</div>
                <div class="stat-title">Matched Skills</div>
            </div>
            """, unsafe_allow_html=True)

        with sc2:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-value" style="color: #DC2626;">{len(missing_skills)}</div>
                <div class="stat-title">Missing Skills</div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-value" style="color: #475569;">{word_count}</div>
                <div class="stat-title">Resume Word Count</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<hr style='border: none; border-top: 1px solid #E2E8F0; margin: 24px 0 20px 0;'>", unsafe_allow_html=True)

    # --- SKILL PILLS SECTIONS: Matched, Missing, and Extra ---
    col_m, col_u = st.columns(2)

    with col_m:
        st.markdown(f"#### ✅ Matched Skills ({len(matched_skills)})")
        st.markdown("<p style='font-size: 0.85rem; color: #64748B;'>Present in both your resume and the job description.</p>", unsafe_allow_html=True)
        if matched_skills:
            badges_html = " ".join([f'<span class="badge-matched">✓ {skill}</span>' for skill in matched_skills])
            st.markdown(f"<div>{badges_html}</div>", unsafe_allow_html=True)
        else:
            st.info("No matching skills detected between resume and job description.")

    with col_u:
        st.markdown(f"#### ❌ Missing Skills ({len(missing_skills)})")
        st.markdown("<p style='font-size: 0.85rem; color: #64748B;'>Requested in job description but not detected in resume.</p>", unsafe_allow_html=True)
        if missing_skills:
            badges_html = " ".join([f'<span class="badge-missing">✗ {skill}</span>' for skill in missing_skills])
            st.markdown(f"<div>{badges_html}</div>", unsafe_allow_html=True)
        else:
            st.success("🎉 Fantastic! 100% of the recognized job skills appear in your resume.")

    st.markdown("<br>", unsafe_allow_html=True)

    # Extra Skills Section (Neutral Blue/Slate Badges)
    with st.expander(f"➕ Extra Resume Skills ({len(extra_skills)})", expanded=False):
        st.markdown("<p style='font-size: 0.85rem; color: #64748B;'>Skills detected in your resume that were not explicitly mentioned in this job posting.</p>", unsafe_allow_html=True)
        if extra_skills:
            badges_html = " ".join([f'<span class="badge-extra">• {skill}</span>' for skill in extra_skills])
            st.markdown(f"<div>{badges_html}</div>", unsafe_allow_html=True)
        else:
            st.write("No additional unrequested skills found.")

    st.markdown("<hr style='border: none; border-top: 1px solid #E2E8F0; margin: 24px 0 20px 0;'>", unsafe_allow_html=True)

    # --- CATEGORY BREAKDOWN ---
    st.markdown("#### 📈 Skill Category Breakdown")
    st.markdown("<p style='font-size: 0.85rem; color: #64748B;'>Detailed coverage across technical and soft skill domains.</p>", unsafe_allow_html=True)
    if cat_breakdown:
        render_category_barchart(cat_breakdown)
    else:
        st.info("No category data available.")

    st.markdown("<hr style='border: none; border-top: 1px solid #E2E8F0; margin: 24px 0 20px 0;'>", unsafe_allow_html=True)

    # --- RULE-BASED IMPROVEMENT SUGGESTIONS ---
    st.markdown("#### 💡 Improvement Recommendations")
    st.markdown("<p style='font-size: 0.85rem; color: #64748B;'>Targeted advice based on your resume's content, structure, and missing keywords.</p>", unsafe_allow_html=True)

    if suggestions:
        for sug in suggestions:
            prio = sug.get("priority", "Medium")
            prio_class = "prio-high" if prio == "High" else ("prio-medium" if prio == "Medium" else "prio-low")
            st.markdown(f"""
            <div class="sug-card">
                <div class="sug-header">
                    <span class="{prio_class}">{prio} Priority</span>
                    <span style="font-size: 0.8rem; color: #64748B;">&bull; {sug.get('category', 'Advice')}</span>
                </div>
                <div style="font-weight: 700; color: #0F172A; font-size: 0.98rem; margin-bottom: 4px;">
                    {sug.get('title', '')}
                </div>
                <div style="font-size: 0.88rem; color: #475569; line-height: 1.5;">
                    {sug.get('description', '')}
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.success("No critical improvements needed. Your resume is exceptionally well-structured!")

    st.markdown("<hr style='border: none; border-top: 1px solid #E2E8F0; margin: 28px 0 24px 0;'>", unsafe_allow_html=True)

    # --- ACTION BUTTONS ---
    btn_col1, btn_col2, btn_col3 = st.columns([1, 1, 1])

    # 1. Download PDF Report Button
    pdf_bytes = None
    download_filename = f"ResumeIQ_Report_{candidate_name.replace(' ', '_')}.pdf"

    if report_filepath and Path(report_filepath).exists():
        try:
            with open(report_filepath, "rb") as f:
                pdf_bytes = f.read()
        except Exception:
            pdf_bytes = None

    if not pdf_bytes:
        # Generate on demand
        try:
            new_path = generate_pdf_report(
                candidate_name=candidate_name,
                resume_filename=resume_filename,
                match_result=match_result,
                suggestions=suggestions
            )
            with open(new_path, "rb") as f:
                pdf_bytes = f.read()
        except Exception as e:
            st.error(f"Failed to prepare PDF for download: {e}")

    with btn_col1:
        if pdf_bytes:
            st.download_button(
                label="📥 Download PDF Report",
                data=pdf_bytes,
                file_name=download_filename,
                mime="application/pdf",
                type="primary",
                use_container_width=True
            )
        else:
            st.button("📥 Download PDF Report", disabled=True, use_container_width=True)

    with btn_col2:
        if st.button("🔄 Analyze Another Resume", use_container_width=True):
            st.session_state.current_page = "analyze"
            st.rerun()

    with btn_col3:
        if st.button("📜 View Audit History", use_container_width=True):
            st.session_state.current_page = "history"
            st.rerun()
