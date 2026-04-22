import streamlit as st
import os
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
import random
import streamlit.components.v1 as components

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
        st.error(f"Email Error: {e}")
        return False

# ---------------- TIMER FUNCTION ----------------
def show_statistics(pending_count):
    st.markdown("<h2 style='text-align: center;'>Live Assignment Statistics</h2>", unsafe_allow_html=True)

    html_code = f"""
    <html>
    <head>
    <style>
    body {{
        margin: 0;
        display: flex;
        justify-content: center;
        gap: 40px;
        background: transparent;
    }}

    .circle-container {{
        display: flex;
        flex-direction: column;
        align-items: center;
    }}

    .circle {{
        height: 130px;
        width: 130px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 28px;
        font-weight: bold;
        background: conic-gradient(#4f46e5 0deg, #f3f4f6 0deg);
        box-shadow: 0 6px 12px rgba(0,0,0,0.1);
    }}

    .label {{
        margin-top: 10px;
        font-weight: 600;
    }}
    </style>
    </head>
    <body>

    <div class="circle-container">
        <div class="circle">{pending_count}</div>
        <div class="label">Pending</div>
    </div>

    <div class="circle-container">
        <div class="circle" id="h">0</div>
        <div class="label">Hours</div>
    </div>

    <div class="circle-container">
        <div class="circle" id="m">0</div>
        <div class="label">Minutes</div>
    </div>

    <div class="circle-container">
        <div class="circle" id="s">0</div>
        <div class="label">Seconds</div>
    </div>

    <script>
    window.onload = function() {{
        let deadline = new Date();
        deadline.setHours(deadline.getHours() + 11);
        deadline.setMinutes(deadline.getMinutes() + 45);
        deadline.setSeconds(deadline.getSeconds() + 30);

        function updateTimer() {{
            let now = new Date().getTime();
            let distance = deadline.getTime() - now;

            if (distance < 0) distance = 0;

            let hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
            let minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
            let seconds = Math.floor((distance % (1000 * 60)) / 1000);

            document.getElementById("h").innerText = hours;
            document.getElementById("m").innerText = minutes;
            document.getElementById("s").innerText = seconds;
        }}

        setInterval(updateTimer, 1000);
        updateTimer();
    }}
    </script>

    </body>
    </html>
    """
    components.html(html_code, height=280)

# ---------------- CSS ----------------
st.markdown("""
<style>
.stApp { background-color: #cce7ff !important; }
.block-container { background-color: #ffffff !important; padding: 30px !important; border-radius: 14px !important; }
.subject-card { background:#f3f4f6; padding:20px; border-radius:12px; text-align:center; margin-bottom:20px;}
</style>
""", unsafe_allow_html=True)

# ---------------- STORAGE ----------------
UPLOAD_DIR = "uploaded_assignments"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# ---------------- SESSION ----------------
if "users" not in st.session_state:
    st.session_state.users = {"admin": "pass@123", "student": "correct123"}
if "emails" not in st.session_state:
    st.session_state.emails = {"admin": "admin@gmail.com", "student": "student@gmail.com"}
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
    st.session_state.student_stage = "notifications"

subjects = [
    {"name": "Operating System", "icon": "💻"},
    {"name": "Network Administration", "icon": "🌐"},
    {"name": "Cyber Security", "icon": "🛡️"},
    {"name": "Python Programming", "icon": "🐍"},
]

# ---------------- ADMIN ----------------
def admin_dashboard():
    st.title("👨‍💻 Admin Dashboard")
    for subj in subjects:
        file = st.file_uploader(f"Upload {subj['name']}", key=subj["name"])
        if st.button(f"Send {subj['name']}"):
            if file:
                path = os.path.join(UPLOAD_DIR, subj["name"].replace(" ", "_") + "_" + file.name)
                with open(path, "wb") as f:
                    f.write(file.getbuffer())
                st.success("Uploaded successfully ✅")

# ---------------- STUDENT ----------------
def student_dashboard():
    stage = st.session_state.student_stage

    # -------- Notifications --------
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

    # -------- Subjects --------
    elif stage == "subjects":
        st.title("📚 Subjects")
        for subj in subjects:
            st.markdown(f"<div class='subject-card'>{subj['icon']}<br>{subj['name']}</div>", unsafe_allow_html=True)
            if st.button(f"View {subj['name']}", key=subj["name"]):
                st.session_state.student_stage = f"assignments_{subj['name']}"
                st.rerun()

    # -------- Assignments + TIMER --------
    elif stage.startswith("assignments_"):
        subj_name = stage.replace("assignments_", "")
        st.title(f"📂 {subj_name} Assignments")

        files = os.listdir(UPLOAD_DIR)
        subject_files = [f for f in files if f.startswith(subj_name.replace(" ", "_"))]

        # 🔥 TIMER
        show_statistics(len(subject_files))

        for f in subject_files:
            file_path = os.path.join(UPLOAD_DIR, f)
            with open(file_path, "rb") as file:
                st.download_button(f"📥 Download {f}", file, file_name=f)

        if not subject_files:
            st.info("No assignments uploaded yet.")

        if st.button("Back to Subjects"):
            st.session_state.student_stage = "subjects"
            st.rerun()

        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.student_stage = "notifications"
            st.rerun()

# ---------------- MAIN ----------------
st.title("📚 StudyIQ")
menu = st.sidebar.selectbox("Menu", ["Signup", "Login"])

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
                        st.success("OTP sent ✅")
                else:
                    st.error("No email found ❌")
            else:
                st.error("Invalid credentials ❌")

    otp_input = st.text_input("Enter OTP")

    if st.button("Verify OTP"):
        if otp_input == st.session_state.otp:
            st.session_state.logged_in = True
            st.session_state.user = st.session_state.otp_user
            st.session_state.student_stage = "notifications"
            st.session_state.otp_sent = False
            st.rerun()
        else:
            st.error("Wrong OTP ❌")

# ---------------- ROUTING ----------------
if st.session_state.logged_in:
    if st.session_state.user == "admin":
        admin_dashboard()
    else:
        student_dashboard()