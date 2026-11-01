"""
pages_ui/history.py
-------------------
Audit history page for ResumeIQ.
Displays past evaluations with candidate names, timestamps, scores, and skills counts.
Allows inspecting past results in the results dashboard, re-downloading the PDF report,
deleting individual records, or clearing all history with confirmation.
"""

from pathlib import Path
import streamlit as st

from modules.history_manager import (
    list_history,
    delete_history_by_id,
    clear_history
)
from modules.report_generator import generate_pdf_report


def render_history_page():
    """Renders the historical resume evaluations and action controls."""
    st.markdown("## 📜 Audit History")
    st.markdown(
        "<p style='color: #64748B; margin-bottom: 20px;'>"
        "Review past candidate evaluations, inspect detailed audit breakdowns, and re-download PDF reports."
        "</p>",
        unsafe_allow_html=True
    )

    records = list_history()

    # Empty state handling
    if not records:
        st.markdown("""
        <div style="background: white; border-radius: 16px; border: 1px dashed #CBD5E1; padding: 48px 24px; text-align: center; margin-top: 16px;">
            <div style="font-size: 3rem; margin-bottom: 12px;">📂</div>
            <h4 style="color: #0F172A; margin-bottom: 6px;">No Resume Analyses Saved Yet</h4>
            <p style="color: #64748B; font-size: 0.95rem; max-width: 450px; margin: 0 auto 20px auto;">
                Every time you analyze a resume, the full audit breakdown, score, and recommendations
                will be archived here for instant review.
            </p>
        </div>
        """, unsafe_allow_html=True)

        col_c1, col_c2, col_c3 = st.columns([1, 1, 1])
        with col_c2:
            st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
            if st.button("🚀 Analyze Your First Resume", key="first_analysis_btn", type="primary", use_container_width=True):
                st.session_state.current_page = "analyze"
                st.rerun()
        return

    # Header controls with record count and Clear All option
    top_col1, top_col2 = st.columns([1.5, 1], vertical_alignment="center")
    with top_col1:
        st.markdown(f"**Total Records Archived:** `{len(records)}`")
    with top_col2:
        with st.popover("🗑️ Clear All History", use_container_width=True):
            st.warning("⚠️ Are you sure you want to delete all past analysis records? This cannot be undone.")
            if st.button("Yes, Clear Entire History", type="primary", key="confirm_clear_all"):
                clear_history()
                st.success("All history records cleared.")
                st.rerun()

    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

    # Render each history entry as a polished card
    for record in records:
        entry_id = record.get("id", "")
        name = record.get("name", "Candidate")
        timestamp = record.get("timestamp", "Recent")
        filename = record.get("filename", "resume.pdf")
        score = record.get("score", 0)
        matched_count = record.get("matched_count", len(record.get("matched", [])))
        missing_count = record.get("missing_count", len(record.get("missing", [])))
        report_path = record.get("report_filename")

        # Color-coded score styling
        if score >= 70:
            score_color = "#059669"
            score_bg = "#ECFDF5"
        elif score >= 40:
            score_color = "#D97706"
            score_bg = "#FFFBEB"
        else:
            score_color = "#DC2626"
            score_bg = "#FEF2F2"

        with st.container():
            st.markdown(f"""
            <div style="background: white; border: 1px solid #E2E8F0; border-radius: 14px; padding: 18px; margin-bottom: 12px; box-shadow: 0 2px 6px rgba(0,0,0,0.02);">
                <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px;">
                    <div>
                        <div style="font-family: 'Poppins', sans-serif; font-size: 1.1rem; font-weight: 700; color: #0F172A;">
                            {name}
                        </div>
                        <div style="font-size: 0.82rem; color: #64748B; margin-top: 2px;">
                            📄 {filename} &bull; 🕒 {timestamp}
                        </div>
                    </div>
                    <div style="display: flex; align-items: center; gap: 12px;">
                        <div style="background: {score_bg}; color: {score_color}; font-weight: 800; font-size: 1.1rem; padding: 4px 14px; border-radius: 10px; border: 1px solid {score_color}40;">
                            {score}% Match
                        </div>
                        <span style="font-size: 0.85rem; font-weight: 600; color: #059669;">✓ {matched_count} Matched</span>
                        <span style="font-size: 0.85rem; font-weight: 600; color: #DC2626;">✗ {missing_count} Missing</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Actions row for this specific entry
            act_c1, act_c2, act_c3, act_c4 = st.columns([1, 1, 0.6, 2.4])

            with act_c1:
                # View details in dashboard
                if st.button("👁️ View Dashboard", key=f"view_{entry_id}", use_container_width=True):
                    # Load this record into session_state.current_result
                    match_result = {
                        "matched": record.get("matched", []),
                        "missing": record.get("missing", []),
                        "extra": record.get("extra", []),
                        "total_job_skills": record.get("total_job_skills", matched_count + missing_count),
                        "total_resume_skills": record.get("total_resume_skills", len(record.get("matched", [])) + len(record.get("extra", []))),
                        "match_score": score,
                        "has_job_skills": record.get("has_job_skills", True),
                        "category_breakdown": record.get("category_breakdown", {})
                    }
                    st.session_state.current_result = {
                        "id": entry_id,
                        "candidate_name": name,
                        "resume_filename": filename,
                        "resume_text": "",
                        "job_description": "",
                        "match_result": match_result,
                        "suggestions": record.get("suggestions", []),
                        "word_count": record.get("word_count", 0),
                        "page_count": record.get("page_count", 1),
                        "report_filepath": report_path
                    }
                    st.session_state.current_page = "results"
                    st.rerun()

            with act_c2:
                # Re-download PDF
                pdf_bytes = None
                if report_path and Path(report_path).exists():
                    try:
                        with open(report_path, "rb") as f:
                            pdf_bytes = f.read()
                    except Exception:
                        pdf_bytes = None

                if not pdf_bytes:
                    try:
                        temp_match = {
                            "matched": record.get("matched", []),
                            "missing": record.get("missing", []),
                            "extra": record.get("extra", []),
                            "total_job_skills": record.get("total_job_skills", matched_count + missing_count),
                            "match_score": score,
                            "category_breakdown": record.get("category_breakdown", {})
                        }
                        new_rep = generate_pdf_report(
                            candidate_name=name,
                            resume_filename=filename,
                            match_result=temp_match,
                            suggestions=record.get("suggestions", [])
                        )
                        with open(new_rep, "rb") as f:
                            pdf_bytes = f.read()
                    except Exception:
                        pdf_bytes = None

                if pdf_bytes:
                    st.download_button(
                        label="📥 Download PDF",
                        data=pdf_bytes,
                        file_name=f"ResumeIQ_Report_{name.replace(' ', '_')}.pdf",
                        mime="application/pdf",
                        key=f"dl_{entry_id}",
                        use_container_width=True
                    )
                else:
                    st.button("📥 Download PDF", key=f"dl_dis_{entry_id}", disabled=True, use_container_width=True)

            with act_c3:
                # Delete entry
                if st.button("🗑️ Delete", key=f"del_{entry_id}", use_container_width=True):
                    delete_history_by_id(entry_id)
                    st.rerun()

            st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
