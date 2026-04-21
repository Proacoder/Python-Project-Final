📚 Smart Assignment Tracker (StudyIQ)
🚀 Project Overview
StudyIQ is a Python-based web application built using Streamlit. It helps students manage assignments efficiently with login authentication, OTP verification, assignment uploads, and smart priority tracking.
👨‍💻 Features
🔐 Authentication System

User Signup & Login
Email-based OTP verification
Salted SHA-256 password hashing

👨‍💼 Admin Dashboard

Upload assignments for different subjects
Store files in system

🎓 Student Dashboard

View assignment notifications
Download assignments
Subject-wise organization

🧠 Smart Priority Engine

Auto-calculates priority based on deadline proximity and assignment length
🔴 High / 🟡 Medium / 🟢 Low — updates on every app load

⏱️ Smart Tracking

Live assignment statistics
Countdown timer for deadlines
Auto status: Pending / Completed / Overdue

🛠️ Technologies Used

Python
Streamlit
SQLite
SMTP (Email OTP system)
HTML/CSS (for UI styling)

📂 Project Structure
StudyIQ/
├── app.py
├── login.py
├── signup.py
├── dashboard.py
├── subject_page.py
├── all_assignments.py
├── auth.py
├── database.py
├── subjects.py
├── assignments.py
├── priority.py
├── requirements.txt
├── uploads/
├── tracker.db
└── README.md
⚙️ Installation & Setup

Clone the Repository

bashgit clone https://github.com/aaryadalvi0807/Python-Miniproject-Remote-.git

Navigate to Project Folder

bashcd Python-Miniproject-Remote-

Install Dependencies

bashpip install -r requirements.txt

Run the Application

bashstreamlit run app.py
▶️ How It Works

User registers using username, email, and password
OTP is sent to registered email for verification
Login with credentials
After verification:

Admin uploads assignments for subjects
Students receive notifications


Students can:

View subjects & download assignments
Track pending tasks with live stats and countdown timers
Priority auto-updates as deadlines approach

Interact with chatbot for help on assignments, enlightenment on projects, etc.


👥 Team Contributions
MemberContributions
Aarya Dalvi: Core logic, OTP system, authentication, dashboards
Aagam Lodaria: Priority engine, countdown timer system, deadline tracking
Harsh Mane: Assignment management, All Assignments View, Subject Management, file uploads, chatbot, Database Design, documentation & testing
🌐 GitHub Repository
👉 View Project Repository
1.  (https://github.com/aaryadalvi0807/Python-Miniproject-Remote-)
2.  (https://github.com/Proacoder/Python-Project)
🎥 Project Demo Videos

Aarya:

Demo 1: https://drive.google.com/file/d/1OX9GCkWWfcp16HSpML9YIrbL8_Q4Xu-V/view

Demo 2: https://drive.google.com/file/d/1cG4BuQY0GGhmK5xGFPfDo6-rmVyBkqfo/view?usp=sharing__

Harsh:

Demo 1: Demonstration of Assignment Tracker
https://drive.google.com/file/d/1x7rhLl7SvlJ-Opu1R6GtFLiAfqQXejCk/view?usp=drive_link

Demo 2: Working of Chatbot
https://drive.google.com/file/d/1WQhUoqAr3hJw4FSNBzRwLqXZb84T1Yvc/view?usp=drive_link
