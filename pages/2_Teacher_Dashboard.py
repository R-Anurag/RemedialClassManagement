import streamlit as st
from utils.db_ops import (
    get_all_remedial_classes, get_all_subjects, get_attendance_for_class,
    mark_attendance, get_all_students, record_performance, get_performance_by_student
)
from utils.theme import apply_theme
from datetime import date
import pandas as pd
import plotly.express as px
from streamlit_lottie import st_lottie
import requests
import json

st.set_page_config(page_title="Teacher Dashboard", layout="wide", page_icon="🏫")

# Apply theme
apply_theme()

# Load Lottie animation
def load_lottieurl(url: str):
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None

teacher_animation = load_lottieurl("https://assets4.lottiefiles.com/packages/lf20_0yfsb3ma.json")  # Teacher animation

# Redirect to login if user not authenticated
if "user" not in st.session_state or st.session_state.user is None:
    st.warning("🔒 You must be logged in to view this page.")
    st.stop()

st.markdown('<div class="fade-in">', unsafe_allow_html=True)

col1, col2 = st.columns([1, 3])

with col1:
    if teacher_animation:
        st_lottie(teacher_animation, height=100, key="teacher")
    else:
        st.markdown("👩‍🏫", unsafe_allow_html=True)

with col2:
    st.title("📘 Teacher Dashboard")
    st.markdown(
        """
        <div class='fade-in' style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 1rem; border-radius: 15px; color: white; box-shadow: 0 4px 15px rgba(0,0,0,0.1);'>
            <h4 style='margin: 0;'>Welcome Teacher! 👋</h4>
            <p style='margin: 0.5rem 0 0 0;'>Manage attendance and performance for your remedial classes with ease.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

user = st.session_state.user
teacher_id = user["user_id"]

# Fetch all remedial classes and subjects
classes = get_all_remedial_classes()
subjects = {s[0]: s[1] for s in get_all_subjects()}

# Filter only teacher's classes
teacher_classes = [c for c in classes if c[2] == teacher_id]

st.subheader("📅 My Remedial Classes")

if teacher_classes:
    class_map = {f"{subjects[c[1]]} on {c[3]} at {c[4]} (Room {c[5]})": c[0] for c in teacher_classes}
    selected_class_label = st.selectbox("Select a Class to Manage", options=list(class_map.keys()))
    selected_class_id = class_map[selected_class_label]

    tabs = st.tabs(["📋 Attendance", "📈 Performance", "🗂️ Attendance Records", "📊 Visual Insights"])

    # ------------ ATTENDANCE TAB ------------
    with tabs[0]:
        st.markdown('<div class="slide-in">', unsafe_allow_html=True)
        st.markdown("<div style='background-color:#FFEBF0; padding:1rem; border-radius:10px;'>Mark attendance for this class</div>", unsafe_allow_html=True)
        students = get_all_students()
        student_map = {f"{s[1]} ({s[0]})": s[0] for s in students}

        with st.form("attendance_form"):
            date_today = st.date_input("Date", value=date.today())
            attendance_data = {}

            for name, sid in student_map.items():
                status = st.radio(f"{name}", ["present", "absent"], horizontal=True, key=f"att_{sid}")
                attendance_data[sid] = status

            if st.form_submit_button("✅ Submit Attendance"):
                with st.spinner("Recording attendance..."):
                    for sid, status in attendance_data.items():
                        mark_attendance(selected_class_id, sid, status, str(date_today))
                st.success("✅ Attendance recorded successfully!")
                st.balloons()
        st.markdown('</div>', unsafe_allow_html=True)

    # ------------ PERFORMANCE TAB ------------
    with tabs[1]:
        st.markdown('<div class="slide-in">', unsafe_allow_html=True)
        st.markdown("<div style='background-color:#E4F2F1; padding:1rem; border-radius:10px;'>Record student performance before and after remedial class</div>", unsafe_allow_html=True)
        with st.form("performance_form"):
            selected_student_name = st.selectbox("Student", list(student_map.keys()))
            student_id = student_map[selected_student_name]
            col1, col2 = st.columns(2)
            with col1:
                score_before = st.slider("Score Before", 0, 100, value=50)
            with col2:
                score_after = st.slider("Score After", 0, 100, value=70)
            perf_date = st.date_input("Date", value=date.today(), key="perf")
            submitted = st.form_submit_button("📊 Record Performance")

            if submitted:
                with st.spinner("Recording performance..."):
                    subject_id = [c[1] for c in teacher_classes if c[0] == selected_class_id][0]
                    record_performance(student_id, subject_id, score_before, score_after, str(perf_date))
                st.success("✅ Performance data recorded successfully!")
                st.balloons()
        st.markdown('</div>', unsafe_allow_html=True)

    # ------------ ATTENDANCE RECORDS TAB ------------
    with tabs[2]:
        st.markdown('<div class="slide-in">', unsafe_allow_html=True)
        st.markdown("<div style='background-color:#FDF6F0; padding:1rem; border-radius:10px;'>All attendance records for this class</div>", unsafe_allow_html=True)
        records = get_attendance_for_class(selected_class_id)
        if records:
            # Make sure columns match returned tuples
            sample_len = len(records[0])
            if sample_len == 5:
                columns = ["ID", "ClassID", "StudentID", "Status", "Date"]
            elif sample_len == 4:
                columns = ["ClassID", "StudentID", "Status", "Date"]
            else:
                columns = [f"col_{i}" for i in range(sample_len)]

            att_df = pd.DataFrame(records, columns=columns)
            st.dataframe(att_df, height=300)
        else:
            st.warning("⚠️ No attendance records found for this class")
        st.markdown('</div>', unsafe_allow_html=True)

    # ------------ VISUAL INSIGHTS TAB ------------
    with tabs[3]:
        st.markdown('<div class="slide-in">', unsafe_allow_html=True)
        st.markdown("<div style='background-color:#F4F4FC; padding:1rem; border-radius:10px;'>Visual analysis of attendance and performance</div>", unsafe_allow_html=True)

        # ATTENDANCE CHART
        att_data = get_attendance_for_class(selected_class_id)
        if att_data:
            sample_len = len(att_data[0])
            if sample_len == 5:
                att_df = pd.DataFrame(att_data, columns=["ID", "ClassID", "StudentID", "Status", "Date"])
            elif sample_len == 4:
                att_df = pd.DataFrame(att_data, columns=["ClassID", "StudentID", "Status", "Date"])
            else:
                att_df = pd.DataFrame(att_data)

            att_summary = att_df["Status"].value_counts().reset_index(name="Count").rename(columns={"index": "Status"})
            chart_att = px.pie(att_summary, names="Status", values="Count",
                               color_discrete_sequence=["#FFB6B9", "#A3D2CA"],
                               title="Attendance Distribution")
            st.plotly_chart(chart_att)
        else:
            st.info("📊 No attendance data available for charts.")

        # PERFORMANCE CHART
        # NOTE: You probably want to call performance by student, not by class
        performance_rows = []
        for s_id in student_map.values():
            perf = get_performance_by_student(s_id)
            if perf:
                performance_rows.extend(perf)

        if performance_rows:
            perf_df = pd.DataFrame(performance_rows, columns=["ID", "StudentID", "SubjectID", "Before", "After", "Date"])
            chart_perf = px.bar(perf_df, x="StudentID", y=["Before", "After"],
                                barmode="group",
                                color_discrete_map={"Before": "#FFB6B9", "After": "#A3D2CA"},
                                title="Performance Before vs After")
            st.plotly_chart(chart_perf)
        else:
            st.info("📊 No performance data available for charts.")
        st.markdown('</div>', unsafe_allow_html=True)

else:
    st.warning("⚠️ No remedial classes assigned to you.")
    st.markdown('</div>', unsafe_allow_html=True)
