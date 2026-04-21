import streamlit as st

def show_chatbot_page():
    """Render the chatbot page embedding the Flask app in fullscreen."""
    user = st.session_state.user

    # Hide sidebar and top elements for fullscreen
    st.markdown("""
    <style>
        /* Hide sidebar */
        [data-testid="stSidebar"] { display: none !important; }
        
        /* Hide main menu */
        #MainMenu { display: none !important; }
        
        /* Hide footer */
        footer { display: none !important; }
        
        /* Maximize content area */
        .stMainBlockContainer {
            max-width: 100% !important;
            padding: 0 !important;
            margin: 0 !important;
        }
        
        .stApp {
            max-width: 100% !important;
            margin: 0 !important;
            padding: 0 !important;
        }
        
        /* Remove padding from main container */
        [data-testid="stAppViewContainer"] {
            padding: 0 !important;
            max-width: 100% !important;
        }
        
        /* Ensure iframe container is fullscreen */
        .chatbot-container {
            width: 100vw;
            height: 100vh;
            margin-left: calc(-50vw + 50%);
            margin-top: -50px;
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            z-index: 1000;
        }
    </style>
    """, unsafe_allow_html=True)

    # Embed the Flask chatbot in fullscreen iframe
    st.markdown("""
    <div class="chatbot-container">
        <iframe 
            src="http://localhost:5000" 
            id="chatbot-iframe"
            width="100%" 
            height="100%" 
            style="border: none; display: block; position: absolute; top: 0; left: 0;"
            title="Gemini AI Chatbot"
            allow="*">
        </iframe>
    </div>
    """, unsafe_allow_html=True)