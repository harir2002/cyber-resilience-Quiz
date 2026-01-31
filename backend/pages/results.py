"""
Results Page - Display assessment results, scores, and recommendations
"""

import streamlit as st
import plotly.graph_objects as go
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from config import SESSION_KEYS, QUESTIONNAIRE_SECTIONS, COLORS, COMPANY_NAME
from utils.ui_components import render_header, render_maturity_badge, render_risk_badge
from utils.scoring import ResilienceScorer


def show():
    """Render the results page"""
    
    render_header("🎯 Your Cyber Resilience Assessment Results", "Detailed analysis and recommendations")
    
    # Calculate scores
    scorer = ResilienceScorer()
    responses = st.session_state[SESSION_KEYS["responses"]]
    
    # Prepare responses for scoring
    scoring_responses = {}
    for section_name, questions in responses.items():
        scoring_responses[section_name] = [
            {
                "question_type": q_data["question_type"],
                "answer": q_data["answer"]
            }
            for q_data in questions.values()
            if q_data.get("answer")
        ]
    
    # Calculate overall score
    results = scorer.calculate_overall_score(scoring_responses)
    
    # Overall Score Card
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(
            f"""
            <div class='metric-container'>
                <div class='metric-label'>Overall Score</div>
                <div class='metric-value'>{results['overall_percentage']:.1f}%</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col2:
        st.markdown(
            f"""
            <div class='metric-container'>
                <div class='metric-label'>Maturity Level</div>
                <div style='margin-top: 15px;'>
                    {render_maturity_badge(results['overall_maturity'])}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col3:
        st.markdown(
            f"""
            <div class='metric-container'>
                <div class='metric-label'>Risk Level</div>
                <div style='margin-top: 15px;'>
                    {render_risk_badge(results['risk_level'])}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col4:
        # Company info
        company_info = st.session_state[SESSION_KEYS["company_info"]]
        st.markdown(
            f"""
            <div class='metric-container'>
                <div class='metric-label'>Organization</div>
                <div style='margin-top: 15px; font-size: 1.2em; font-weight: bold;'>
                    {company_info.get('company_name', 'N/A')}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Section Scores
    st.markdown(
        f"""
        <div class='section-header'>
            Section-wise Performance
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Create radar chart
    section_scores = results['section_scores']
    
    categories = list(section_scores.keys())
    values = [section_scores[cat]['percentage'] for cat in categories]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        fillcolor=COLORS['secondary'],
        opacity=0.6,
        line=dict(color=COLORS['secondary'], width=2),
        marker=dict(color=COLORS['secondary'], size=8)
    ))
    
    fig.update_layout(
        polar=dict(
            bgcolor=COLORS['background'],
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                gridcolor='#333333',
                tickfont=dict(color=COLORS['text'])
            ),
            angularaxis=dict(
                gridcolor='#333333',
                linecolor='#333333',
                tickfont=dict(color=COLORS['text'], size=11)
            )
        ),
        showlegend=False,
        paper_bgcolor=COLORS['background'],
        plot_bgcolor=COLORS['background'],
        font=dict(color=COLORS['text']),
        height=500
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Detailed section breakdown
    st.markdown(
        f"""
        <div class='section-header'>
            Detailed Section Scores
        </div>
        """,
        unsafe_allow_html=True
    )
    
    for section_name in QUESTIONNAIRE_SECTIONS:
        score_data = section_scores[section_name]
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown(f"**{section_name}**")
            st.progress(score_data['percentage'] / 100)
        
        with col2:
            st.markdown(
                f"""
                <div style='text-align: right;'>
                    <strong style='font-size: 1.3em; color: {COLORS['secondary']};'>{score_data['percentage']:.1f}%</strong><br>
                    {render_maturity_badge(score_data['maturity_level'])}
                </div>
                """,
                unsafe_allow_html=True
            )
        
        st.markdown("<br>", unsafe_allow_html=True)
    
    # Recommendations
    st.markdown(
        f"""
        <div class='section-header'>
            🎯 Top Priority Recommendations
        </div>
        """,
        unsafe_allow_html=True
    )
    
    recommendations = scorer.generate_recommendations(section_scores)
    
    for idx, rec in enumerate(recommendations, 1):
        priority_colors = {
            "High": "#e7000b",
            "Medium": "#ffa500",
            "Low": "#90ee90"
        }
        
        priority_color = priority_colors.get(rec['priority'], COLORS['text'])
        
        st.markdown(
            f"""
            <div class='custom-card'>
                <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;'>
                    <h4 style='margin: 0; color: {COLORS['secondary']};'>{idx}. {rec['section']}</h4>
                    <div style='background-color: {priority_color}; color: {COLORS['background']}; padding: 5px 15px; border-radius: 15px; font-weight: bold;'>
                        {rec['priority']} Priority
                    </div>
                </div>
                <p><strong>Current Score:</strong> {rec['current_score']:.1f}%</p>
                <p><strong>Recommendation:</strong></p>
                <p style='font-size: 1.05em; line-height: 1.6;'>{rec['recommendation']}</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Next Steps
    st.markdown(
        f"""
        <div class='section-header'>
            📋 Next Steps
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown(
        f"""
        <div class='info-box'>
            <h4>What's Next?</h4>
            <ol>
                <li><strong>Share Results:</strong> Distribute this assessment with your security team and leadership</li>
                <li><strong>Prioritize Actions:</strong> Focus on high-priority recommendations first</li>
                <li><strong>Create Roadmap:</strong> Develop a 6-12 month cybersecurity improvement plan</li>
                <li><strong>Regular Assessment:</strong> Re-evaluate your posture quarterly or after major changes</li>
                <li><strong>Expert Consultation:</strong> Consider engaging cybersecurity consultants for gap analysis</li>
            </ol>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Action buttons
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🏠 Return to Home", use_container_width=True):
            # Reset session for new assessment
            for key in SESSION_KEYS.values():
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()
    
    with col2:
        if st.button("📊 View Detailed Data", use_container_width=True):
            st.session_state["show_detailed_data"] = True
            st.rerun()
    
    with col3:
        # Download report (placeholder for future PDF generation)
        st.button("📄 Download Report (Coming Soon)", use_container_width=True, disabled=True)
    
    # Show detailed data if requested
    if st.session_state.get("show_detailed_data", False):
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown(
            f"""
            <div class='section-header'>
                📈 Detailed Assessment Data
            </div>
            """,
            unsafe_allow_html=True
        )
        
        st.json({
            "company_info": st.session_state[SESSION_KEYS["company_info"]],
            "assessment_id": st.session_state[SESSION_KEYS["assessment_id"]],
            "overall_results": results,
            "total_responses": sum(len(q.values()) for q in responses.values())
        })
