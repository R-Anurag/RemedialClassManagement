import streamlit as st
import sqlite3
import hashlib

# Database connection
conn = sqlite3.connect('remedial_class.db', check_same_thread=False)
cursor = conn.cursor()

# Password hashing
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password, hashed):
    return hash_password(password) == hashed

# Create user
def create_user(username, password, role):
    try:
        cursor.execute("INSERT INTO Users (username, password_hash, role) VALUES (?, ?, ?)",
                       (username, hash_password(password), role))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False

# Authenticate user
def login_user(username, password):
    cursor.execute("SELECT user_id, password_hash, role FROM Users WHERE username = ?", (username,))
    result = cursor.fetchone()
    if result and verify_password(password, result[1]):
        return {"user_id": result[0], "username": username, "role": result[2]}
    return None

# Streamlit UI
def show_login_page():
    st.title("🔐 Login or Register")

    form_type = st.radio("Select Option:", ["Login", "Register"], horizontal=True)

    with st.form(key="auth_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if form_type == "Register":
            role = st.selectbox("Role", ["student", "teacher", "admin"])

        submitted = st.form_submit_button(form_type)

        if submitted:
            if form_type == "Login":
                user = login_user(username, password)
                if user:
                    st.success(f"Welcome, {username}!")
                    st.session_state.logged_in = True
                    st.session_state.user = user
                else:
                    st.error("Invalid credentials")

            elif form_type == "Register":
                success = create_user(username, password, role)
                if success:
                    st.success("User registered successfully! Please log in.")
                else:
                    st.error("Username already exists.")

# Initialize session state
def auth_gate():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.user = None

    if not st.session_state.logged_in:
        show_login_page()
        st.stop()
