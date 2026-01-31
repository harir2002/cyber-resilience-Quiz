"""
Company Information Page - Collect organization details
"""

import streamlit as st
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from config import SESSION_KEYS, COMPANY_SIZES, INDUSTRIES, REGIONS, COLORS
from utils.ui_components import render_header
from database.chromadb_manager import ChromaDBManager


def show():
    """Render the company information collection page"""
    
    render_header("Company Information", "Please provide your organization details")
    
    st.markdown(
        f"""
        <div class='info-box'>
            <p>ℹ️ This information helps us provide tailored recommendations for your organization.</p>
            <p>All fields marked with * are required.</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Create form
    with st.form("company_info_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            company_name = st.text_input(
                "Company Name *",
                value=st.session_state[SESSION_KEYS["company_info"]].get("company_name", ""),
                placeholder="Enter your company name"
            )
            
            industry = st.selectbox(
                "Industry *",
                options=[""] + INDUSTRIES,
                index=INDUSTRIES.index(st.session_state[SESSION_KEYS["company_info"]].get("industry", "")) + 1 
                    if st.session_state[SESSION_KEYS["company_info"]].get("industry") in INDUSTRIES else 0
            )
            
            company_size = st.selectbox(
                "Company Size *",
                options=[""] + COMPANY_SIZES,
                index=COMPANY_SIZES.index(st.session_state[SESSION_KEYS["company_info"]].get("company_size", "")) + 1 
                    if st.session_state[SESSION_KEYS["company_info"]].get("company_size") in COMPANY_SIZES else 0
            )
        
        with col2:
            region = st.selectbox(
                "Region / Country *",
                options=[""] + REGIONS,
                index=REGIONS.index(st.session_state[SESSION_KEYS["company_info"]].get("region", "")) + 1 
                    if st.session_state[SESSION_KEYS["company_info"]].get("region") in REGIONS else 0
            )
            
            contact_email = st.text_input(
                "Primary Contact Email *",
                value=st.session_state[SESSION_KEYS["company_info"]].get("contact_email", ""),
                placeholder="email@company.com"
            )
            
            contact_name = st.text_input(
                "Contact Person Name",
                value=st.session_state[SESSION_KEYS["company_info"]].get("contact_name", ""),
                placeholder="John Doe"
            )
        
        # Additional information
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### Additional Information (Optional)")
        
        additional_notes = st.text_area(
            "Any specific areas of concern or focus?",
            value=st.session_state[SESSION_KEYS["company_info"]].get("additional_notes", ""),
            placeholder="E.g., recent security incidents, regulatory requirements, planned initiatives...",
            height=100
        )
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Form buttons
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            back_button = st.form_submit_button("← Back to Home", use_container_width=True)
        
        with col3:
            submit_button = st.form_submit_button("Continue to Assessment →", type="primary", use_container_width=True)
        
        if back_button:
            st.session_state[SESSION_KEYS["current_page"]] = "landing"
            st.rerun()
        
        if submit_button:
            # Validation
            errors = []
            
            if not company_name.strip():
                errors.append("Company Name is required")
            if not industry:
                errors.append("Industry is required")
            if not company_size:
                errors.append("Company Size is required")
            if not region:
                errors.append("Region is required")
            if not contact_email.strip():
                errors.append("Contact Email is required")
            elif "@" not in contact_email or "." not in contact_email:
                errors.append("Contact Email must be valid")
            
            if errors:
                st.error("Please fix the following errors:")
                for error in errors:
                    st.error(f"• {error}")
            else:
                # Save company information
                company_data = {
                    "company_name": company_name.strip(),
                    "industry": industry,
                    "company_size": company_size,
                    "region": region,
                    "contact_email": contact_email.strip(),
                    "contact_name": contact_name.strip(),
                    "additional_notes": additional_notes.strip()
                }
                
                st.session_state[SESSION_KEYS["company_info"]] = company_data
                
                # Save to database and create assessment
                db = ChromaDBManager()
                
                # Check if company already exists (for returning users)
                existing_companies = db.search_companies(company_name=company_name.strip())
                
                if existing_companies:
                    # Use existing company
                    company_id = existing_companies[0].get("company_id", db.add_company(company_data))
                else:
                    # Create new company
                    company_id = db.add_company(company_data)
                
                # Create new assessment
                assessment_id = db.create_assessment(company_id)
                st.session_state[SESSION_KEYS["assessment_id"]] = assessment_id
                
                st.success("✅ Company information saved successfully!")
                st.session_state[SESSION_KEYS["current_page"]] = "questionnaire"
                st.rerun()
