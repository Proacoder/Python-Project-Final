import streamlit as st
import os
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
import random

# ---------------- EMAIL FUNCTION ----------------
def send_email(to_email, otp):
    sender_email = "aaryadalvi0807@gmail.com"
    sender_password = "moruaiyqsoeihobe"

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
        print("Email Error:", e)
        return False


# ---------------- LIGHT UI ----------------
st.markdown("""
<style>
.stApp {
    background-color: #f5f7fb;
}
.block-container {
    background: white;
    padding: 25px;
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
}
h1, h2, h3 {
    color: #222;
}
div.stButton > button {
    background-color: #4CAF50;
    color: white;
    border-radius: 8px;
    font-weight: 500;
}
section[data-testid="stSidebar"] {
    background-color: #ffffff;
}
</style>
""", unsafe_allow_html=True)


# ---------------- STORAGE ----------------
UPLOAD_DIR = "uploaded_assignments"
os.makedirs(UPLOAD_DIR, exist_ok=True)

if "users" not in st.session_state:
    st.session_state.users = {}
if "emails" not in st.session_state:
    st.session_state.emails = {}
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


subjects = [
    "Operating System","Network Administration","Cyber Security",
    "Python Programming","Project Survey & Practices","Advanced DBMS","IoT"
]


# ---------------- ADMIN DASHBOARD ----------------
def admin_dashboard():
    st.title("👨‍💻 Admin Dashboard")

    for subj in subjects:
        st.subheader(subj)
        file = st.file_uploader(f"Upload {subj}", key=subj)

        if st.button(f"Send {subj}"):
            if file:
                safe_subj = subj.replace(" ", "_")
                path = os.path.join(UPLOAD_DIR, safe_subj + "_" + file.name)

                with open(path, "wb") as f:
                    f.write(file.getbuffer())

                st.success("Assignment uploaded successfully ✅")

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()


# ---------------- STUDENT DASHBOARD ----------------
def student_dashboard():
    st.title(f"🎓 Welcome {st.session_state.user}")

    subj = st.radio("Select Subject", subjects)

    st.subheader(f"📂 Files for {subj}")

    files = os.listdir(UPLOAD_DIR)
    found = False

    for f in files:
        if f.startswith(subj.replace(" ", "_")):
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
        st.info("No files uploaded for this subject yet.")

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()


# ---------------- MAIN ----------------
st.title("📚 StudyIQ")

menu = st.sidebar.selectbox("Menu", ["Signup", "Login"])


# -------- SIGNUP --------
if menu == "Signup":
    u = st.text_input("Username")
    e = st.text_input("Email")
    p = st.text_input("Password", type="password")

    if st.button("Register"):
        if u and e and p:
            st.session_state.users[u] = p
            st.session_state.emails[u] = e
            st.success("Registered Successfully ✅")
        else:
            st.warning("Please fill all fields")


# -------- LOGIN --------
elif menu == "Login":
    u = st.text_input("Username")
    p = st.text_input("Password", type="password")

    if st.button("Send OTP"):
        if st.session_state.otp_sent:
            st.warning("OTP already sent")
        else:
            if u in st.session_state.users and st.session_state.users[u] == p:
                otp = str(random.randint(100000, 999999))
                st.session_state.otp = otp
                st.session_state.otp_user = u
                st.session_state.otp_sent = True

                email = st.session_state.emails.get(u)

                if email and send_email(email, otp):
                    st.success("OTP sent to email ✅")
                else:
                    st.error("Failed to send email ❌")
            else:
                st.error("Invalid credentials ❌")

    otp_input = st.text_input("Enter OTP")

    if st.button("Verify OTP"):
        if otp_input == st.session_state.otp:
            st.session_state.logged_in = True
            st.session_state.user = st.session_state.otp_user
            st.session_state.otp = ""
            st.session_state.otp_sent = False
            st.success("Login successful ✅")
        else:
            st.error("Wrong OTP ❌")


# ---------------- ROUTING ----------------
if st.session_state.logged_in:
    if st.session_state.user == "admin":
        admin_dashboard()
    else:
        student_dashboard()