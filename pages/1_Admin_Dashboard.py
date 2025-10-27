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
def apply_theme(theme):
    if theme == "dark":
        st.markdown("""
            <style>
                /* ==== GENERAL LAYOUT ==== */
                body, .stApp {
                    background-color: #0E1117 !important;
                    color: #E4E6EB !important;
                }

                /* ==== HEADERS ==== */
                h1, h2, h3, h4, h5, h6 {
                    color: #F1F3F5 !important;
                    font-weight: 600 !important;
                }

                /* ==== SIDEBAR ==== */
                section[data-testid="stSidebar"] {
                    background: linear-gradient(180deg, #1E1E2F 0%, #161625 100%) !important;
                    color: #E4E6EB !important;
                    border-right: 1px solid #2C2C3A !important;
                }
                section[data-testid="stSidebar"] .css-1v3fvcr {
                    color: #E4E6EB !important;
                }
                section[data-testid="stSidebar"] .css-1v3fvcr:hover {
                    color: #A4B1FF !important;
                }

                /* ==== BUTTONS ==== */
                .stButton>button {
                    background: linear-gradient(90deg, #6366F1 0%, #8B5CF6 100%) !important;
                    color: #FFFFFF !important;
                    border: none !important;
                    border-radius: 8px !important;
                    font-weight: 600 !important;
                    transition: all 0.2s ease-in-out !important;
                }
                .stButton>button:hover {
                    transform: scale(1.03);
                    box-shadow: 0 0 15px rgba(139, 92, 246, 0.6);
                }

                /* ==== INPUT FIELDS ==== */
                input, textarea, select {
                    background-color: #1A1D26 !important;
                    color: #E4E6EB !important;
                    border: 1px solid #3A3A4A !important;
                    border-radius: 6px !important;
                }

                /* ==== SLIDERS ==== */
                div[data-baseweb="slider"] > div {
                    background: linear-gradient(90deg, #8B5CF6, #6366F1);
                    height: 6px !important;
                    border-radius: 3px;
                }

                /* ==== TABS ==== */
                .stTabs [role="tablist"] button {
                    background-color: #1E1E2F !important;
                    color: #E4E6EB !important;
                    border-radius: 8px 8px 0 0 !important;
                    font-weight: 500;
                }
                .stTabs [role="tablist"] button[aria-selected="true"] {
                    background-color: #292B3A !important;
                    color: #A5B4FC !important;
                    border-bottom: 3px solid #8B5CF6 !important;
                }

                /* ==== DATAFRAMES / TABLES ==== */
                .stDataFrame, .stTable {
                    background-color: #1A1D26 !important;
                    color: #F1F3F5 !important;
                    border-radius: 10px !important;
                }

                /* ==== EXPANDERS ==== */
                div[data-testid="stExpander"] {
                    background-color: #1A1D26 !important;
                    color: #F1F3F5 !important;
                    border-radius: 8px !important;
                    border: 1px solid #2C2C3A !important;
                }

                /* ==== DOWNLOAD BUTTON ==== */
                div[data-testid="stDownloadButton"] > button {
                    background: linear-gradient(90deg, #6366F1, #8B5CF6);
                    color: white !important;
                    border: none !important;
                    border-radius: 8px !important;
                    font-weight: 600;
                    transition: 0.3s;
                }
                div[data-testid="stDownloadButton"] > button:hover {
                    transform: scale(1.05);
                    box-shadow: 0 0 20px rgba(99, 102, 241, 0.5);
                }

                /* ==== FIX: PINK/LIGHT PANELS ==== */
                div[style*="background-color:#FFF1F4"],
                div[style*="background-color:#FFEBF0"],
                div[style*="background-color:#FDF6F0"],
                div[style*="background-color:#F4F4FC"],
                div[style*="background-color:#FFEFF1"],
                div[style*="background-color:#FFFFFF"] {
                    background-color: #1E1E2F !important;
                    color: #E4E6EB !important;
                }

                /* ==== ALERTS (success, warning, info) ==== */
                .stAlert, .stSuccess, .stWarning, .stInfo {
                    background-color: #1E1E2F !important;
                    color: #E4E6EB !important;
                    border: 1px solid #2C2C3A !important;
                }

                /* ==== FEEDBACK/FORM BUTTONS VISIBILITY ==== */
                button[kind="secondary"],
                button[kind="primary"],
                .css-1emrehy {
                    color: #FFFFFF !important;
                    background: linear-gradient(90deg, #6366F1 0%, #8B5CF6 100%) !important;
                    border: none !important;
                }

                /* ==== FIX EXPANDER/CONTAINER BG ==== */
                div[data-testid="stExpander"], .css-1dp5vir {
                    background-color: #1A1D26 !important;
                    color: #E4E6EB !important;
                    border: 1px solid #2C2C3A !important;
                }
            </style>
        """, unsafe_allow_html=True)

    else:
       pass
        
apply_theme(st.session_state["theme"])    
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
