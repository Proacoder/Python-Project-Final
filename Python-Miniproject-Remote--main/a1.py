import streamlit as st
import smtplib
import os
import re
from email.mime.text import MIMEText

# ---------------- USERS ----------------
users = {
    "user1": "pass123",
    "user2": "abc456"
}

# ---------------- EMAIL VALIDATION ----------------
def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

# ---------------- EMAIL FUNCTION ----------------
def test_email(to_email, username):
    """
    Sends an alert email.
    """

    sender_email = os.getenv("EMAIL_USER")
    app_password = os.getenv("EMAIL_PASS")

    if not sender_email or not app_password:
        st.error("Email credentials not set.")
        return

    if not is_valid_email(to_email):
        st.error("Invalid email address.")
        return

    subject = "⚠️ Test Email Alert"
    body = f"⚠️ Test email triggered for user: {username}"

    msg = MIMEText(body)
    msg['From'] = sender_email
    msg['To'] = to_email
    msg['Subject'] = subject

    try:
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login(sender_email, app_password)
        server.send_message(msg)
        server.quit()
        st.success(f"Test email sent to {to_email} ✅")
    except Exception as e:
        st.error(f"Email Error: {e}")

# ---------------- SIDEBAR NAVIGATION ----------------
st.sidebar.title("Account")
option = st.sidebar.selectbox("Choose Option", ["Login", "Sign Up"])

# ---------------- LOGIN ----------------
if option == "Login":
    st.subheader("🔒 Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username in users and users[username] == password:
            st.success(f"Welcome, {username}!")
        else:
            st.error("Incorrect username or password!")

# ---------------- SIGN UP ----------------
elif option == "Sign Up":
    st.subheader("📝 Sign Up")
    new_username = st.text_input("New Username")
    new_password = st.text_input("New Password", type="password")
    email = st.text_input("Email")

    if st.button("Register"):
        if new_username in users:
            st.warning("Username already exists!")
        else:
            users[new_username] = new_password
            st.success(f"User {new_username} registered successfully!")

    # ---------------- TEST EMAIL BUTTON ----------------
    if st.button("Test Email"):
        if new_username and email:
            test_email(email, new_username)
        else:
            st.warning("Enter a username and email to test.")