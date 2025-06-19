import streamlit as st
from utils.db_ops import (
    add_student, get_all_students,
    add_teacher, get_all_teachers,
    add_subject, get_all_subjects,
    add_remedial_class, get_all_remedial_classes
)

st.set_page_config(page_title="Admin Dashboard", layout="wide")
st.title("🛠️ Admin Dashboard")

# Tabs for managing entities
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
    st.dataframe(students, use_container_width=True)

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
    st.dataframe(teachers, use_container_width=True)

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
    st.dataframe(subjects, use_container_width=True)

# ------------------------ REMEDIAL CLASSES ------------------------
with tabs[3]:
    st.header("🏫 Schedule Remedial Classes")

    # Dynamic dropdowns
    subject_options = get_all_subjects()
    teacher_options = get_all_teachers()

    with st.form("add_class_form"):
        subject_id = st.selectbox("Subject", options=[(s[0], s[1]) for s in subject_options], format_func=lambda x: x[1])[0]
        teacher_id = st.selectbox("Teacher", options=[(t[0], t[1]) for t in teacher_options], format_func=lambda x: x[1])[0]
        date = st.date_input("Date")
        time = st.time_input("Time")
        room = st.text_input("Room")
        submitted = st.form_submit_button("Schedule Class")
        if submitted:
            add_remedial_class(subject_id, teacher_id, str(date), str(time), room)
            st.success("Class scheduled successfully")

    st.subheader("📋 All Scheduled Classes")
    classes = get_all_remedial_classes()
    st.dataframe(classes, use_container_width=True)
