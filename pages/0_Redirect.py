import streamlit as st
import time
from utils.theme import apply_theme
from streamlit_lottie import st_lottie
import requests

st.set_page_config(page_title="Redirect", layout="centered", page_icon="🏫")

# Apply theme
apply_theme()

# Load Lottie animation for redirect
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

redirect_animation = load_lottieurl("https://assets2.lottiefiles.com/packages/lf20_usmfx6bp.json")  # Loading animation

# --- Session Guard ---
if "user" not in st.session_state or st.session_state.user is None:
    st.markdown('<div class="fade-in">', unsafe_allow_html=True)
    st.error("⚠️ You are not logged in. Redirecting to login page...")
    st.markdown('</div>', unsafe_allow_html=True)
    with st.spinner("Redirecting..."):
        time.sleep(2)
    st.switch_page("app.py")
    st.stop()

# Main redirect page
st.markdown('<div class="fade-in">', unsafe_allow_html=True)

col1, col2 = st.columns([1, 2])

with col1:
    st_lottie(redirect_animation, height=150, key="redirect")

with col2:
    st.title("🔄 Redirecting to Your Dashboard")
    st.markdown("""
    <div style='font-size:16px; margin-bottom:20px;'>
        Please wait while we set up your personalized dashboard...
    </div>
    """, unsafe_allow_html=True)

user = st.session_state.user
role = user["role"]

# Progress bar for redirect
progress_bar = st.progress(0)
for i in range(100):
    progress_bar.progress(i + 1)
    time.sleep(0.01)

st.success(f"🎯 Welcome, {user['name']}! Redirecting to {role.capitalize()} Dashboard...")

# Redirect based on role
if role == "admin":
    st.switch_page("pages/1_Admin_Dashboard.py")
elif role == "teacher":
    st.switch_page("pages/2_Teacher_Dashboard.py")
elif role == "student":
    st.switch_page("pages/3_Student_Dashboard.py")
else:
    st.error("❌ Unknown role. Please contact the administrator.")

st.markdown('</div>', unsafe_allow_html=True)
