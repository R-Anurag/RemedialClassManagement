import streamlit as st
import time

# --- Session Guard ---
if "user" not in st.session_state or st.session_state.user is None:
    st.warning("⚠️ You are not logged in. Redirecting to login page...")
    st.switch_page("")
    st.stop()  # Prevent further execution

st.set_page_config(page_title="Home", layout="centered")
st.title("🔐 Welcome to Remedial Class Manager")

user = st.session_state.user
role = user["role"]

# Simulate short delay before redirect
with st.spinner("Redirecting to your dashboard..."):
    time.sleep(1)

# Redirect based on role
if role == "admin":
    st.switch_page("pages/1_Admin_Dashboard.py")
elif role == "teacher":
    st.switch_page("pages/2_Teacher_Dashboard.py")
elif role == "student":
    st.switch_page("pages/3_Student_Dashboard.py")
else:
    st.error("Unknown role. Please contact the administrator.")
