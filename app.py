import streamlit as st
from utils.auth import login_user, register_user, user_exists

st.set_page_config(page_title="Remedial Class Manager", layout="centered")
st.title("🔑 Welcome to Remedial Class Manager")

# --- Auth Mode Selector ---
auth_mode = st.sidebar.selectbox("Select Option", ["Login", "Register"])

# --- Session Initialization ---
if "user" not in st.session_state:
    st.session_state.user = None

# --- Login Section ---
if auth_mode == "Login":
    st.subheader("🔐 Login to Continue")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        user = login_user(username, password)  # Pass plain password
        if user:
            st.success(f"Welcome, {user.get('name', username)} ({user['role']})!")
            st.session_state.user = user
            st.switch_page("0_Home.py")
        else:
            st.error("Invalid credentials. Please try again.")

# --- Register Section ---
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
            success = register_user(name, username, password, role)  # Pass plain password
            if success:
                st.success("Registration successful! You can now log in.")
            else:
                st.error("Registration failed. Please try a different username.")
