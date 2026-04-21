import streamlit as st
from auth import signup_user


def show_signup_page():
    """Render the Signup / Registration page."""
    st.markdown("""
        <style>
            .auth-logo { text-align: center; font-size: 3rem; margin-bottom: 1rem; }
            .auth-title {
                font-size: 2rem; font-weight: 700; color: #cdd6f4;
                text-align: center; margin-bottom: 0.25rem;
            }
            .auth-subtitle {
                text-align: center; color: #a6adc8;
                margin-bottom: 2rem; font-size: 0.95rem;
            }
            .pw-hint {
                font-size: 0.78rem; color: #6c7086;
                margin-top: -0.6rem; margin-bottom: 0.5rem;
            }
        </style>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<div class="auth-logo">🎓</div>', unsafe_allow_html=True)
        st.markdown('<div class="auth-title">Create Account</div>', unsafe_allow_html=True)
        st.markdown('<div class="auth-subtitle">Start tracking your assignments today</div>', unsafe_allow_html=True)

        with st.form("signup_form", clear_on_submit=False):
            username = st.text_input("Username", placeholder="Choose a username (min 3 chars)")
            email    = st.text_input("Email", placeholder="you@example.com")
            password = st.text_input("Password", type="password", placeholder="Min 8 chars, 1 uppercase, 1 digit")
            st.markdown(
                '<div class="pw-hint">Minimum 8 characters · 1 uppercase letter · 1 digit</div>',
                unsafe_allow_html=True
            )
            confirm  = st.text_input("Confirm Password", type="password", placeholder="Re-enter your password")

            st.markdown("<br>", unsafe_allow_html=True)
            submitted = st.form_submit_button("Create Account", use_container_width=True, type="primary")

            if submitted:
                if not username or not email or not password or not confirm:
                    st.error("Please fill in all fields.")
                elif password != confirm:
                    st.error("Passwords do not match.")
                else:
                    success, message = signup_user(username, email, password)
                    if success:
                        st.success(message + " Please log in.")
                        st.session_state.page = "login"
                        st.rerun()
                    else:
                        st.error(message)

        st.markdown("---")
        st.markdown(
            "<div style='text-align:center; color:#a6adc8;'>Already have an account?</div>",
            unsafe_allow_html=True
        )
        if st.button("Sign In", use_container_width=True):
            st.session_state.page = "login"
            st.rerun()
