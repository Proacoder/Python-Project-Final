"""
Assignment Tracker – Main entry point.
Run with:  streamlit run app.py
"""
import streamlit as st
from database import init_db

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Assignment Tracker",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Global dark theme CSS ─────────────────────────────────────────────────────
st.markdown("""
<style>
    /* Dark Catppuccin-inspired palette */
    :root {
        --bg-base:    #1e1e2e;
        --bg-surface: #181825;
        --border:     #313244;
        --text:       #cdd6f4;
        --subtext:    #a6adc8;
        --accent:     #cba6f7;
        --red:        #f38ba8;
        --yellow:     #f9e2af;
        --green:      #a6e3a1;
    }
    .stApp { background-color: #181825; color: #cdd6f4; }
    .stTextInput > div > input,
    .stTextArea > div > textarea,
    .stSelectbox > div > div,
    .stNumberInput > div > input,
    .stDateInput > div > input {
        background-color: #1e1e2e !important;
        color: #cdd6f4 !important;
        border: 1px solid #313244 !important;
        border-radius: 8px !important;
    }
    .stButton > button {
        border-radius: 8px;
        border: 1px solid #313244;
        background-color: #313244;
        color: #cdd6f4;
        transition: all 0.2s;
    }
    .stButton > button:hover {
        background-color: #45475a;
        border-color: #cba6f7;
    }
    .stButton > button[kind="primary"] {
        background-color: #cba6f7 !important;
        color: #1e1e2e !important;
        border: none !important;
        font-weight: 600;
    }
    .stButton > button[kind="primary"]:hover {
        background-color: #b4befe !important;
    }
    .stExpander {
        background-color: #1e1e2e !important;
        border: 1px solid #313244 !important;
        border-radius: 10px !important;
    }
    .stMetric {
        background-color: #1e1e2e;
        border: 1px solid #313244;
        border-radius: 10px;
        padding: 0.75rem;
    }
    h1, h2, h3, h4 { color: #cdd6f4 !important; }
    hr { border-color: #313244 !important; }
    div[data-testid="stFileUploader"] {
        background-color: #1e1e2e;
        border: 1px dashed #45475a;
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

# ── Init DB on first run ──────────────────────────────────────────────────────
init_db()

# ── Session defaults ──────────────────────────────────────────────────────────
if "page" not in st.session_state:
    st.session_state.page = "login"
if "user" not in st.session_state:
    st.session_state.user = None

# ── Router ─────────────────────────────────────────────────────────────────────
page = st.session_state.page

# Guard: unauthenticated pages
if st.session_state.user is None and page not in ("login", "signup"):
    st.session_state.page = "login"
    page = "login"

if page == "login":
    from login import show_login_page
    show_login_page()

elif page == "signup":
    from signup import show_signup_page
    show_signup_page()

elif page == "dashboard":
    from dashboard import show_dashboard
    show_dashboard()

elif page == "subject":
    from subject_page import show_subject_page
    show_subject_page()

elif page == "all_assignments":
    from all_assignments import show_all_assignments_page
    show_all_assignments_page()

elif page == "chatbot":
    from chatbot_page import show_chatbot_page
    show_chatbot_page()

else:
    st.error(f"Unknown page: {page}")
    if st.button("Go Home"):
        st.session_state.page = "dashboard"
        st.rerun()
