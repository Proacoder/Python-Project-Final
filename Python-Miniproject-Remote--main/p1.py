import streamlit as st
import os
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
import random

# ---------------- EMAIL FUNCTION ----------------
def send_email(to_email, otp):
    sender_email = "aaryadalvi0807@gmail.com"  # Replace with your Gmail
    sender_password = "moruaiyqsoeihobe"  # Use App Password

    try:
        body = f"""Hello,

Your OTP is: {otp}

Welcome to StudyIQ 🎓

Regards,  
StudyIQ Team
"""
        msg = MIMEText(body, "plain")
        msg["Subject"] = "StudyIQ Login OTP"
        msg["From"] = formataddr(("StudyIQ", sender_email))
        msg["To"] = to_email

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        st.error(f"Email Error: {e}")
        return False

# ---------------- STATIC CLEAN CSS ----------------
st.markdown("""
<style>
/* Full-page light blue background */
.stApp {
    background-color: #cce7ff !important;
    font-family: 'Segoe UI', sans-serif;
}

/* Main container */
.block-container {
    background-color: #ffffff !important;
    padding: 30px !important;
    border-radius: 14px !important;
    box-shadow: 0 6px 18px rgba(0,0,0,0.06) !important;
}

/* Headings */
h1 { text-align: center; color: #1f2937; font-weight: 700; }
h2,h3 { color: #374151; font-weight: 600; }

/* Buttons */
div.stButton > button {
    background-color: #4f46e5 !important;
    color: white !important;
    border-radius: 8px !important;
    border: none !important;
    padding: 10px 16px !important;
    font-weight: 600 !important;
}
div.stButton > button:hover { background-color: #4338ca !important; }

/* Inputs */
input {
    border-radius: 8px !important;
    border: 1px solid #d1d5db !important;
    padding: 8px !important;
}
input:focus {
    border: 1px solid #4f46e5 !important;
    box-shadow: 0 0 4px rgba(79,70,229,0.3) !important;
    outline: none !important;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #ffffff !important;
    border-right: 1px solid #e5e7eb !important;
}

/* Radio buttons */
div[role="radiogroup"] {
    background-color: #f9fafb !important;
    padding: 10px !important;
    border-radius: 8px !important;
}

/* File uploader */
section[data-testid="stFileUploader"] {
    border: 1.5px dashed #9ca3af !important;
    border-radius: 10px !important;
    padding: 10px !important;
    background-color: #e0f0ff !important;
}

/* Download button */
div.stDownloadButton > button {
    background-color: #10b981 !important;
    color: white !important;
    border-radius: 8px !important;
}
div.stDownloadButton > button:hover { background-color: #059669 !important; }

/* Alerts */
.stAlert { border-radius: 8px !important; }

/* Subject cards */
.subject-card {
    background-color: #f3f4f6 !important;
    padding: 20px !important;
    border-radius: 12px !important;
    text-align: center !important;
    box-shadow: 0 4px 12px rgba(0,0,0,0.05) !important;
    margin-bottom: 20px !important;
}
.subject-card img { width: 50px !important; height: 50px !important; margin-bottom: 10px !important; }
</style>
""", unsafe_allow_html=True)

# ---------------- STORAGE ----------------
UPLOAD_DIR = "uploaded_assignments"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# ---------------- SESSION STATE ----------------
if "users" not in st.session_state:
    st.session_state.users = {"admin": "pass@123", "student": "correct123"}  # Default users
if "emails" not in st.session_state:
    st.session_state.emails = {"admin": "admin@gmail.com", "student": "student@gmail.com"}  # Default emails
if "otp" not in st.session_state:
    st.session_state.otp = ""
if "otp_user" not in st.session_state:
    st.session_state.otp_user = ""
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user" not in st.session_state:
    st.session_state.user = ""
if "otp_sent" not in st.session_state:
    st.session_state.otp_sent = False
if "student_stage" not in st.session_state:
    st.session_state.student_stage = "notifications"  # notifications -> subjects -> assignments

subjects = [
    {"name": "Operating System", "icon": "💻"},
    {"name": "Network Administration", "icon": "🌐"},
    {"name": "Cyber Security", "icon": "🛡️"},
    {"name": "Python Programming", "icon": "🐍"},
    {"name": "Project Survey & Practices", "icon": "📊"},
    {"name": "Advanced DBMS", "icon": "🗄️"},
    {"name": "IoT", "icon": "📡"},
]

# ---------------- ADMIN DASHBOARD ----------------
def admin_dashboard():
    st.title("👨‍💻 Admin Dashboard")
    for subj in subjects:
        st.subheader(subj["name"])
        file = st.file_uploader(f"Upload {subj['name']}", key=subj["name"])
        if st.button(f"Send {subj['name']}"):
            if file:
                safe_subj = subj["name"].replace(" ", "_")
                path = os.path.join(UPLOAD_DIR, safe_subj + "_" + file.name)
                with open(path, "wb") as f:
                    f.write(file.getbuffer())
                st.success("Uploaded successfully ✅")
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

# ---------------- STUDENT DASHBOARD ----------------
def student_dashboard():
    stage = st.session_state.student_stage

    # ---------- Notifications stage ----------
    if stage == "notifications":
        st.title(f"🎓 Welcome {st.session_state.user}")
        files = os.listdir(UPLOAD_DIR)
        notifications = []
        for f in files:
            for subj in subjects:
                if f.startswith(subj["name"].replace(" ", "_")):
                    notifications.append(f"{subj['name']}: {f.split('_',1)[1]}")
        if notifications:
            for note in notifications:
                st.info(f"🔔 New assignment uploaded: {note}")
        else:
            st.info("No new assignments yet.")
        if st.button("Next"):
            st.session_state.student_stage = "subjects"
            st.rerun()

    # ---------- Subjects stage ----------
    elif stage == "subjects":
        st.title("📚 Subjects")
        for subj in subjects:
            st.markdown(f"""
            <div class="subject-card">
                <div style="font-size:30px">{subj['icon']}</div>
                <div style="font-weight:600">{subj['name']}</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"View {subj['name']}", key=subj["name"]):
                st.session_state.student_stage = f"assignments_{subj['name']}"
                st.rerun()

    # ---------- Assignments stage ----------
    elif stage.startswith("assignments_"):
        subj_name = stage.replace("assignments_", "")
        st.title(f"📂 {subj_name} Assignments")
        files = os.listdir(UPLOAD_DIR)
        found = False
        for f in files:
            if f.startswith(subj_name.replace(" ", "_")):
                found = True
                file_path = os.path.join(UPLOAD_DIR, f)
                with open(file_path, "rb") as file:
                    st.download_button(
                        label=f"📥 Download {f}",
                        data=file,
                        file_name=f,
                        key=f
                    )
        if not found:
            st.info("No assignments uploaded yet.")
        if st.button("Back to Subjects"):
            st.session_state.student_stage = "subjects"
            st.rerun()
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.student_stage = "notifications"
            st.rerun()

# ---------------- MAIN ----------------
st.title("📚 StudyIQ")
menu = st.sidebar.selectbox("Menu", ["Signup", "Login"])

# -------- SIGNUP --------
if menu == "Signup":
    st.subheader("Create Account")
    u = st.text_input("Username")
    e = st.text_input("Email")
    p = st.text_input("Password", type="password")
    if st.button("Register"):
        if u and e and p:
            st.session_state.users[u] = p
            st.session_state.emails[u] = e
            st.success("Registered ✅")
        else:
            st.warning("Fill all fields")

# -------- LOGIN --------
elif menu == "Login":
    st.subheader("Login")
    u = st.text_input("Username")
    p = st.text_input("Password", type="password")
    if st.button("Send OTP"):
        if st.session_state.otp_sent:
            st.warning("OTP already sent")
        else:
            if u in st.session_state.users and st.session_state.users[u] == p:
                email = st.session_state.emails.get(u)
                if email:
                    otp = str(random.randint(100000, 999999))
                    st.session_state.otp = otp
                    st.session_state.otp_user = u
                    st.session_state.otp_sent = True
                    if send_email(email, otp):
                        st.success("OTP sent ✅ Check your email")
                    else:
                        st.error("Email failed ❌ Check SMTP settings")
                else:
                    st.error("No email found for this user ❌")
            else:
                st.error("Invalid credentials ❌")
    otp_input = st.text_input("Enter OTP")
    if st.button("Verify OTP"):
        if otp_input == st.session_state.otp:
            st.session_state.logged_in = True
            st.session_state.user = st.session_state.otp_user
            st.session_state.otp = ""
            st.session_state.otp_sent = False
            st.session_state.student_stage = "notifications"
            st.success("Login successful ✅")
            st.rerun()
        else:
            st.error("Wrong OTP ❌")

# ---------------- ROUTING ----------------
if st.session_state.logged_in:
    if st.session_state.user == "admin":
        admin_dashboard()
    else:
        student_dashboard()