import streamlit as st
import pandas as pd
import plotly.express as px
from utils.db_ops import (
    get_all_remedial_classes, get_performance_by_student,
    get_attendance_for_student, add_feedback, get_all_subjects
)
from datetime import date
import streamlit_calendar as st_cal
from fpdf import FPDF
import io
from utils.db_ops import export_student_data

st.markdown("""
<style>
.stDownloadButton>button {
    background-color: #b197fc; /* light purple background */
    color: white;
    font-weight: 600;
    font-size: 18px;
    border: none;
    border-radius: 50px; /* rounded capsule */
    padding: 0.6rem 1.8rem;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 10px;
    transition: all 0.4s ease-in-out;
    box-shadow: 0 4px 10px rgba(177, 151, 252, 0.4);
}

/* Hover effect (brighter button) */
.stDownloadButton>button:hover {
    background-color: #c7aefc;
    transform: translateY(-2px);
    box-shadow: 0 6px 15px rgba(177, 151, 252, 0.6);
}

/* On click / active state: change icon and glow */
.stDownloadButton>button:active::after {
    background-color: #ff85c1;
    transform: scale(1.1);
}

/* Focus outline for accessibility */
.stDownloadButton>button:focus {
    outline: 2px solid #ff63b1;
    outline-offset: 3px;
}
</style>
""", unsafe_allow_html=True)





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
        
        perf_df = pd.DataFrame(columns=["Subject", "Before", "After", "Date"])

    st.markdown("<p style='color:#333; font-size:17px; font-weight:500;'>Preview your performance before download</p>",
                unsafe_allow_html=True)

    with st.expander("Preview Performance Data"):
        st.dataframe(perf_df, use_container_width=True)

    col1, col2 = st.columns([4, 1])
    with col2:
        csv_perf = perf_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download",
            data=csv_perf,
            file_name=f"performance_student_{student_id}.csv",
            mime="text/csv",
            key="perf_csv",
            use_container_width=True
        )



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
            st.markdown("<p style='color:#333; font-size:17px; font-weight:500;'>Preview your attendance before download</p>", unsafe_allow_html=True)
            with st.expander("Preview Attendance Data"):
                st.dataframe(att_df[["Date", "Subject", "Status"]], use_container_width=True)

            col3, col4 = st.columns([4, 1])
            with col4:
                csv_att = att_df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="Download",
                    data=csv_att,
                    file_name=f"attendance_student_{student_id}.csv",
                    mime="text/csv",
                    key="att_csv",
                    use_container_width=True
                )
        except Exception:
            st.warning("⚠️ Attendance data format issue. Please check the backend.")
    else:
        st.info("No attendance records available.")
        
        att_df = pd.DataFrame(columns=["Date", "Subject", "Status"])

    st.markdown("<p style='color:#333; font-size:17px; font-weight:500;'>Preview your attendance before download</p>",
                unsafe_allow_html=True)

    with st.expander("Preview Attendance Data"):
        st.dataframe(att_df, use_container_width=True)

    col3, col4 = st.columns([4, 1])
    with col4:
        csv_att = att_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download",
            data=csv_att,
            file_name=f"attendance_student_{student_id}.csv",
            mime="text/csv",
            key="att_csv",
            use_container_width=True
        )
        
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
                
# ----------------- FULL REPORT DOWNLOAD SECTION-----------------
st.markdown("<hr>", unsafe_allow_html=True)
st.subheader("📤 Download My Progress Report")
st.markdown("<p style='color:#333; font-size:17px; font-weight:500;'>Preview full report (Attendance + Performance)</p>", unsafe_allow_html=True)

def create_pdf(att_df, perf_df):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Student Progress Report", ln=True, align="C")
    pdf.cell(200, 10, txt="", ln=True)

    pdf.cell(200, 10, txt="Attendance Records:", ln=True)
    if not att_df.empty:
        for _, row in att_df.iterrows():
            pdf.cell(200, 8, txt=f"{row['Date']} - {row['Subject']} - {row['Status']}", ln=True)
    else:
        pdf.cell(200, 8, txt="No attendance records available.", ln=True)

    pdf.cell(200, 10, txt="", ln=True)

    pdf.cell(200, 10, txt="Performance Records:", ln=True)
    if not perf_df.empty:
        for _, row in perf_df.iterrows():
            pdf.cell(200, 8, txt=f"{row['Subject']}: Before={row['Before']}, After={row['After']}", ln=True)
    else:
        pdf.cell(200, 8, txt="No performance records available.", ln=True)

    pdf_output = pdf.output(dest="S").encode("latin1")
    return io.BytesIO(pdf_output)

pdf_buffer = create_pdf(att_df, perf_df)

with st.expander("Preview Combined Report"):
    st.write("**Attendance Data:**")
    st.dataframe(att_df, use_container_width=True)

    st.write("**Performance Data:**")
    st.dataframe(perf_df, use_container_width=True)

col5, col6 = st.columns([4, 1])
with col6:
    st.download_button(
        label="Download",
        data=pdf_buffer,
        file_name=f"student_report_{student_id}.pdf",
        mime="application/pdf",
        key="pdf_report",
        use_container_width=True
    )
                
            
