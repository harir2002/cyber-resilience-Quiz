"""
Main Streamlit Application - Cyber Resilience Maturity Assessment
Entry point for the questionnaire application
"""

import streamlit as st
import sys
from pathlib import Path

# Add current directory to path
sys.path.append(str(Path(__file__).parent))

from config import APP_TITLE, APP_SUBTITLE, COLORS, SESSION_KEYS
from utils.ui_components import apply_custom_css, render_header
from database.chromadb_manager import ChromaDBManager

# Page configuration
st.set_page_config(
    page_title=f"{APP_TITLE} - SBA Info Solutions",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        'About': "Cyber Resilience Assessment Platform by SBA Info Solutions"
    }
)

# Apply custom styling
apply_custom_css()

# Initialize session state
def init_session_state():
    """Initialize all session state variables"""
    if SESSION_KEYS["current_page"] not in st.session_state:
        st.session_state[SESSION_KEYS["current_page"]] = "landing"
    
    if SESSION_KEYS["company_info"] not in st.session_state:
        st.session_state[SESSION_KEYS["company_info"]] = {}
    
    if SESSION_KEYS["responses"] not in st.session_state:
        st.session_state[SESSION_KEYS["responses"]] = {}
    
    if SESSION_KEYS["assessment_id"] not in st.session_state:
        st.session_state[SESSION_KEYS["assessment_id"]] = None
    
    if SESSION_KEYS["completed_sections"] not in st.session_state:
        st.session_state[SESSION_KEYS["completed_sections"]] = []

init_session_state()

# Navigation
current_page = st.session_state[SESSION_KEYS["current_page"]]

# Import pages (will be created next)
from pages import landing, company_info, questionnaire, review, results

# Page routing
if current_page == "landing":
    landing.show()
elif current_page == "company_info":
    company_info.show()
elif current_page == "questionnaire":
    questionnaire.show()
elif current_page == "review":
    review.show()
elif current_page == "results":
    results.show()
else:
    landing.show()
