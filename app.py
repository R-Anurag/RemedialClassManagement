import streamlit as st
from utils.auth import login_user, register_user, user_exists
import hashlib

st.set_page_config(page_title="Remedial Class Manager", layout="centered")
st.title("🔑 Welcome to Remedial Class Manager")

# --- Utility: hash password ---
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# --- Auth Mode Selector ---
auth_mode = st.sidebar.selectbox("Login / Register", ["Login", "Register"])

if "user" not in st.session_state:
    st.session_state.user = None

# --- Login ---
if auth_mode == "Login":
    st.subheader("🔐 Login to Continue")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        hashed = hash_password(password)
        user = login_user(username, hashed)
        if user:
            st.success(f"Welcome, {user['name']} ({user['role']})!")
            st.session_state.user = user
            st.switch_page("home.py")
        else:
            st.error("Invalid credentials.")

# --- Register ---
else:
    st.subheader("📝 Register New Account")
    name = st.text_input("Full Name")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    role = st.selectbox("Role", ["student", "teacher", "admin"])

    if st.button("Register"):
        if user_exists(username):
            st.warning("Username already exists. Try logging in.")
        else:
            hashed = hash_password(password)
            register_user(name, username, hashed, role)
            st.success("Account created successfully! Please log in.")
