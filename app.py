# --- Streamlit for web app interface ---
import streamlit as st  # Used to build interactive web-based UI components

# --- Custom authentication utilities ---
from utils.auth import login_user, register_user, user_exists  # Functions for handling user authentication and registration

# --- Database handling ---
import sqlite3  # Built-in SQLite library for lightweight database management
from db_setup import init_database  # Custom function to initialize or set up the database schema

init_database()

st.set_page_config(page_title="Remedial Class Manager", layout="centered", page_icon="🏫" )
st.title("🔑 Welcome to Remedial Class Manager")


if "theme" not in st.session_state:
    st.session_state["theme"] = "light"

theme_choice = st.sidebar.toggle("🌙 Dark Mode", value=(st.session_state["theme"] == "dark"))
st.session_state["theme"] = "dark" if theme_choice else "light"

def apply_theme(theme):
    if theme == "dark":
        st.markdown("""
            <style>
                body, .stApp {
                    background-color: #0E1117 !important;
                    color: #E4E6EB !important;
                }

                h1, h2, h3, h4, h5, h6 {
                    color: #F1F3F5 !important;
                    font-weight: 600 !important;
                }

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

                input, textarea, select {
                    background-color: #1A1D26 !important;
                    color: #E4E6EB !important;
                    border: 1px solid #3A3A4A !important;
                    border-radius: 6px !important;
                }

                div[data-baseweb="slider"] > div {
                    background: linear-gradient(90deg, #8B5CF6, #6366F1);
                    height: 6px !important;
                    border-radius: 3px;
                }

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

                div[style*="background-color:#FFF1F4"],
                div[style*="background-color:#FFEBF0"],
                div[style*="background-color:#FDF6F0"],
                div[style*="background-color:#F4F4FC"],
                div[style*="background-color:#FFEFF1"],
                div[style*="background-color:#FFFFFF"] {
                    background-color: #1E1E2F !important;
                    color: #E4E6EB !important;
                }
                .stAlert, .stSuccess, .stWarning, .stInfo {
                    background-color: #1E1E2F !important;
                    color: #E4E6EB !important;
                    border: 1px solid #2C2C3A !important;
                }

                button[kind="secondary"],
                button[kind="primary"],
                .css-1emrehy {
                    color: #FFFFFF !important;
                    background: linear-gradient(90deg, #6366F1 0%, #8B5CF6 100%) !important;
                    border: none !important;
                }

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
# # Inject custom font with HTML and CSS
# st.markdown("""
#     <style>
#     @import url('https://fonts.googleapis.com/css2?family=Poppins&display=swap');

#     html, body, [class*="css"]  {
#         font-family: 'Poppins', sans-serif;
#     }
#     </style>
# """, unsafe_allow_html=True)


# --- Initialize session state ---
if "user" not in st.session_state:
    st.session_state.user = None

# --- Auth Mode Selector ---
auth_mode = st.sidebar.selectbox("Select Option", ["Login", "Register"])

# --- Login ---
if auth_mode == "Login":
    st.subheader("🔐 Login to Continue")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        user = login_user(username, password)  # Pass raw password
        if user:
            st.success(f"Welcome, {user.get('name', username)} ({user['role']})!")
            st.session_state.user = user
            st.switch_page("pages/0_Redirect.py")  # Fixed path
        else:
            st.error("Invalid credentials. Please try again.")

# --- Register ---
else:
    st.subheader("📝 Create New Account")
    name = st.text_input("Full Name")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    role = st.selectbox("Select Role", ["student", "teacher", "admin"])

    if st.button("Register"):
        if user_exists(username):
            st.warning("Username already exists. Try logging in instead.")
        else:
            success = register_user(name, username, password, role)
            if success:
                st.success("Registration successful! You can now log in.")
            else:
                st.error("Registration failed. Try a different username.")
