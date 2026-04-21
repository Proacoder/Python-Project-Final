import streamlit as st
from auth import login_user


def show_login_page():
    """Render the Login page."""
    st.markdown("""
        <style>
            .auth-card {
                background: #1e1e2e;
                border: 1px solid #313244;
                border-radius: 16px;
                padding: 2.5rem;
                max-width: 420px;
                margin: 2rem auto;
            }
            .auth-title {
                font-size: 2rem;
                font-weight: 700;
                color: #cdd6f4;
                text-align: center;
                margin-bottom: 0.25rem;
            }
            .auth-subtitle {
                text-align: center;
                color: #a6adc8;
                margin-bottom: 2rem;
                font-size: 0.95rem;
            }
            .auth-logo {
                text-align: center;
                font-size: 3rem;
                margin-bottom: 1rem;
            }
        </style>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<div class="auth-logo">📚</div>', unsafe_allow_html=True)
        st.markdown('<div class="auth-title">Welcome Back</div>', unsafe_allow_html=True)
        st.markdown('<div class="auth-subtitle">Sign in to your Assignment Tracker</div>', unsafe_allow_html=True)

        with st.form("login_form", clear_on_submit=False):
            username = st.text_input("Username", placeholder="Enter your username")
            password = st.text_input("Password", type="password", placeholder="Enter your password")

            st.markdown("<br>", unsafe_allow_html=True)
            submitted = st.form_submit_button("Sign In", use_container_width=True, type="primary")

            if submitted:
                if not username or not password:
                    st.error("Please fill in all fields.")
                else:
                    success, result = login_user(username, password)
                    if success:
                        st.session_state.user = result
                        st.session_state.page = "dashboard"
                        st.success("Login successful! Redirecting...")
                        st.rerun()
                    else:
                        st.error(result)

        st.markdown("---")
        st.markdown(
            "<div style='text-align:center; color:#a6adc8;'>Don't have an account?</div>",
            unsafe_allow_html=True
        )
        if st.button("Create an Account", use_container_width=True):
            st.session_state.page = "signup"
            st.rerun()
