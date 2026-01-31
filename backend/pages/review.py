"""
Review Page - Review responses before final submission
"""

import streamlit as st
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from config import SESSION_KEYS, QUESTIONNAIRE_SECTIONS, COLORS
from utils.ui_components import render_header
from database.chromadb_manager import ChromaDBManager


def show():
    """Render the review page"""
    
    render_header("Review Your Responses", "Please review your answers before submitting")
    
    # Company information review
    st.markdown(
        f"""
        <div class='section-header'>
            Company Information
        </div>
        """,
        unsafe_allow_html=True
    )
    
    company_info = st.session_state[SESSION_KEYS["company_info"]]
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(
            f"""
            <div class='info-box'>
                <p><strong>Company Name:</strong> {company_info.get('company_name', 'N/A')}</p>
                <p><strong>Industry:</strong> {company_info.get('industry', 'N/A')}</p>
                <p><strong>Company Size:</strong> {company_info.get('company_size', 'N/A')}</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col2:
        st.markdown(
            f"""
            <div class='info-box'>
                <p><strong>Region:</strong> {company_info.get('region', 'N/A')}</p>
                <p><strong>Contact Email:</strong> {company_info.get('contact_email', 'N/A')}</p>
                <p><strong>Contact Name:</strong> {company_info.get('contact_name', 'N/A')}</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Assessment responses review
    st.markdown(
        f"""
        <div class='section-header'>
            Assessment Responses
        </div>
        """,
        unsafe_allow_html=True
    )
    
    responses = st.session_state[SESSION_KEYS["responses"]]
    
    for section_idx, section_name in enumerate(QUESTIONNAIRE_SECTIONS, 1):
        section_responses = responses.get(section_name, {})
        
        answered_count = len([r for r in section_responses.values() if r.get("answer")])
        
        with st.expander(f"{section_idx}. {section_name} ({answered_count} responses)", expanded=False):
            if section_responses:
                for q_idx, (question_key, response_data) in enumerate(section_responses.items(), 1):
                    if response_data.get("answer"):
                        st.markdown(
                            f"""
                            <div style='background-color: {COLORS['card_bg']}; padding: 15px; margin: 10px 0; border-radius: 5px;'>
                                <p><strong>Q{q_idx}:</strong> {response_data['question_text']}</p>
                                <p style='color: {COLORS['secondary']};'><strong>Answer:</strong> {response_data['answer']}</p>
                                {f"<p><strong>Comment:</strong> {response_data['comment']}</p>" if response_data.get('comment') else ""}
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
            else:
                st.info("No responses recorded for this section")
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Confirmation
    st.markdown(
        f"""
        <div class='info-box' style='border-color: {COLORS['secondary']};'>
            <h4>Before you submit:</h4>
            <ul>
                <li>Please review all your responses carefully</li>
                <li>Once submitted, your assessment will be finalized</li>
                <li>You will receive a detailed report with your resilience score and recommendations</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Confirmation checkbox
    confirm = st.checkbox(
        "I confirm that all responses are accurate and complete",
        key="confirm_submission"
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Navigation buttons
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button("← Back to Edit", use_container_width=True):
            st.session_state[SESSION_KEYS["current_page"]] = "questionnaire"
            st.rerun()
    
    with col3:
        if confirm:
            if st.button("✅ Submit Assessment", type="primary", use_container_width=True):
                # Final save and mark as completed
                finalize_assessment()
                st.session_state[SESSION_KEYS["current_page"]] = "results"
                st.rerun()
        else:
            st.button("Submit Assessment", use_container_width=True, disabled=True)


def finalize_assessment():
    """Finalize and submit the assessment"""
    db = ChromaDBManager()
    assessment_id = st.session_state[SESSION_KEYS["assessment_id"]]
    
    # Update assessment status to completed
    db.update_assessment_status(
        assessment_id,
        "completed",
        st.session_state[SESSION_KEYS["completed_sections"]]
    )
