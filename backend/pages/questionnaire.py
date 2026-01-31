"""
Questionnaire Page - Main assessment questonn with all sections
"""

import streamlit as st
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from config import SESSION_KEYS, QUESTIONNAIRE_SECTIONS, COLORS
from utils.ui_components import render_header, render_progress_bar, render_section_header
from questionnaire.questionnaire_schema import get_questionnaire_schema
from database.chromadb_manager import ChromaDBManager


def show():
    """Render the main questionnaire page"""
    
    render_header("Cyber Resilience Assessment Questionnaire", "Answer all questions to complete your assessment")
    
    # Get questionnaire schema
    schema = get_questionnaire_schema()
    
    # Initialize responses if not exists
    if not st.session_state[SESSION_KEYS["responses"]]:
        st.session_state[SESSION_KEYS["responses"]] = {section: {} for section in QUESTIONNAIRE_SECTIONS}
    
    # Calculate progress
    total_questions = sum(len(questions) for questions in schema.values())
    answered_questions = sum(
        len([q for q in st.session_state[SESSION_KEYS["responses"]].get(section, {}).values() if q.get("answer")])
        for section in QUESTIONNAIRE_SECTIONS
    )
    
    # Progress indicator
    render_progress_bar(answered_questions, total_questions, "Overall Progress")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Render each section
    for section_idx, section_name in enumerate(QUESTIONNAIRE_SECTIONS, 1):
        questions = schema[section_name]
        
        # Section progress
        section_answered = len([
            q for q in st.session_state[SESSION_KEYS["responses"]].get(section_name, {}).values() 
            if q.get("answer")
        ])
        section_completion = (section_answered / len(questions)) * 100 if questions else 0
        
        # Section header with expander
        section_complete = section_completion == 100
        completion_icon = "✅" if section_complete else "⏺️"
        
        with st.expander(
            f"{completion_icon} {section_idx}. {section_name} ({section_answered}/{len(questions)} completed)",
            expanded=(section_idx == 1)  # Expand first section by default
        ):
            st.markdown(
                f"""
                <div style='margin-bottom: 20px;'>
                    <div style='background-color: {COLORS['card_bg']}; padding: 10px; border-radius: 5px;'>
                        Section Progress: {section_completion:.0f}%
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            # Render questions in this section
            for q_idx, question in enumerate(questions):
                st.markdown(f"<br>", unsafe_allow_html=True)
                
                question_key = f"{section_name}_q{q_idx}"
                question_text = question["question_text"]
                question_type = question["question_type"]
                response_options = question["response_options"]
                help_text = question.get("help_text", "")
                required = question.get("required", True)
                
                # Question label
                required_marker = " *" if required else ""
                st.markdown(
                    f"""
                    <div style='background-color: {COLORS['card_bg']}; padding: 15px; border-left: 3px solid {COLORS['secondary']}; border-radius: 5px; margin-bottom: 10px;'>
                        <strong>Question {q_idx + 1}{required_marker}:</strong> {question_text}
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                
                # Get existing answer
                existing_answer = st.session_state[SESSION_KEYS["responses"]].get(section_name, {}).get(question_key, {}).get("answer", "")
                existing_index = response_options.index(existing_answer) if existing_answer in response_options else 0
                
                # Render input based on question type
                answer = st.radio(
                    f"Select your response:",
                    options=response_options,
                    index=existing_index,
                    key=f"radio_{question_key}",
                    help=help_text
                )
                
                # Optional comments
                existing_comment = st.session_state[SESSION_KEYS["responses"]].get(section_name, {}).get(question_key, {}).get("comment", "")
                comment = st.text_area(
                    "Additional comments (optional):",
                    value=existing_comment,
                    key=f"comment_{question_key}",
                    height=70,
                    placeholder="Provide any additional context or notes..."
                )
                
                # Save response
                if section_name not in st.session_state[SESSION_KEYS["responses"]]:
                    st.session_state[SESSION_KEYS["responses"]][section_name] = {}
                
                st.session_state[SESSION_KEYS["responses"]][section_name][question_key] = {
                    "question_text": question_text,
                    "question_type": question_type,
                    "answer": answer,
                    "comment": comment
                }
                
                st.markdown("<hr style='opacity: 0.2;'>", unsafe_allow_html=True)
            
            # Mark section as complete if all required questions answered
            if section_complete and section_name not in st.session_state[SESSION_KEYS["completed_sections"]]:
                st.session_state[SESSION_KEYS["completed_sections"]].append(section_name)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Navigation buttons
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button("← Back to Company Info", use_container_width=True):
            st.session_state[SESSION_KEYS["current_page"]] = "company_info"
            st.rerun()
    
    with col2:
        # Save progress button
        if st.button("💾 Save Progress", use_container_width=True):
            save_responses_to_db()
            st.success("Progress saved successfully!")
    
    with col3:
        # Check if all required questions are answered
        all_answered = answered_questions == total_questions
        
        if all_answered:
            if st.button("Review & Submit →", type="primary", use_container_width=True):
                save_responses_to_db()
                st.session_state[SESSION_KEYS["current_page"]] = "review"
                st.rerun()
        else:
            st.button(
                f"Complete All Questions ({answered_questions}/{total_questions})",
                use_container_width=True,
                disabled=True
            )


def save_responses_to_db():
    """Save all responses to ChromaDB"""
    db = ChromaDBManager()
    assessment_id = st.session_state[SESSION_KEYS["assessment_id"]]
    
    for section_name, questions in st.session_state[SESSION_KEYS["responses"]].items():
        for question_key, response_data in questions.items():
            if response_data.get("answer"):
                response_entry = {
                    "assessment_id": assessment_id,
                    "section": section_name,
                    "question_id": question_key,
                    "question_text": response_data["question_text"],
                    "question_type": response_data["question_type"],
                    "answer": response_data["answer"],
                    "comment": response_data.get("comment", "")
                }
                db.add_response(response_entry)
    
    # Update assessment status
    db.update_assessment_status(
        assessment_id,
        "in_progress",
        st.session_state[SESSION_KEYS["completed_sections"]]
    )
