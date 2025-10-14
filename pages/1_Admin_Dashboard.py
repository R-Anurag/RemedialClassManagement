import streamlit as st
from utils.db_ops import (
    add_student, get_all_students,
    add_teacher, get_all_teachers,
    add_subject, get_all_subjects,
    add_remedial_class, get_all_remedial_classes
)
from utils.theme import apply_theme
from streamlit_lottie import st_lottie
import requests

st.set_page_config(page_title="Admin Dashboard", layout="wide", page_icon="🏫")

# Apply theme
apply_theme()

# Load Lottie animation
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

admin_animation = load_lottieurl("https://assets3.lottiefiles.com/packages/lf20_qp1q7mct.json")  # Admin/dashboard animation

# Redirect to login if user not authenticated
if "user" not in st.session_state or st.session_state.user is None:
    st.warning("🔒 You must be logged in to view this page.")
    st.stop()

st.markdown('<div class="fade-in">', unsafe_allow_html=True)

col1, col2 = st.columns([1, 3])

with col1:
    st_lottie(admin_animation, height=100, key="admin")

with col2:
    st.title("🛠️ Admin Dashboard")
    st.markdown(
        """
        <div class='fade-in' style='background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%); padding: 1rem; border-radius: 15px; color: #333; box-shadow: 0 4px 15px rgba(0,0,0,0.1);'>
            <h4 style='margin: 0;'>Welcome Admin! 👋</h4>
            <p style='margin: 0.5rem 0 0 0;'>Manage students, teachers, subjects, and remedial classes.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

tabs = st.tabs(["👨‍🎓 Students", "👩‍🏫 Teachers", "📚 Subjects", "🏫 Remedial Classes"])

# ------------------------ STUDENTS ------------------------
with tabs[0]:
    st.markdown('<div class="slide-in">', unsafe_allow_html=True)
    st.header("👨‍🎓 Manage Students")

    with st.form("add_student_form"):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Name", placeholder="Student's full name")
            email = st.text_input("Email", placeholder="student@example.com")
        with col2:
            phone = st.text_input("Phone", placeholder="Phone number")
            course = st.text_input("Course", placeholder="Course name")
        year = st.number_input("Year", min_value=1, max_value=5, step=1, value=1)
        submitted = st.form_submit_button("➕ Add Student")
        if submitted:
            with st.spinner("Adding student..."):
                add_student(name, email, phone, course, year)
            st.success("✅ Student added successfully!")
            st.balloons()

    st.subheader("📋 All Students")
    students = get_all_students()
    if students:
        st.dataframe(students, height=300)
    else:
        st.info("📝 No students found. Add some students to get started!")
    st.markdown('</div>', unsafe_allow_html=True)

# ------------------------ TEACHERS ------------------------
with tabs[1]:
    st.markdown('<div class="slide-in">', unsafe_allow_html=True)
    st.header("👩‍🏫 Manage Teachers")

    with st.form("add_teacher_form"):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Teacher Name", placeholder="Teacher's full name")
            email = st.text_input("Teacher Email", placeholder="teacher@example.com")
        with col2:
            phone = st.text_input("Teacher Phone", placeholder="Phone number")
            subject = st.text_input("Subject Specialty", placeholder="e.g., Mathematics")
        submitted = st.form_submit_button("➕ Add Teacher")
        if submitted:
            with st.spinner("Adding teacher..."):
                add_teacher(name, email, phone, subject)
            st.success("✅ Teacher added successfully!")
            st.balloons()

    st.subheader("📋 All Teachers")
    teachers = get_all_teachers()
    if teachers:
        st.dataframe(teachers, height=300)
    else:
        st.info("📝 No teachers found. Add some teachers to get started!")
    st.markdown('</div>', unsafe_allow_html=True)

# ------------------------ SUBJECTS ------------------------
with tabs[2]:
    st.markdown('<div class="slide-in">', unsafe_allow_html=True)
    st.header("📚 Manage Subjects")

    with st.form("add_subject_form"):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Subject Name", placeholder="e.g., Algebra")
        with col2:
            dept = st.text_input("Department", placeholder="e.g., Mathematics")
        submitted = st.form_submit_button("➕ Add Subject")
        if submitted:
            with st.spinner("Adding subject..."):
                add_subject(name, dept)
            st.success("✅ Subject added successfully!")
            st.balloons()

    st.subheader("📋 All Subjects")
    subjects = get_all_subjects()
    if subjects:
        st.dataframe(subjects, height=300)
    else:
        st.info("📝 No subjects found. Add some subjects to get started!")
    st.markdown('</div>', unsafe_allow_html=True)

# ------------------------ REMEDIAL CLASSES ------------------------
with tabs[3]:
    st.markdown('<div class="slide-in">', unsafe_allow_html=True)
    st.header("🏫 Schedule Remedial Classes")

    subject_options = get_all_subjects()
    teacher_options = get_all_teachers()

    if not subject_options or not teacher_options:
        st.warning("⚠️ Please make sure both subjects and teachers are added before scheduling a class.")
    else:
        with st.form("add_class_form"):
            col1, col2 = st.columns(2)
            with col1:
                selected_subject = st.selectbox("Subject", options=subject_options, format_func=lambda s: s[1])
                selected_teacher = st.selectbox("Teacher", options=teacher_options, format_func=lambda t: t[1])
            with col2:
                date = st.date_input("Date")
                time = st.time_input("Time")
            room = st.text_input("Room", placeholder="e.g., Room 101")
            submitted = st.form_submit_button("📅 Schedule Class")
            if submitted:
                with st.spinner("Scheduling class..."):
                    subject_id = selected_subject[0]
                    teacher_id = selected_teacher[0]
                    add_remedial_class(subject_id, teacher_id, str(date), str(time), room)
                st.success("✅ Class scheduled successfully!")
                st.balloons()

    st.subheader("📋 All Scheduled Classes")
    classes = get_all_remedial_classes()
    if classes:
        st.dataframe(classes, height=300)
    else:
        st.info("📝 No remedial classes scheduled yet. Schedule your first class!")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
