import streamlit as st

def show_chatbot_page():
    """Render the chatbot page embedding the Flask app."""
    user = st.session_state.user

    # Top bar
    col_title, col_back = st.columns([5, 1])
    with col_title:
        st.markdown("## 🤖 AI Chatbot")
    with col_back:
        if st.button("← Back to Dashboard", use_container_width=True):
            st.session_state.page = "dashboard"
            st.rerun()

    st.markdown("---")

    # Embed the Flask chatbot in an iframe
    st.markdown("""
    <iframe 
        src="http://localhost:5000" 
        width="100%" 
        height="800px" 
        style="border: none; border-radius: 10px;"
        title="Gemini AI Chatbot">
    </iframe>
    """, unsafe_allow_html=True)

    st.info("💡 The chatbot is running in the Flask server at localhost:5000. Make sure to start it with: `python chatbot.py` in the LXA folder.")
