import streamlit as st
import sqlite3
import hashlib

# Database connection
conn = sqlite3.connect('remedial_class.db', check_same_thread=False)
cursor = conn.cursor()

# Ensure table exists
cursor.execute("""
CREATE TABLE IF NOT EXISTS Users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL
)
""")
conn.commit()

# --- Password utilities ---
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password, hashed):
    return hash_password(password) == hashed

# --- Create User ---
def register_user(name, username, password, role):
    try:
        password_hash = hash_password(password)
        cursor.execute("""
            INSERT INTO Users (name, username, password_hash, role)
            VALUES (?, ?, ?, ?)
        """, (name, username, password_hash, role))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False

# --- Authenticate User ---
def login_user(username, password):
    cursor.execute("""
        SELECT user_id, name, password_hash, role FROM Users WHERE username = ?
    """, (username,))
    result = cursor.fetchone()
    if result and verify_password(password, result[2]):
        return {
            "user_id": result[0],
            "name": result[1],
            "username": username,
            "role": result[3]
        }
    return None

# --- Check if user exists ---
def user_exists(username):
    cursor.execute("SELECT 1 FROM Users WHERE username = ?", (username,))
    return cursor.fetchone() is not None

# --- Auth UI (optional) ---
def show_login_page():
    st.title("🔐 Login or Register")
    form_type = st.radio("Select Option:", ["Login", "Register"], horizontal=True)

    with st.form(key="auth_form"):
        if form_type == "Register":
            name = st.text_input("Full Name")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if form_type == "Register":
            role = st.selectbox("Role", ["student", "teacher", "admin"])

        submitted = st.form_submit_button(form_type)

        if submitted:
            if form_type == "Login":
                user = login_user(username, password)
                if user:
                    st.success(f"Welcome, {user['name']}!")
                    st.session_state.logged_in = True
                    st.session_state.user = user
                else:
                    st.error("Invalid credentials")

            elif form_type == "Register":
                if user_exists(username):
                    st.warning("Username already exists. Try a different one.")
                else:
                    success = register_user(name, username, password, role)
                    if success:
                        st.success("User registered successfully! Please log in.")
                    else:
                        st.error("Registration failed.")

# --- Auth Gate ---
def auth_gate():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.user = None

    if not st.session_state.logged_in:
        show_login_page()
        st.stop()
