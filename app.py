import streamlit as st
from utils.auth import login_user, register_user, user_exists
import sqlite3

def init_db():
    conn = sqlite3.connect("remedial_class.db")
    cursor = conn.cursor()

    # Create tables
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        username TEXT UNIQUE,
        password_hash TEXT,
        role TEXT
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Students (
        student_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        phone TEXT,
        course TEXT,
        year TEXT
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Teachers (
        teacher_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        phone TEXT,
        subject TEXT
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Subjects (
        subject_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        department TEXT
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS RemedialClasses (
        class_id INTEGER PRIMARY KEY AUTOINCREMENT,
        subject_id INTEGER,
        teacher_id INTEGER,
        date TEXT,
        time TEXT,
        room TEXT
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS StudentClassMapping (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER,
        class_id INTEGER
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Attendance (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        class_id INTEGER,
        student_id INTEGER,
        status TEXT,
        date TEXT
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Performance (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER,
        subject_id INTEGER,
        score_before INTEGER,
        score_after INTEGER,
        date TEXT
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Feedback (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        class_id INTEGER,
        student_id INTEGER,
        comment TEXT,
        rating INTEGER
    )
    """)

    conn.commit()
    conn.close()

init_db()

st.set_page_config(page_title="Remedial Class Manager", layout="centered")
st.title("🔑 Welcome to Remedial Class Manager")

# --- Initialize session state ---
if "user" not in st.session_state:
    st.session_state.user = None

# --- Auth Mode Selector ---
auth_mode = st.sidebar.selectbox("Select Option", ["Login", "Register"])

# --- Login ---
if auth_mode == "Login":
    st.subheader("🔐 Login to Continue")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        user = login_user(username, password)  # Pass raw password
        if user:
            st.success(f"Welcome, {user.get('name', username)} ({user['role']})!")
            st.session_state.user = user
            st.switch_page("pages/0_Home.py")  # Fixed path
        else:
            st.error("Invalid credentials. Please try again.")

# --- Register ---
else:
    st.subheader("📝 Create New Account")
    name = st.text_input("Full Name")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    role = st.selectbox("Select Role", ["student", "teacher", "admin"])

    if st.button("Register"):
        if user_exists(username):
            st.warning("Username already exists. Try logging in instead.")
        else:
            success = register_user(name, username, password, role)
            if success:
                st.success("Registration successful! You can now log in.")
            else:
                st.error("Registration failed. Try a different username.")
