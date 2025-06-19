import streamlit as st
from utils.db_ops import (
    add_student, get_all_students,
    add_teacher, get_all_teachers,
    add_subject, get_all_subjects,
    add_remedial_class, get_all_remedial_classes
)

import streamlit as st

# Redirect to login if user not authenticated
if "user" not in st.session_state or st.session_state.user is None:
    st.warning("🔒 You must be logged in to view this page.")
    st.stop()  # Prevent the rest of the page from running

st.set_page_config(page_title="Admin Dashboard", layout="wide", page_icon="🏫")
st.title("🛠️ Admin Dashboard")

tabs = st.tabs(["Students", "Teachers", "Subjects", "Remedial Classes"])

# ------------------------ STUDENTS ------------------------
with tabs[0]:
    st.header("👨‍🎓 Manage Students")

    with st.form("add_student_form"):
        name = st.text_input("Name")
        email = st.text_input("Email")
        phone = st.text_input("Phone")
        course = st.text_input("Course")
        year = st.number_input("Year", min_value=1, max_value=5, step=1)
        submitted = st.form_submit_button("Add Student")
        if submitted:
            add_student(name, email, phone, course, year)
            st.success("Student added successfully")

    st.subheader("📋 All Students")
    students = get_all_students()
    if students:
        st.dataframe(students, use_container_width=True)
    else:
        st.info("No students found.")

# ------------------------ TEACHERS ------------------------
with tabs[1]:
    st.header("👩‍🏫 Manage Teachers")

    with st.form("add_teacher_form"):
        name = st.text_input("Teacher Name")
        email = st.text_input("Teacher Email")
        phone = st.text_input("Teacher Phone")
        subject = st.text_input("Subject Specialty")
        submitted = st.form_submit_button("Add Teacher")
        if submitted:
            add_teacher(name, email, phone, subject)
            st.success("Teacher added successfully")

    st.subheader("📋 All Teachers")
    teachers = get_all_teachers()
    if teachers:
        st.dataframe(teachers, use_container_width=True)
    else:
        st.info("No teachers found.")

# ------------------------ SUBJECTS ------------------------
with tabs[2]:
    st.header("📚 Manage Subjects")

    with st.form("add_subject_form"):
        name = st.text_input("Subject Name")
        dept = st.text_input("Department")
        submitted = st.form_submit_button("Add Subject")
        if submitted:
            add_subject(name, dept)
            st.success("Subject added successfully")

    st.subheader("📋 All Subjects")
    subjects = get_all_subjects()
    if subjects:
        st.dataframe(subjects, use_container_width=True)
    else:
        st.info("No subjects found.")

# ------------------------ REMEDIAL CLASSES ------------------------
with tabs[3]:
    st.header("🏫 Schedule Remedial Classes")

    subject_options = get_all_subjects()
    teacher_options = get_all_teachers()

    if not subject_options or not teacher_options:
        st.warning("Please make sure both subjects and teachers are added before scheduling a class.")
    else:
        with st.form("add_class_form"):
            selected_subject = st.selectbox("Subject", options=subject_options, format_func=lambda s: s[1])
            selected_teacher = st.selectbox("Teacher", options=teacher_options, format_func=lambda t: t[1])
            date = st.date_input("Date")
            time = st.time_input("Time")
            room = st.text_input("Room")
            submitted = st.form_submit_button("Schedule Class")
            if submitted:
                subject_id = selected_subject[0]
                teacher_id = selected_teacher[0]
                add_remedial_class(subject_id, teacher_id, str(date), str(time), room)
                st.success("Class scheduled successfully")

    st.subheader("📋 All Scheduled Classes")
    classes = get_all_remedial_classes()
    if classes:
        st.dataframe(classes, use_container_width=True)
    else:
        st.info("No remedial classes scheduled yet.")
