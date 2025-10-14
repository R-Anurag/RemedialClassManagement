import streamlit as st
import pandas as pd
import plotly.express as px
from utils.db_ops import (
    get_all_remedial_classes, get_performance_by_student,
    get_attendance_for_student, add_feedback, get_all_subjects
)
from utils.theme import apply_theme
from datetime import date
import streamlit_calendar as st_cal
from streamlit_lottie import st_lottie
import requests

st.set_page_config(page_title="Student Dashboard", layout="wide", page_icon="🏫")

# Apply theme
apply_theme()

# Load Lottie animation
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

student_animation = load_lottieurl("https://assets9.lottiefiles.com/packages/lf20_1pxqjqps.json")  # Student animation

# Redirect to login if user not authenticated
if "user" not in st.session_state or st.session_state.user is None:
    st.warning("🔒 You must be logged in to view this page.")
    st.stop()

st.markdown('<div class="fade-in">', unsafe_allow_html=True)

col1, col2 = st.columns([1, 3])

with col1:
    st_lottie(student_animation, height=100, key="student")

with col2:
    st.title("🎓 Student Dashboard")
    user = st.session_state.user
    student_id = user["user_id"]

    st.markdown(
        f"""
        <div class='fade-in' style='background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%); padding: 1rem; border-radius: 15px; color: white; box-shadow: 0 4px 15px rgba(0,0,0,0.1);'>
            <h4 style='margin: 0;'>Welcome back, {user['name']}! 👋</h4>
            <p style='margin: 0.5rem 0 0 0;'>Here's a quick look at your classes, progress, and attendance.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

# ----------------- DATA LOADING -----------------
classes = get_all_remedial_classes()
subjects = {s[0]: s[1] for s in get_all_subjects()}

# ----------------- UPCOMING CLASSES -----------------
with st.container():
    st.markdown('<div class="slide-in">', unsafe_allow_html=True)
    st.subheader("📅 Upcoming Remedial Classes")
    today = date.today()
    upcoming = [c for c in classes if c[3] >= str(today)]

    if upcoming:
        events = []
        for c in upcoming:
            subject = subjects.get(c[1], "Unknown")
            events.append({
                "title": f"{subject} ({c[4]})",
                "start": f"{c[3]}T{c[4]}",
                "end": f"{c[3]}T{c[4]}",
                "location": f"Room {c[5]}"
            })

        st_cal.calendar(events=events, options={"initialView": "dayGridMonth"})
    else:
        st.info("📅 No upcoming classes scheduled.")
    st.markdown('</div>', unsafe_allow_html=True)

# ----------------- PERFORMANCE CHART -----------------
with st.container():
    st.markdown('<div class="slide-in">', unsafe_allow_html=True)
    st.subheader("📈 My Performance")
    perf = get_performance_by_student(student_id)
    if perf:
        try:
            # Load into DataFrame
            perf_df = pd.DataFrame(perf, columns=["ID", "StudentID", "SubjectID", "Before", "After", "Date"])
            perf_df["Date"] = pd.to_datetime(perf_df["Date"])  # Ensure datetime
            perf_df["Subject"] = perf_df["SubjectID"].map(subjects)

            # Melt to long format for line chart
            long_df = pd.melt(
                perf_df,
                id_vars=["Date", "Subject"],
                value_vars=["Before", "After"],
                var_name="Test Type",
                value_name="Score"
            )

            # Plot with lines and markers
            chart = px.line(
                long_df,
                x="Date",
                y="Score",
                color="Test Type",
                markers=True,
                line_shape="linear",
                labels={"Score": "Score", "Date": "Date"},
                title="Performance Before vs After Remedial Classes"
            )

            st.plotly_chart(chart)
        except Exception as e:
            st.error(f"❌ Error displaying performance chart. {e}")
    else:
        st.info("📊 No performance data available.")
    st.markdown('</div>', unsafe_allow_html=True)



# ----------------- ATTENDANCE -----------------
with st.container():
    st.markdown('<div class="slide-in">', unsafe_allow_html=True)
    st.subheader("🗂️ My Attendance Record")
    att = get_attendance_for_student(student_id)
    if att:
        try:
            att_df = pd.DataFrame(att, columns=["ID", "ClassID", "StudentID", "Status", "Date", "Subject"])
            attendance_rate = att_df["Status"].value_counts(normalize=True) * 100
            st.metric("📊 Attendance Rate", f"{attendance_rate.get('present', 0):.1f}% Present")
            st.dataframe(
                att_df[["Date", "Subject", "Status"]].sort_values("Date"),
                height=300
            )
        except Exception:
            st.warning("⚠️ Attendance data format issue. Please check the backend.")
    else:
        st.info("📝 No attendance records available.")
    st.markdown('</div>', unsafe_allow_html=True)


# ----------------- FEEDBACK -----------------
with st.container():
    st.markdown('<div class="slide-in">', unsafe_allow_html=True)
    st.subheader("💬 Submit Feedback")
    with st.form("feedback_form"):
        subject = st.selectbox("Subject", list(subjects.values()))
        feedback = st.text_area("Your Feedback", max_chars=500, placeholder="Share your thoughts about the class...")
        rating = st.slider("Rate the class (1 = poor, 5 = excellent)", 1, 5, 3)
        submitted = st.form_submit_button("📝 Submit Feedback")

        if submitted:
            subject_ids = [k for k, v in subjects.items() if v == subject]
            if subject_ids:
                subject_id = subject_ids[0]
                if not feedback.strip():
                    st.error("❌ Please enter some feedback before submitting.")
                else:
                    try:
                        with st.spinner("Submitting feedback..."):
                            add_feedback(subject_id, student_id, feedback, rating)
                        st.success("🎉 Thank you for your feedback!")
                        st.balloons()
                    except Exception as e:
                        st.error(f"❌ Failed to submit feedback: {e}")
            else:
                st.error("❌ Subject not found. Please try again.")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

