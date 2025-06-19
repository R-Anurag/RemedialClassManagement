import streamlit as st
from utils.auth import login_user, register_user, user_exists
import sqlite3
from db_setup import init_database
init_database()


st.set_page_config(page_title="Remedial Class Manager", layout="centered", page_icon="https://media.istockphoto.com/id/970757378/vector/open-school-backpack-with-supplies.jpg?s=612x612&w=0&k=20&c=ERikE3WguMEr7QRww10O5iXm2E8EjfgHzjhl3xi6k7w=" )
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
