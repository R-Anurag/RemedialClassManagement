import streamlit as st
import pandas as pd
import plotly.express as px
from utils.db_ops import (
    get_all_remedial_classes, get_performance_by_student,
    get_attendance_for_student, add_feedback, get_all_subjects
)
from datetime import date
import streamlit_calendar as st_cal

st.set_page_config(page_title="Student Dashboard", layout="wide", page_icon="🏫")

# Redirect to login if user not authenticated
if "user" not in st.session_state or st.session_state.user is None:
    st.warning("🔒 You must be logged in to view this page.")
    st.stop()

# ----------------- HEADER -----------------
st.title("🎓 Student Dashboard")
user = st.session_state.user
student_id = user["user_id"]

st.markdown(
    f"""
    <div style='background-color:#FFE0E9; padding: 1rem; border-radius: 10px;'>
        <h4 style='color:#444;'>Welcome back, <em>{user['name']}</em>! Here's a quick look at your classes, progress, and attendance.</h4>
    </div>
    """,
    unsafe_allow_html=True
)

# ----------------- DATA LOADING -----------------
classes = get_all_remedial_classes()
subjects = {s[0]: s[1] for s in get_all_subjects()}

# ----------------- UPCOMING CLASSES -----------------
with st.container():
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
        st.info("No upcoming classes scheduled.")

# ----------------- PERFORMANCE CHART -----------------
with st.container():
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

            st.plotly_chart(chart, use_container_width=True)
        except Exception as e:
            st.error(f"Error displaying performance chart. {e}")
    else:
        st.info("No performance data available.")



# ----------------- ATTENDANCE -----------------
with st.container():
    st.subheader("🗂️ My Attendance Record")
    att = get_attendance_for_student(student_id)
    if att:
        try:
            att_df = pd.DataFrame(att, columns=["ID", "ClassID", "StudentID", "Status", "Date", "Subject"])
            attendance_rate = att_df["Status"].value_counts(normalize=True) * 100
            st.metric("Attendance Rate", f"{attendance_rate.get('present', 0):.1f}% Present")
            st.dataframe(
                att_df[["Date", "Subject", "Status"]].sort_values("Date"),
                use_container_width=True
            )
        except Exception:
            st.warning("⚠️ Attendance data format issue. Please check the backend.")
    else:
        st.info("No attendance records available.")


# ----------------- FEEDBACK -----------------
with st.container():
    st.subheader("💬 Submit Feedback")
    with st.form("feedback_form"):
        subject = st.selectbox("Subject", list(subjects.values()))
        feedback = st.text_area("Your Feedback", max_chars=500)
        rating = st.slider("Rate the class (1 = poor, 5 = excellent)", 1, 5, 3)
        submitted = st.form_submit_button("Submit Feedback")

        if submitted:
            subject_ids = [k for k, v in subjects.items() if v == subject]
            if subject_ids:
                subject_id = subject_ids[0]
                if not feedback.strip():
                    st.error("Please enter some feedback before submitting.")
                else:
                    try:
                        add_feedback(subject_id, student_id, feedback, rating)
                        st.success("Thank you for your feedback!")
                    except Exception as e:
                        st.error(f"Failed to submit feedback: {e}")
            else:
                st.error("Subject not found. Please try again.")

