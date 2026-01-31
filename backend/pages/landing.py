"""
Landing Page - Introduction and Start Assessment
"""

import streamlit as st
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from config import APP_TITLE, APP_SUBTITLE, SESSION_KEYS, COLORS, COMPANY_NAME, COMPANY_TAGLINE, LOGO_PATH
from utils.ui_components import render_header, render_info_box
from PIL import Image


def show():
    """Render the landing page"""
    
    # Header with SBA Info Solutions logo
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        # Display SBA logo
        if LOGO_PATH.exists():
            logo = Image.open(LOGO_PATH)
            st.image(logo, width=300, use_container_width=False)
        
        st.markdown(
            f"""
            <div style='text-align: center; margin-top: 30px;'>
                <h1 style='color: {COLORS['text']}; margin-bottom: 10px;'>{APP_TITLE}</h1>
                <h3 style='color: {COLORS['secondary']};'>{APP_SUBTITLE}</h3>
                <p style='color: {COLORS['text']}; font-size: 1.1em; margin-top: 15px; opacity: 0.8;'>{COMPANY_TAGLINE}</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Introduction
    st.markdown(
        f"""
        <div class='custom-card' style='margin: 30px auto; max-width: 800px;'>
            <h2 style='color: {COLORS['secondary']}; text-align: center;'>Welcome to Your Cyber Resilience Assessment</h2>
            <p style='font-size: 1.1em; line-height: 1.8; text-align: justify;'>
                In today's digital landscape, cyber threats are constantly evolving. Understanding your organization's 
                cyber resilience posture is critical to protecting your assets, reputation, and stakeholders.
            </p>
            <p style='font-size: 1.1em; line-height: 1.8; text-align: justify;'>
                This comprehensive assessment evaluates your cybersecurity maturity across <strong>8 critical security domains</strong>, 
                providing you with actionable insights and recommendations to strengthen your defenses.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # What to expect
    st.markdown(
        f"""
        <div style='margin: 40px auto; max-width: 900px;'>
            <h2 style='color: {COLORS['secondary']}; text-align: center; margin-bottom: 30px;'>What to Expect</h2>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(
            f"""
            <div class='metric-container'>
                <div style='font-size: 50px; margin-bottom: 15px;'>📋</div>
                <div class='metric-label' style='font-size: 1.1em;'><strong>8 Security Domains</strong></div>
                <p style='margin-top: 10px; font-size: 0.9em;'>Comprehensive coverage of cybersecurity controls</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col2:
        st.markdown(
            f"""
            <div class='metric-container'>
                <div style='font-size: 50px; margin-bottom: 15px;'>⏱️</div>
                <div class='metric-label' style='font-size: 1.1em;'><strong>20-30 Minutes</strong></div>
                <p style='margin-top: 10px; font-size: 0.9em;'>Expected completion time</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col3:
        st.markdown(
            f"""
            <div class='metric-container'>
                <div style='font-size: 50px; margin-bottom: 15px;'>📊</div>
                <div class='metric-label' style='font-size: 1.1em;'><strong>Detailed Insights</strong></div>
                <p style='margin-top: 10px; font-size: 0.9em;'>Actionable recommendations and scoring</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    # Assessment domains
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    st.markdown(
        f"""
        <div style='margin: 40px auto; max-width: 900px;'>
            <h2 style='color: {COLORS['secondary']}; text-align: center; margin-bottom: 30px;'>Assessment Domains</h2>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    domains = [
        ("🏛️", "Governance & Risk Management", "Strategy, policies, and risk assessment processes"),
        ("💼", "Asset Management", "Inventory and classification of IT assets"),
        ("🔐", "Access Control & Identity Management", "Authentication, authorization, and access controls"),
        ("🔍", "Security Operations & Monitoring", "Threat detection, monitoring, and vulnerability management"),
        ("🚨", "Incident Response & Recovery", "Incident handling and business continuity"),
        ("🔒", "Data Protection & Privacy", "Encryption, privacy controls, and data governance"),
        ("🤝", "Third-Party Risk Management", "Vendor security and supply chain risk"),
        ("🎓", "Security Awareness & Training", "Employee education and security culture")
    ]
    
    col1, col2 = st.columns(2)
    
    for i, (icon, title, desc) in enumerate(domains):
        with col1 if i % 2 == 0 else col2:
            st.markdown(
                f"""
                <div class='info-box'>
                    <div style='font-size: 30px; margin-bottom: 10px;'>{icon}</div>
                    <h4 style='color: {COLORS['secondary']};'>{title}</h4>
                    <p style='font-size: 0.9em;'>{desc}</p>
                </div>
                """,
                unsafe_allow_html=True
            )
    
    # Call to action
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🚀 Start Assessment", use_container_width=True, type="primary"):
            st.session_state[SESSION_KEYS["current_page"]] = "company_info"
            st.rerun()
    
    # Footer
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown(
        f"""
        <div style='text-align: center; color: {COLORS['text']}; opacity: 0.7; font-size: 0.9em;'>
            <p>🔒 All responses are stored securely and confidentially</p>
            <p>© 2026 {COMPANY_NAME} - Enterprise Cybersecurity Solutions</p>
            <p style='font-size: 0.85em;'>📧 Contact: info@sbainfosolutions.com | 🌐 www.sbainfosolutions.com</p>
        </div>
        """,
        unsafe_allow_html=True
    )
