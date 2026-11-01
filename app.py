"""
app.py
------
Streamlit entry point and routing manager for ResumeIQ.
Loads custom CSS, renders the top navigation bar, and controls page switching
via st.session_state (without multipage sidebars).
"""

import sys
from pathlib import Path
import streamlit as st

# Ensure project root is available in module search path
PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Page configuration
st.set_page_config(
    page_title="ResumeIQ – AI-Based Resume Analyzer & Job Matching",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Load custom CSS
CSS_FILE = PROJECT_ROOT / "styles" / "style.css"
if CSS_FILE.exists():
    with open(CSS_FILE, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Import page rendering functions
from pages_ui.home import render_home_page
from pages_ui.analyze import render_analyze_page
from pages_ui.results import render_results_page
from pages_ui.how_it_works import render_how_it_works_page
from pages_ui.history import render_history_page
from pages_ui.about import render_about_page

# Initialize session state routing
if "current_page" not in st.session_state:
    st.session_state.current_page = "home"


def render_navbar():
    """Renders the top navigation bar with active page indicator."""
    nav_c1, nav_c2, nav_c3, nav_c4, nav_c5, nav_c6 = st.columns(
        [2.2, 1, 1.2, 1.1, 1, 1],
        vertical_alignment="center"
    )

    current = st.session_state.current_page

    with nav_c1:
        # Brand Logo and Title
        st.markdown("""
        <div class="brand-container">
            <div class="brand-logo">⚡</div>
            <div class="brand-text">ResumeIQ</div>
        </div>
        """, unsafe_allow_html=True)

    with nav_c2:
        is_active = (current == "home")
        if st.button("🏠 Home", key="nav_home", type="primary" if is_active else "secondary", use_container_width=True):
            st.session_state.current_page = "home"
            st.rerun()

    with nav_c3:
        is_active = (current == "analyze")
        if st.button("🔍 Analyze", key="nav_analyze", type="primary" if is_active else "secondary", use_container_width=True):
            st.session_state.current_page = "analyze"
            st.rerun()

    with nav_c4:
        is_active = (current == "how_it_works")
        if st.button("⚙️ How It Works", key="nav_how", type="primary" if is_active else "secondary", use_container_width=True):
            st.session_state.current_page = "how_it_works"
            st.rerun()

    with nav_c5:
        is_active = (current == "history")
        if st.button("📜 History", key="nav_hist", type="primary" if is_active else "secondary", use_container_width=True):
            st.session_state.current_page = "history"
            st.rerun()

    with nav_c6:
        is_active = (current == "about")
        if st.button("ℹ️ About", key="nav_about", type="primary" if is_active else "secondary", use_container_width=True):
            st.session_state.current_page = "about"
            st.rerun()

    st.markdown("<hr style='border: none; border-top: 1px solid #E2E8F0; margin: 12px 0 24px 0;'>", unsafe_allow_html=True)


def main():
    """Main routing controller."""
    render_navbar()

    # Route based on session state
    page = st.session_state.get("current_page", "home")

    if page == "home":
        render_home_page()
    elif page == "analyze":
        render_analyze_page()
    elif page == "results":
        render_results_page()
    elif page == "how_it_works":
        render_how_it_works_page()
    elif page == "history":
        render_history_page()
    elif page == "about":
        render_about_page()
    else:
        render_home_page()


if __name__ == "__main__":
    main()
