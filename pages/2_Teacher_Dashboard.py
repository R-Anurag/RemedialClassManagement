import streamlit as st
from utils.db_ops import (
    get_all_remedial_classes, get_all_subjects, get_attendance_for_class,
    mark_attendance, get_all_students, record_performance, get_performance_by_student
)
from datetime import date

st.set_page_config(page_title="Teacher Dashboard", layout="wide")
st.title("📘 Teacher Dashboard")

user = st.session_state.user
teacher_id = user["user_id"]

# Fetch all remedial classes (in production you'd filter by teacher_id)
classes = get_all_remedial_classes()
subjects = {s[0]: s[1] for s in get_all_subjects()}

# Filter only teacher's classes
teacher_classes = [c for c in classes if c[2] == teacher_id]

st.subheader("📅 My Remedial Classes")
if teacher_classes:
    class_map = {f"{subjects[c[1]]} on {c[3]} at {c[4]} (Room {c[5]})": c[0] for c in teacher_classes}
    selected_class_label = st.selectbox("Select a Class to Manage", options=list(class_map.keys()))
    selected_class_id = class_map[selected_class_label]

    tabs = st.tabs(["📋 Attendance", "📈 Performance", "🗂️ Attendance Records"])

    # ------------ ATTENDANCE TAB ------------
    with tabs[0]:
        st.info("Mark attendance for this class")
        students = get_all_students()
        student_map = {f"{s[1]} ({s[0]})": s[0] for s in students}

        with st.form("attendance_form"):
            date_today = st.date_input("Date", value=date.today())
            attendance_data = {}

            for name, sid in student_map.items():
                status = st.radio(f"{name}", ["present", "absent"], horizontal=True, key=sid)
                attendance_data[sid] = status

            if st.form_submit_button("Submit Attendance"):
                for sid, status in attendance_data.items():
                    mark_attendance(selected_class_id, sid, status, str(date_today))
                st.success("Attendance recorded")

    # ------------ PERFORMANCE TAB ------------
    with tabs[1]:
        st.info("Record student performance before and after remedial class")
        with st.form("performance_form"):
            selected_student_name = st.selectbox("Student", list(student_map.keys()))
            student_id = student_map[selected_student_name]
            score_before = st.slider("Score Before", 0, 100)
            score_after = st.slider("Score After", 0, 100)
            perf_date = st.date_input("Date", value=date.today(), key="perf")
            submitted = st.form_submit_button("Record Performance")

            if submitted:
                subject_id = [c[1] for c in teacher_classes if c[0] == selected_class_id][0]
                record_performance(student_id, subject_id, score_before, score_after, str(perf_date))
                st.success("Performance data recorded")

    # ------------ ATTENDANCE RECORDS TAB ------------
    with tabs[2]:
        st.info("View all attendance records for this class")
        records = get_attendance_for_class(selected_class_id)
        if records:
            st.dataframe(records, use_container_width=True)
        else:
            st.warning("No attendance records found for this class")
else:
    st.warning("No remedial classes assigned to you.")
