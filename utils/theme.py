import streamlit as st

def apply_theme():
    # Initialize theme settings in session state
    if "dark_mode" not in st.session_state:
        st.session_state.dark_mode = False
    if "dark_theme" not in st.session_state:
        st.session_state.dark_theme = "Classic Dark"

    # Theme controls in sidebar
    st.sidebar.header("🎨 Theme Settings")
    dark_mode = st.sidebar.checkbox("🌙 Dark Mode", value=st.session_state.dark_mode)
    if dark_mode != st.session_state.dark_mode:
        st.session_state.dark_mode = dark_mode
        st.rerun()

    if st.session_state.dark_mode:
        theme_options = ["Ocean Blue", "Sunset Orange", "Forest Green", "Royal Purple", "Midnight Black", "Sunrise Pink"]
        selected_theme = st.sidebar.selectbox("Choose Theme", theme_options, index=3)  # Default to Royal Purple
        st.session_state.dark_theme = selected_theme
    else:
        st.session_state.dark_theme = "Light Mode"

    # Custom CSS for themes and animations
    if st.session_state.dark_mode:
        theme = st.session_state.dark_theme

        if theme == "Ocean Blue":
            bg_gradient = "linear-gradient(135deg, #0f1419 0%, #1a1a2e 50%, #0f3460 100%)"
            sidebar_gradient = "linear-gradient(135deg, #1e3a8a 0%, #3b82f6 50%, #06b6d4 100%)"
            accent_color = "#06b6d4"
            accent_hover = "#0891b2"
        elif theme == "Sunset Orange":
            bg_gradient = "linear-gradient(135deg, #7c2d12 0%, #ea580c 50%, #f97316 100%)"
            sidebar_gradient = "linear-gradient(135deg, #9a3412 0%, #c2410c 50%, #ea580c 100%)"
            accent_color = "#f97316"
            accent_hover = "#ea580c"
        elif theme == "Forest Green":
            bg_gradient = "linear-gradient(135deg, #14532d 0%, #166534 50%, #16a34a 100%)"
            sidebar_gradient = "linear-gradient(135deg, #166534 0%, #15803d 50%, #16a34a 100%)"
            accent_color = "#22c55e"
            accent_hover = "#16a34a"
        elif theme == "Royal Purple":
            bg_gradient = "linear-gradient(135deg, #2d1b69 0%, #4c1d95 50%, #7c3aed 100%)"
            sidebar_gradient = "linear-gradient(135deg, #581c87 0%, #7c3aed 50%, #a855f7 100%)"
            accent_color = "#a855f7"
            accent_hover = "#9333ea"
        elif theme == "Midnight Black":
            bg_gradient = "linear-gradient(135deg, #000000 0%, #1a1a1a 50%, #2a2a2a 100%)"
            sidebar_gradient = "linear-gradient(135deg, #1a1a1a 0%, #2a2a2a 50%, #3a3a3a 100%)"
            accent_color = "#f59e0b"
            accent_hover = "#d97706"
        elif theme == "Sunrise Pink":
            bg_gradient = "linear-gradient(135deg, #831843 0%, #be185d 50%, #ec4899 100%)"
            sidebar_gradient = "linear-gradient(135deg, #be185d 0%, #db2777 50%, #ec4899 100%)"
            accent_color = "#f472b6"
            accent_hover = "#ec4899"

        theme_css = f"""
        <style>
        /* Dark Theme - {theme} */
        body, .stApp {{
            background: {bg_gradient} !important;
            color: #ffffff !important;
        }}
        /* Force black text on all elements */
        /* Streamlit element containers in black */
        .stContainer, .stBlock, .stVerticalBlock, .stForm, .stColumns, .stExpander {{
            background-color: #000000 !important;
            border: 1px solid {accent_color} !important;
            border-radius: 8px !important;
            padding: 15px !important;
            margin: 10px 0 !important;
            transition: all 0.3s ease !important;
        }}
        .stContainer:hover, .stBlock:hover, .stVerticalBlock:hover, .stForm:hover, .stColumns:hover, .stExpander:hover {{
            background-color: rgba(0, 0, 0, 0.95) !important;
            border-color: {accent_hover} !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3) !important;
        }}
        /* Override any inherited colors */
        h1, h2, h3, h4, h5, h6, p, span, div, label, strong, em, b, i {{
            color: #ffffff !important;
        }}
        .stMarkdown, .stText, .stHeader, .stSubheader {{
            color: #ffffff !important;
        }}
        .stMarkdown p, .stMarkdown span, .stMarkdown div {{
            color: #ffffff !important;
        }}
        /* Form labels and text */
        .stTextInput label, .stTextArea label, .stSelectbox label, .stNumberInput label, .stDateInput label, .stTimeInput label {{
            color: #ffffff !important;
            font-weight: bold !important;
        }}
        /* Button text */
        .stButton button {{
            color: white !important;
            background-color: #000000 !important;
            border: 2px solid {accent_color} !important;
            transition: all 0.3s ease !important;
        }}
        .stButton button:hover {{
            background-color: {accent_color} !important;
            color: white !important;
            transform: scale(1.05) !important;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3) !important;
        }}
        /* Tab text */
        .stTabs [data-baseweb="tab"] {{
            color: #ffffff !important;
        }}
        /* Metric text */
        .stMetric label, .stMetric .metric-value {{
            color: #ffffff !important;
        }}
        /* Dataframe text */
        .stDataFrame, .stTable {{
            color: #ffffff !important;
        }}
        /* List items styling */
        li {{
            background-color: #000000 !important;
            color: #ffffff !important;
            padding: 8px 12px !important;
            margin: 4px 0 !important;
            border-radius: 5px !important;
            border: 1px solid {accent_color} !important;
            transition: all 0.3s ease !important;
        }}
        li:hover {{
            background-color: {accent_color} !important;
            transform: translateX(5px) !important;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3) !important;
        }}
        /* Additional list styling */
        ul, ol {{
            color: black !important;
        }}
        input, button {{
            color: black !important;
        }}
        /* Radio button text (Login/Register selector) */
        .stRadio [data-baseweb="radio"] label {{
            color: #ffffff !important;
            font-weight: bold !important;
        }}
        .stRadio [data-baseweb="radio"] [data-baseweb="radio-mark"] {{
            background-color: {accent_color} !important;
            border-color: {accent_color} !important;
        }}
        /* Form submit button text */
        .stFormSubmitter button {{
            color: white !important;
            background-color: {accent_color} !important;
            border: none !important;
            transition: all 0.3s ease !important;
        }}
        .stFormSubmitter button:hover {{
            background-color: {accent_hover} !important;
            transform: scale(1.05) !important;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3) !important;
        }}
        /* Force white text on all Streamlit components */
        .css-1v0mbdj, .css-1v3fvcr, .css-10trblm, .css-1q8dd3e, .css-1r6slb0 {{
            color: #ffffff !important;
        }}
        /* Override any dark backgrounds that might hide text */
        .stTextInput, .stTextArea, .stSelectbox {{
            background-color: rgba(255, 255, 255, 0.1) !important;
            border: 1px solid {accent_color} !important;
        }}
        .stTextInput input, .stTextArea textarea {{
            color: #ffffff !important;
            background-color: transparent !important;
        }}
        .stSidebar {{
            background: linear-gradient(135deg, #2d1b69 0%, #e94560 100%) !important;
            border-right: 2px solid {accent_color} !important;
            color: #ffffff !important;
        }}
        .stSidebar h1, .stSidebar h2, .stSidebar h3, .stSidebar p, .stSidebar span, .stSidebar div, .stSidebar label {{
            color: #ffffff !important;
        }}
        .stTextInput, .stTextArea, .stSelectbox, .stNumberInput, .stDateInput, .stTimeInput {{
            background-color: #1e1e2f !important;
            color: #ffffff !important;
            border: 2px solid {accent_color} !important;
            border-radius: 10px !important;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2) !important;
        }}
        .stTextInput input, .stTextArea textarea, .stSelectbox select {{
            background-color: #1e1e2f !important;
            color: #ffffff !important;
        }}
        .stSelectbox [data-baseweb="select"] [data-baseweb="tag"] {{
            background-color: {accent_color} !important;
            color: #ffffff !important;
        }}
        .stSelectbox [data-baseweb="select"] [data-baseweb="popover"] {{
            background-color: #000000 !important;
            border: 2px solid {accent_color} !important;
            border-radius: 10px !important;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3) !important;
        }}
        .stSelectbox [data-baseweb="select"] [data-baseweb="option"] {{
            background-color: #000000 !important;
            color: #ffffff !important;
            padding: 10px !important;
            border-bottom: 1px solid #333 !important;
        }}
        .stSelectbox [data-baseweb="select"] [data-baseweb="option"]:hover {{
            background-color: {accent_color} !important;
            color: #000000 !important;
            transform: scale(1.02) !important;
        }}
        .stSelectbox [data-baseweb="select"] [data-baseweb="option"]:last-child {{
            border-bottom: none !important;
        }}
        /* Additional selectbox styling for better visibility */
        [data-baseweb="select"] [data-baseweb="popover"] [role="listbox"] [role="option"] {{
            color: #ffffff !important;
            background-color: #1e1e2f !important;
            padding: 12px 15px !important;
            font-size: 16px !important;
            font-weight: 500 !important;
        }}
        [data-baseweb="select"] [data-baseweb="popover"] [role="listbox"] [role="option"]:hover {{
            background-color: {accent_color} !important;
            color: #ffffff !important;
            border-radius: 5px !important;
        }}
        /* Sidebar selectbox specific styling */
        .stSidebar .stSelectbox [data-baseweb="select"] {{
            background: {sidebar_gradient} !important;
            border: 2px solid {accent_color} !important;
            border-radius: 10px !important;
        }}
        .stSidebar .stSelectbox [data-baseweb="select"] [data-baseweb="value-container"] {{
            color: #ffffff !important;
            font-weight: bold !important;
        }}
        .stSidebar .stSelectbox [data-baseweb="select"] [data-baseweb="icon"] {{
            color: {accent_color} !important;
        }}
        /* Theme selector dropdown visibility */
        .stSidebar .stSelectbox [data-baseweb="select"] [data-baseweb="popover"] {{
            background: #000000 !important;
            border: 2px solid {accent_color} !important;
            border-radius: 10px !important;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3) !important;
        }}
        .stSidebar .stSelectbox [data-baseweb="select"] [data-baseweb="option"] {{
            background: #000000 !important;
            color: #ffffff !important;
            padding: 12px 15px !important;
            font-size: 16px !important;
            font-weight: 500 !important;
            border-bottom: 1px solid rgba(255, 255, 255, 0.2) !important;
            transition: all 0.2s ease !important;
        }}
        .stSidebar .stSelectbox [data-baseweb="select"] [data-baseweb="option"]:hover {{
            background-color: {accent_color} !important;
            color: #000000 !important;
            border-radius: 5px !important;
            transform: translateX(5px) !important;
        }}
        .stSidebar .stSelectbox [data-baseweb="select"] [data-baseweb="option"]:last-child {{
            border-bottom: none !important;
        }}
        /* Main selectbox styling */
        .stSidebar .stSelectbox [data-baseweb="select"] {{
            background: {sidebar_gradient} !important;
            border: 2px solid {accent_color} !important;
            border-radius: 10px !important;
        }}
        .stSidebar .stSelectbox [data-baseweb="select"] [data-baseweb="value-container"] {{
            color: #ffffff !important;
            font-weight: bold !important;
        }}
        .stSidebar .stSelectbox [data-baseweb="select"] [data-baseweb="icon"] {{
            color: {accent_color} !important;
        }}
        /* Ensure no black backgrounds */
        .stSelectbox [data-baseweb="option"] {{
            background: {sidebar_gradient} !important;
            color: #ffffff !important;
        }}
        .stSelectbox [data-baseweb="option"]:hover {{
            background-color: {accent_color} !important;
            color: #ffffff !important;
        }}
        /* Tooltip and hover text visibility */
        .stTooltip, [data-testid="stTooltip"] {{
            background-color: #1e1e2f !important;
            color: #ffffff !important;
            border: 1px solid {accent_color} !important;
            border-radius: 5px !important;
        }}
        /* General hover states for better visibility */
        .stMarkdown:hover, .stText:hover {{
            color: #ffffff !important;
        }}
        .stButton button {{
            background: linear-gradient(135deg, {accent_color} 0%, {accent_hover} 100%) !important;
            color: white !important;
            border: none !important;
            border-radius: 25px !important;
            padding: 10px 20px !important;
            font-weight: bold !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.4) !important;
        }}
        .stButton button:hover {{
            background: linear-gradient(135deg, {accent_hover} 0%, {accent_color} 100%) !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 20px rgba(0, 0, 0, 0.6) !important;
        }}
        .stDataFrame, .stTable {{
            background-color: #1e1e2f !important;
            color: #ffffff !important;
            border-radius: 10px !important;
            border: 1px solid {accent_color} !important;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2) !important;
        }}
        .stTabs [data-baseweb="tab-list"] {{
            background: {sidebar_gradient} !important;
            border-radius: 10px !important;
        }}
        .stTabs [data-baseweb="tab"] {{
            color: #ffffff !important;
            border-radius: 10px !important;
            transition: all 0.3s ease !important;
        }}
        .stTabs [aria-selected="true"] {{
            background: linear-gradient(135deg, {accent_color} 0%, {accent_hover} 100%) !important;
            color: white !important;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.4) !important;
        }}
        .stMetric {{
            background: {sidebar_gradient} !important;
            border-radius: 15px !important;
            padding: 20px !important;
            border: 2px solid {accent_color} !important;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3) !important;
        }}
        .stMetric label {{
            color: {accent_color} !important;
            font-weight: bold !important;
        }}
        .stMetric .metric-value {{
            color: #ffffff !important;
            font-size: 2em !important;
        }}
        /* Plotly charts styling */
        .js-plotly-plot .plotly .modebar {{
            background: #1e1e2f !important;
        }}
        .js-plotly-plot .plotly .modebar-btn {{
            color: #ffffff !important;
        }}
        /* Animations */
        .fade-in {{
            animation: fadeIn 1s ease-in;
        }}
        @keyframes fadeIn {{
            from {{ opacity: 0; }}
            to {{ opacity: 1; }}
        }}
        .slide-in {{
            animation: slideIn 0.5s ease-out;
        }}
        @keyframes slideIn {{
            from {{ transform: translateX(-100%); }}
            to {{ transform: translateX(0); }}
        }}
        .bounce {{
            animation: bounce 2s infinite;
        }}
        @keyframes bounce {{
            0%, 20%, 50%, 80%, 100% {{ transform: translateY(0); }}
            40% {{ transform: translateY(-10px); }}
            60% {{ transform: translateY(-5px); }}
        }}
        /* Custom card styling */
        .card {{
            background: {sidebar_gradient} !important;
            border-radius: 15px !important;
            padding: 20px !important;
            margin: 10px 0 !important;
            border: 2px solid {accent_color} !important;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3) !important;
        }}
        /* Background decorative objects */
        body::before {{
            content: "📚";
            position: fixed;
            top: 10%;
            left: 5%;
            font-size: 3em;
            opacity: 0.1;
            animation: float 6s ease-in-out infinite;
            z-index: -1;
        }}
        body::after {{
            content: "🎓";
            position: fixed;
            top: 20%;
            right: 5%;
            font-size: 2.5em;
            opacity: 0.1;
            animation: float 8s ease-in-out infinite reverse;
            z-index: -1;
        }}
        .bg-object-1 {{
            content: "✏️";
            position: fixed;
            bottom: 15%;
            left: 10%;
            font-size: 2em;
            opacity: 0.1;
            animation: float 7s ease-in-out infinite;
            z-index: -1;
        }}
        .bg-object-2 {{
            content: "💡";
            position: fixed;
            bottom: 25%;
            right: 10%;
            font-size: 2.5em;
            opacity: 0.1;
            animation: float 9s ease-in-out infinite reverse;
            z-index: -1;
        }}
        .bg-object-3 {{
            content: "📖";
            position: fixed;
            top: 30%;
            left: 50%;
            font-size: 2em;
            opacity: 0.1;
            animation: float 5s ease-in-out infinite;
            z-index: -1;
        }}
        .bg-object-4 {{
            content: "🧠";
            position: fixed;
            top: 50%;
            right: 20%;
            font-size: 2.2em;
            opacity: 0.1;
            animation: float 10s ease-in-out infinite reverse;
            z-index: -1;
        }}
        @keyframes float {{
            0%, 100% {{ transform: translateY(0px); }}
            50% {{ transform: translateY(-20px); }}
        }}
        </style>
        """
    else:
        theme_css = """
        <style>
        /* Light Theme */
        body, .stApp {
            background-color: #f5f5f5 !important;
            color: #333333 !important;
        }
        .stSidebar {
            background-color: #ffffff !important;
        }
        .stTextInput, .stTextArea, .stSelectbox, .stNumberInput, .stDateInput, .stTimeInput {
            background-color: #ffffff !important;
            color: #333333 !important;
            border: 1px solid #ddd !important;
        }
        .stButton button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
            color: white !important;
            border: none !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4) !important;
        }
        .stButton button:hover {
            background: linear-gradient(135deg, #764ba2 0%, #667eea 100%) !important;
            transform: translateY(-2px) scale(1.05) !important;
            box-shadow: 0 8px 25px rgba(102, 126, 234, 0.6) !important;
        }
        .stDataFrame, .stTable {
            background-color: #ffffff !important;
            color: #333333 !important;
        }
        .stTabs [data-baseweb="tab-list"] {
            background-color: #f0f0f0 !important;
        }
        .stTabs [data-baseweb="tab"] {
            color: #333333 !important;
        }
        .stTabs [aria-selected="true"] {
            background-color: #4CAF50 !important;
        }
        /* Animations */
        .fade-in {
            animation: fadeIn 1s ease-in;
        }
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        .slide-in {
            animation: slideIn 0.5s ease-out;
        }
        @keyframes slideIn {
            from { transform: translateX(-100%); }
            to { transform: translateX(0); }
        }
        .bounce {
            animation: bounce 2s infinite;
        }
        @keyframes bounce {
            0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
            40% { transform: translateY(-10px); }
            60% { transform: translateY(-5px); }
        }
        </style>
        """

    st.markdown(theme_css, unsafe_allow_html=True)
