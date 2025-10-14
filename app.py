import streamlit as st
from utils.auth import login_user, register_user, user_exists
from utils.theme import apply_theme
import sqlite3
from db_setup import init_database
from streamlit_lottie import st_lottie
import requests
import json

init_database()

st.set_page_config(page_title="Remedial Class Manager", layout="centered", page_icon="🏫")

# Apply theme
apply_theme()

# Load Lottie animation
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_animation = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_jcikwtux.json")  # Education-themed animation

# Main container with fade-in animation
st.markdown('<div class="fade-in">', unsafe_allow_html=True)

col1, col2 = st.columns([1, 2])

with col1:
    st_lottie(lottie_animation, height=200, key="welcome")

with col2:
    st.title("🔑 Welcome to Remedial Class Manager")
    st.markdown(
        """
        <div class='fade-in' style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 1rem; border-radius: 15px; color: white; box-shadow: 0 4px 15px rgba(0,0,0,0.1);'>
            <h4 style='margin: 0;'>Secure Access Portal</h4>
            <p style='margin: 0.5rem 0 0 0;'>Login or register to access your personalized dashboard.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

# --- Initialize session state ---
if "user" not in st.session_state:
    st.session_state.user = None

# --- Auth Mode Selector with animation ---
st.markdown('<div class="slide-in">', unsafe_allow_html=True)
auth_mode = st.sidebar.selectbox("Select Option", ["Login", "Register"])
st.markdown('</div>', unsafe_allow_html=True)

# --- Login ---
if auth_mode == "Login":
    st.subheader("🔐 Login to Continue")
    with st.form("login_form"):
        username = st.text_input("Username", placeholder="Enter your username")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        submitted = st.form_submit_button("🚀 Login")

        if submitted:
            with st.spinner("Authenticating..."):
                user = login_user(username, password)
            if user:
                st.success(f"🎉 Welcome back, {user.get('name', username)} ({user['role']})!")
                st.balloons()
                st.session_state.user = user
                st.switch_page("pages/0_Redirect.py")
            else:
                st.error("❌ Invalid credentials. Please try again.")

# --- Register ---
else:
    st.subheader("📝 Create New Account")
    with st.form("register_form"):
        name = st.text_input("Full Name", placeholder="Enter your full name")
        username = st.text_input("Username", placeholder="Choose a username")
        password = st.text_input("Password", type="password", placeholder="Create a password")
        role = st.selectbox("Select Role", ["student", "teacher", "admin"])
        submitted = st.form_submit_button("✨ Register")

        if submitted:
            if user_exists(username):
                st.warning("⚠️ Username already exists. Try logging in instead.")
            else:
                with st.spinner("Creating account..."):
                    success = register_user(name, username, password, role)
                if success:
                    st.success("🎊 Registration successful! You can now log in.")
                    st.snow()
                else:
                    st.error("❌ Registration failed. Try a different username.")

st.markdown('</div>', unsafe_allow_html=True)
