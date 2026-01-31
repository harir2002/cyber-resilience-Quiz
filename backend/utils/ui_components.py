"""
UI Components - Reusable Streamlit components with consistent branding
Implements the Black/Red/White color scheme
"""

import streamlit as st
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from config import COLORS


def apply_custom_css():
    """Apply custom CSS for branding and styling"""
    
    css = f"""
    <style>
    /* Main background */
    .stApp {{
        background-color: {COLORS['background']};
        color: {COLORS['text']};
    }}
    
    /* Headers */
    h1, h2, h3, h4, h5, h6 {{
        color: {COLORS['text']} !important;
        font-weight: 700 !important;
    }}
    
    h1 {{
        border-bottom: 3px solid {COLORS['secondary']};
        padding-bottom: 10px;
    }}
    
    h2 {{
        color: {COLORS['secondary']} !important;
    }}
    
    /* Text */
    p, li, span, div, label {{
        color: {COLORS['text']} !important;
    }}
    
    /* Buttons */
    .stButton > button {{
        background-color: {COLORS['secondary']};
        color: {COLORS['text']};
        border: none;
        border-radius: 5px;
        padding: 10px 20px;
        font-weight: bold;
        transition: all 0.3s ease;
    }}
    
    .stButton > button:hover {{
        background-color: #ff1a1a;
        transform: scale(1.05);
        box-shadow: 0 0 10px {COLORS['secondary']};
    }}
    
    /* Input fields */
    .stTextInput > div > div > input,
    .stSelectbox > div > div > div,
    .stTextArea > div > div > textarea {{
        background-color: {COLORS['card_bg']};
        color: {COLORS['text']};
        border: 1px solid {COLORS['secondary']};
        border-radius: 5px;
    }}
    
    /* Radio buttons */
    .stRadio > div {{
        background-color: {COLORS['card_bg']};
        padding: 15px;
        border-radius: 5px;
        border: 1px solid {COLORS['border']};
    }}
    
    .stRadio > div > label {{
        color: {COLORS['text']} !important;
    }}
    
    /* Cards/Containers */
    .element-container {{
        color: {COLORS['text']};
    }}
    
    /* Progress bar */
    .stProgress > div > div > div > div {{
        background-color: {COLORS['secondary']};
    }}
    
    /* Sidebar */
    .css-1d391kg {{
        background-color: {COLORS['card_bg']};
    }}
    
    /* Expander */
    .streamlit-expanderHeader {{
        background-color: {COLORS['card_bg']};
        color: {COLORS['text']} !important;
        border: 1px solid {COLORS['border']};
        border-radius: 5px;
    }}
    
    .streamlit-expanderHeader:hover {{
        background-color: {COLORS['secondary']};
    }}
    
    /* Success/Error messages */
    .stSuccess {{
        background-color: {COLORS['success']};
        color: {COLORS['background']};
    }}
    
    .stError {{
        background-color: {COLORS['error']};
        color: {COLORS['text']};
    }}
    
    /* Custom card style */
    .custom-card {{
        background-color: {COLORS['card_bg']};
        border: 2px solid {COLORS['border']};
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
    }}
    
    /* Section header */
    .section-header {{
        background-color: {COLORS['secondary']};
        color: {COLORS['text']};
        padding: 15px;
        border-radius: 5px;
        margin: 20px 0 10px 0;
        font-weight: bold;
        font-size: 1.2em;
    }}
    
    /* Info box */
    .info-box {{
        background-color: {COLORS['card_bg']};
        border-left: 4px solid {COLORS['secondary']};
        padding: 15px;
        margin: 10px 0;
        border-radius: 5px;
    }}
    
    /* Metric container */
    .metric-container {{
        background-color: {COLORS['card_bg']};
        border: 2px solid {COLORS['secondary']};
        border-radius: 10px;
        padding: 20px;
        text-align: center;
        margin: 10px;
    }}
    
    .metric-value {{
        font-size: 2.5em;
        font-weight: bold;
        color: {COLORS['secondary']};
    }}
    
    .metric-label {{
        font-size: 1em;
        color: {COLORS['text']};
        margin-top: 10px;
    }}
    </style>
    """
    
    st.markdown(css, unsafe_allow_html=True)


def render_header(title: str, subtitle: str = ""):
    """Render application header with branding"""
    st.markdown(f"<h1 style='text-align: center;'>{title}</h1>", unsafe_allow_html=True)
    if subtitle:
        st.markdown(f"<p style='text-align: center; font-size: 1.2em;'>{subtitle}</p>", unsafe_allow_html=True)
    st.markdown("---")


def render_section_header(section_name: str, section_number: int = None):
    """Render a section header"""
    if section_number:
        header_text = f"{section_number}. {section_name}"
    else:
        header_text = section_name
    
    st.markdown(
        f"<div class='section-header'>{header_text}</div>",
        unsafe_allow_html=True
    )


def render_info_box(message: str):
    """Render an information box"""
    st.markdown(
        f"<div class='info-box'>{message}</div>",
        unsafe_allow_html=True
    )


def render_metric_card(label: str, value: str, delta: str = None):
    """Render a metric card"""
    delta_html = f"<div style='color: {COLORS['success']}; font-size: 0.9em;'>{delta}</div>" if delta else ""
    
    st.markdown(
        f"""
        <div class='metric-container'>
            <div class='metric-value'>{value}</div>
            <div class='metric-label'>{label}</div>
            {delta_html}
        </div>
        """,
        unsafe_allow_html=True
    )


def render_progress_bar(current: int, total: int, label: str = "Progress"):
    """Render a progress bar with label"""
    percentage = (current / total) * 100 if total > 0 else 0
    st.markdown(f"**{label}:** {current} of {total} ({percentage:.0f}%)")
    st.progress(percentage / 100)


def render_custom_card(content: str, title: str = None):
    """Render a custom card with content"""
    title_html = f"<h3>{title}</h3>" if title else ""
    st.markdown(
        f"""
        <div class='custom-card'>
            {title_html}
            {content}
        </div>
        """,
        unsafe_allow_html=True
    )


def render_maturity_badge(maturity_level: str) -> str:
    """Generate HTML for maturity level badge"""
    colors = {
        "Not Started": "#666666",
        "Initial": "#ff6b6b",
        "Developing": "#ffa500",
        "Defined": "#ffd700",
        "Managed": "#90ee90",
        "Optimized": "#00ff00"
    }
    
    color = colors.get(maturity_level, COLORS['text'])
    
    return f"""
    <div style='
        background-color: {color};
        color: {COLORS['background']};
        padding: 5px 15px;
        border-radius: 20px;
        display: inline-block;
        font-weight: bold;
        margin: 5px;
    '>
        {maturity_level}
    </div>
    """


def render_risk_badge(risk_level: str) -> str:
    """Generate HTML for risk level badge"""
    colors = {
        "Low": "#00ff00",
        "Medium": "#ffa500",
        "High": "#ff6b6b",
        "Critical": "#e7000b"
    }
    
    color = colors.get(risk_level, COLORS['text'])
    
    return f"""
    <div style='
        background-color: {color};
        color: {COLORS['background']};
        padding: 5px 15px;
        border-radius: 20px;
        display: inline-block;
        font-weight: bold;
        margin: 5px;
    '>
        {risk_level} Risk
    </div>
    """
