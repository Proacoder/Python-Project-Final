import streamlit as st
from datetime import datetime
import os

# ---------------- FOLDER SETUP ----------------
UPLOAD_DIR = "uploaded_assignments"
os.makedirs(UPLOAD_DIR, exist_ok=True)  # Persistent folder for all assignments

# ---------------- SESSION STATE ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "admin_logged_in" not in st.session_state:
    st.session_state.admin_logged_in = False
if "user_name" not in st.session_state:
    st.session_state.user_name = ""
if "selected_subject" not in st.session_state:
    st.session_state.selected_subject = None
if "deadlines" not in st.session_state:
    st.session_state.deadlines = {
        "Operating System": None,
        "Network Administration": None,
        "Cyber Security": None,
        "Python Programming": None,
        "Project Survey & Practices": None,
        "Advanced DBMS": None,
        "IoT": None
    }
if "submissions" not in st.session_state:
    st.session_state.submissions = {subj: {"submitted": [], "pending": []} for subj in st.session_state.deadlines}
if "notifications" not in st.session_state:
    st.session_state.notifications = []

subjects = list(st.session_state.deadlines.keys())

# ---------------- TIMERS ----------------
def display_timer(subject):
    deadline = st.session_state.deadlines.get(subject)
    if deadline:
        now = datetime.now()
        if deadline > now:
            remaining = deadline - now
            days = remaining.days
            hours, rem = divmod(remaining.seconds, 3600)
            minutes, seconds = divmod(rem, 60)
            st.markdown(f"⏰ Time Remaining: {days}d {hours}h {minutes}m {seconds}s")
        else:
            st.warning("⚠️ Deadline passed!")

# ---------------- ADMIN DASHBOARD ----------------
def show_admin_dashboard():
    st.title("👨‍💻 Admin Dashboard")
    for subj in subjects:
        st.subheader(f"📌 {subj}")
        display_timer(subj)
        
        # Admin uploads assignment
        uploaded_file = st.file_uploader(f"Upload assignment for {subj}", type=["pdf","docx","txt"], key=subj+"_admin")
        if st.button(f"Send Assignment {subj}"):
            if uploaded_file:
                # Save file with subject prefix
                file_name = f"{subj.replace(' ','_')}_{uploaded_file.name}"
                file_path = os.path.join(UPLOAD_DIR, file_name)
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                st.success(f"Assignment '{uploaded_file.name}' uploaded for {subj}")
                # Notify all pending students
                for student in st.session_state.submissions[subj]["pending"]:
                    st.session_state.notifications.append(f"New assignment '{uploaded_file.name}' for {subj} sent to {student} at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            else:
                st.warning("Upload a file first!")

        # Show existing assignments with Open button
        st.subheader("📄 Existing Assignments")
        all_files = [f for f in os.listdir(UPLOAD_DIR) if f.startswith(subj.replace(" ","_")) and "student_" not in f]
        if all_files:
            for f in all_files:
                file_path = os.path.join(UPLOAD_DIR, f)
                st.download_button(label=f"Open {f}", data=open(file_path, "rb").read(), file_name=f)
        else:
            st.info("No assignments yet.")

        # View submitted / pending students
        col1, col2 = st.columns(2)
        with col1:
            if st.button(f"View Submitted - {subj}"):
                st.write(st.session_state.submissions[subj]["submitted"] if st.session_state.submissions[subj]["submitted"] else "No submissions yet")
        with col2:
            if st.button(f"View Pending - {subj}"):
                st.write(st.session_state.submissions[subj]["pending"] if st.session_state.submissions[subj]["pending"] else "No pending students")

        st.markdown("---")
    
    # Update deadlines
    st.subheader("🛠 Update Deadlines")
    for subj in subjects:
        d = st.date_input(f"{subj} Deadline Date", key=subj+"_date")
        t = st.time_input(f"{subj} Deadline Time", key=subj+"_time")
        st.session_state.deadlines[subj] = datetime.combine(d,t)
    if st.button("Update Deadlines"):
        st.success("Deadlines Updated ✅")
    
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.admin_logged_in = False
        st.rerun()

# ---------------- STUDENT DASHBOARD ----------------
def show_student_dashboard(user):
    st.title(f"🎓 Welcome, {user}")
    for subj in subjects:
        if st.button(subj):
            st.session_state.selected_subject = subj
            st.rerun()

    if st.session_state.selected_subject:
        subj = st.session_state.selected_subject
        st.header(f"📖 {subj}")
        display_timer(subj)

        # Show assignments from admin
        st.subheader("📄 Assignments")
        all_files = [f for f in os.listdir(UPLOAD_DIR) if f.startswith(subj.replace(" ","_")) and "student_" not in f]
        if all_files:
            for f in all_files:
                file_path = os.path.join(UPLOAD_DIR, f)
                st.download_button(label=f"Open {f}", data=open(file_path, "rb").read(), file_name=f)
        else:
            st.info("No assignments yet.")

        # Submit assignment
        st.subheader("📂 Submit Your Assignment")
        uploaded_file = st.file_uploader("Choose your file", type=["pdf","docx","txt"])
        if st.button("Submit Assignment"):
            if uploaded_file:
                student_file = f"{subj.replace(' ','_')}_student_{user}_{uploaded_file.name}"
                path = os.path.join(UPLOAD_DIR, student_file)
                with open(path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                if user not in st.session_state.submissions[subj]["submitted"]:
                    st.session_state.submissions[subj]["submitted"].append(user)
                if user in st.session_state.submissions[subj]["pending"]:
                    st.session_state.submissions[subj]["pending"].remove(user)
                st.session_state.notifications.append(f"{user} submitted {subj} at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                st.success("Assignment submitted ✅")
            else:
                st.warning("Upload a file before submitting")

        if st.button("⬅ Back"):
            st.session_state.selected_subject = None
            st.rerun()

    # Notifications
    if st.button("🔔 View Notifications"):
        st.subheader("🔔 Notifications")
        relevant = [n for n in st.session_state.notifications if user in n or "sent to" in n]
        if relevant:
            for n in reversed(relevant):
                st.info(n)
        else:
            st.info("No notifications yet.")

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

# ---------------- LOGIN / SIGNUP ----------------
st.title("📚 StudyIQ Assignment Tracker")
menu = st.sidebar.selectbox("Choose Option", ["Sign Up","Login"])

if menu == "Sign Up":
    new_user = st.text_input("New Username")
    new_password = st.text_input("New Password", type="password")
    if st.button("Register"):
        st.success("Account created ✅")
        for subj in subjects:
            if new_user not in st.session_state.submissions[subj]["pending"]:
                st.session_state.submissions[subj]["pending"].append(new_user)

elif menu == "Login":
    user = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if user == "admin" and password == "pass@123":
            st.session_state.logged_in = True
            st.session_state.admin_logged_in = True
            st.session_state.user_name = "Admin"
            st.success("Admin Logged In ✅")
            st.rerun()
        elif password == "correct123":
            st.session_state.logged_in = True
            st.session_state.user_name = user
            for subj in subjects:
                if user not in st.session_state.submissions[subj]["submitted"] and user not in st.session_state.submissions[subj]["pending"]:
                    st.session_state.submissions[subj]["pending"].append(user)
            st.success("Student Logged In ✅")
            st.rerun()
        else:
            st.error("Wrong Username or Password ❌")

# ---------------- SHOW DASHBOARD ----------------
if st.session_state.logged_in:
    if st.session_state.admin_logged_in:
        show_admin_dashboard()
    else:
        show_student_dashboard(st.session_state.user_name)