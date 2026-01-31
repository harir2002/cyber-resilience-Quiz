"""
Cyber Resilience Maturity Scoring Engine
Based on: Cyber Resilience Maturity Assessment.xlsx

Scoring System:
- 12 Questions
- 0-4 Points per question
- Maximum Score: 48 points
- 5 Maturity Levels
"""

from questionnaire.questionnaire_schema import get_questionnaire_schema, get_max_score


class ResilienceScorer:
    """Calculate cyber resilience maturity scores and generate insights"""
    
    def __init__(self):
        self.max_score = get_max_score()  # 48
        self.schema = get_questionnaire_schema()
        
    def calculate_score(self, responses):
        """
        Calculate score from responses
        
        Args:
            responses: Dict with structure {section: {question_id: {answer: ...}}}
            OR list of response objects
            
        Returns:
            {
                'total_score': int,
                'max_score': 48,
                'percentage': float,
                'maturity_level': str,
                'maturity_level_number': int,
                'risk_level': str,
                'question_scores': dict
            }
        """
        total_score = 0
        question_scores = {}
        
        # Get all questions with scoring
        all_questions = self.schema["Cyber Resilience Assessment"]
        
        # Process responses
        if isinstance(responses, dict):
            # Handle nested dict structure
            for section, section_responses in responses.items():
                if isinstance(section_responses, dict):
                    for q_id, response_data in section_responses.items():
                        score = self._score_question(q_id, response_data.get('answer', ''))
                        question_scores[q_id] = score
                        total_score += score
        elif isinstance(responses, list):
            # Handle list of responses
            for response in responses:
                q_id = response.get('question_id')
                answer = response.get('answer', '')
                score = self._score_question(q_id, answer)
                question_scores[q_id] = score
                total_score += score
        
        # Calculate percentage
        percentage = (total_score / self.max_score) * 100
        
        # Determine maturity level
        maturity_data = self._get_maturity_level(percentage)
        
        return {
            'total_score': total_score,
            'max_score': self.max_score,
            'percentage': round(percentage, 1),
            'maturity_level': maturity_data['level'],
            'maturity_level_number': maturity_data['level_number'],
            'maturity_description': maturity_data['description'],
            'risk_level': maturity_data['risk'],
            'question_scores': question_scores
        }
    
    def _score_question(self, question_id, answer):
        """Score a single question based on answer"""
        questions = self.schema["Cyber Resilience Assessment"]
        
        for q in questions:
            if q['question_id'] == question_id:
                if q['question_type'] == 'text':
                    # Special scoring for Question 8 (System Coverage Gaps)
                    return self._score_text_question(answer)
                else:
                    # Single select questions
                    return q['scoring'].get(answer, 0)
        
        return 0
    
    def _score_text_question(self, answer):
        """
        Score Question 8 (System Coverage Gaps) based on textual response
        
        Logic:
        - Empty/"None"/"N/A" = 4 points (no gaps)
        - 1-2 systems = 3 points
        - 3-5 systems = 2 points
        - 6-10 systems = 1 point
        - 10+ systems or vague answer = 0 points
        """
        answer_lower = answer.lower().strip()
        
        # Check for "no gaps" indicators
        if not answer or answer_lower in ['none', 'n/a', 'nil', 'no systems', 'all covered']:
            return 4
        
        # Count systems mentioned (simple heuristic - count commas and "and")
        system_indicators = answer.count(',') + answer.count(' and ') + answer.count(';')
        
        if system_indicators == 0 and len(answer) < 50:
            # Single system mentioned
            return 3
        elif system_indicators <= 1:
            # 1-2 systems
            return 3
        elif system_indicators <= 4:
            # 3-5 systems
            return 2
        elif system_indicators <= 9:
            # 6-10 systems
            return 1
        else:
            # Many systems or vague answer
            return 0
    
    def _get_maturity_level(self, percentage):
        """
        Determine maturity level based on percentage score
        
        Levels:
        - Level 1: Basic / Initial (0-19%)
        - Level 2: Developing (20-39%)
        - Level 3: Defined (40-60%)
        - Level 4: Managed (61-81%)
        - Level 5: Optimized (82-100%)
        """
        if percentage < 20:
            return {
                'level_number': 1,
                'level': 'Level 1: Basic / Initial',
                'description': 'Minimal cyber resilience with critical gaps',
                'risk': 'Critical'
            }
        elif percentage < 40:
            return {
                'level_number': 2,
                'level': 'Level 2: Developing',
                'description': 'Basic controls in place but significant gaps remain',
                'risk': 'High'
            }
        elif percentage < 61:
            return {
                'level_number': 3,
                'level': 'Level 3: Defined',
                'description': 'Structured and documented processes established',
                'risk': 'Moderate'
            }
        elif percentage < 82:
            return {
                'level_number': 4,
                'level': 'Level 4: Managed',
                'description': 'Measured, monitored, and largely automated',
                'risk': 'Low'
            }
        else:
            return {
                'level_number': 5,
                'level': 'Level 5: Optimized',
                'description': 'Industry-leading resilience with continuous improvement',
                'risk': 'Minimal'
            }
    
    def generate_recommendations(self, score_data):
        """
        Generate prioritized recommendations based on score
        
        Args:
            score_data: Result from calculate_score()
            
        Returns:
            List of recommendation dicts with priority, title, description
        """
        recommendations = []
        question_scores = score_data.get('question_scores', {})
        maturity_level = score_data.get('maturity_level_number', 1)
        
        # Identify low-scoring questions (0-1 points)
        critical_gaps = [(q_id, score) for q_id, score in question_scores.items() if score <= 1]
        moderate_gaps = [(q_id, score) for q_id, score in question_scores.items() if score == 2]
        
        # Critical Recommendations (High Priority)
        if critical_gaps:
            for q_id, score in critical_gaps:
                rec = self._get_question_recommendation(q_id, score, 'Critical')
                if rec:
                    recommendations.append(rec)
        
        # Moderate Recommendations
        if moderate_gaps:
            for q_id, score in moderate_gaps[:3]:  # Limit to top 3
                rec = self._get_question_recommendation(q_id, score, 'High')
                if rec:
                    recommendations.append(rec)
        
        # General maturity recommendations
        general_rec = self._get_maturity_recommendation(maturity_level)
        if general_rec:
            recommendations.append(general_rec)
        
        return recommendations
    
    def _get_question_recommendation(self, question_id, score, priority):
        """Get specific recommendation for a question"""
        recommendations_map = {
            'q1_rto': {
                'title': 'Reduce Recovery Time Objective (RTO)',
                'description': 'Your current RTO is too long. Target reducing recovery time to hours or minutes through automation and better infrastructure.'
            },
            'q2_backup_protection': {
                'title': 'Strengthen Backup Protection',
                'description': 'Implement immutability and zero-trust controls to protect backups from ransomware and unauthorized modifications.'
            },
            'q3_recovery_testing': {
                'title': 'Increase Recovery Testing Frequency',
                'description': 'Conduct quarterly (or more frequent) end-to-end recovery drills and document all results.'
            },
            'q4_incident_response': {
                'title': 'Automate Incident Response',
                'description': 'Move from manual processes to automated orchestrated response with defined playbooks and monitoring integration.'
            },
            'q5_threat_detection': {
                'title': 'Enhance Threat Detection Capabilities',
                'description': 'Implement proactive threat detection with deception sensors, anomaly detection, or AI-driven predictive systems.'
            },
            'q6_asset_coverage': {
                'title': 'Expand Critical Asset Coverage',
                'description': 'Ensure 95%+ of critical data assets have tested, validated recovery capabilities.'
            },
            'q7_recovery_confidence': {
                'title': 'Improve Recovery Confidence',
                'description': 'Increase confidence in data integrity through regular validation, testing, and verification processes.'
            },
            'q8_coverage_gaps': {
                'title': 'Address System Coverage Gaps',
                'description': 'Develop and test recovery procedures for all critical systems currently without documented processes.'
            },
            'q9_recovery_speed': {
                'title': 'Accelerate Recovery Speed',
                'description': 'Reduce time to isolate and recover compromised systems to under 4 hours through automation and improved processes.'
            },
            'q10_metrics_reporting': {
                'title': 'Implement Recovery Metrics Dashboard',
                'description': 'Deploy automated dashboards or real-time scorecards to track recovery KPIs and report to leadership.'
            },
            'q11_infrastructure_investment': {
                'title': 'Modernize Backup Infrastructure',
                'description': 'Invest in enterprise-grade, cloud-native backup infrastructure to improve resilience and recovery capabilities.'
            },
            'q12_ransomware_resilience': {
                'title': 'Verify Ransomware Recovery Capability',
                'description': 'Test and verify your ability to recover independently from ransomware without paying ransom. Aim for automated, verified recovery.'
            }
        }
        
        rec_data = recommendations_map.get(question_id)
        if rec_data:
            return {
                'priority': priority,
                'title': rec_data['title'],
                'description': rec_data['description'],
                'current_score': score,
                'target_score': 4
            }
        return None
    
    def _get_maturity_recommendation(self, maturity_level):
        """Get overall recommendation based on maturity level"""
        if maturity_level == 1:
            return {
                'priority': 'Critical',
                'title': 'Foundational Cyber Resilience Program Required',
                'description': 'Immediate action needed: Establish baseline backup procedures, implement basic immutability controls, document all recovery processes, and begin monthly testing regimen. Consider engaging cyber resilience consultants for rapid improvement.'
            }
        elif maturity_level == 2:
            return {
                'priority': 'High',
                'title': 'Accelerate to Defined Maturity Level',
                'description': 'Focus on: Increasing testing frequency to quarterly, implementing immutability + air-gap protection, automating alerting mechanisms, and expanding asset coverage to 85%+.'
            }
        elif maturity_level == 3:
            return {
                'priority': 'Medium',
                'title': 'Advance Toward Managed State',
                'description': 'Next steps: Introduce automation in response workflows, implement deception/anomaly detection, target 95%+ asset coverage, reduce recovery time to hours, and add real-time monitoring dashboards.'
            }
        elif maturity_level == 4:
            return {
                'priority': 'Low',
                'title': 'Optimize for Industry Leadership',
                'description': 'Continue improving: Achieve 95-100% validated asset coverage, implement AI-driven threat prediction, automate full recovery orchestration, target sub-hour recovery times, deploy continuous automated validation.'
            }
        else:  # Level 5
            return {
                'priority': 'Low',
                'title': 'Maintain Excellence and Continuous Improvement',
                'description': 'Sustain your industry-leading position through continuous improvement programs, industry benchmarking, advanced threat intelligence integration, regular executive reviews, and longitudinal maturity tracking.'
            }
    
    def get_result_summary(self, score_data):
        """Generate customer-facing result summary text"""
        percentage = score_data['percentage']
        level = score_data['maturity_level']
        risk = score_data['risk_level']
        total = score_data['total_score']
        max_score = score_data['max_score']
        
        # Generate personalized summary
        if percentage >= 82:
            summary = f"Your organization demonstrates **industry-leading cyber resilience** with an overall maturity score of **{percentage}%** ({level}). Your backup and recovery infrastructure is well-protected, automated, and continuously validated. You have verified capability to recover independently from ransomware attacks within minutes to hours, with high confidence in data integrity."
        elif percentage >= 61:
            summary = f"Your organization shows **strong cyber resilience** with an overall maturity score of **{percentage}%** ({level}). You have implemented automated response workflows, multi-layer immutability controls, and regular testing. Recovery times are measured in hours with high asset coverage. Continue advancing toward full automation and 100% asset validation."
        elif percentage >= 40:
            summary = f"Your organization has established a **solid foundation** for cyber resilience with an overall maturity score of **{percentage}%** ({level}). Recovery procedures are documented and tested, with immutability controls in place. Focus on increasing automation, expanding asset coverage to 95%+, and reducing recovery times from days to hours."
        elif percentage >= 20:
            summary = f"Your organization is in the **early stages** of cyber resilience maturity with an overall maturity score of **{percentage}%** ({level}). While basic controls and documentation exist, significant gaps remain in testing frequency, automation, and asset coverage. Prioritize implementing immutability, increasing testing to quarterly, and documenting all recovery procedures."
        else:
            summary = f"Your organization faces **critical cyber resilience gaps** with an overall maturity score of **{percentage}%** ({level}). Recovery processes are largely manual and untested, with extended RTO measured in days or weeks. **Immediate action required:** Establish baseline backup procedures, implement immutability controls, document recovery processes, and begin regular testing."
        
        return {
            'summary': summary,
            'score': f"{total}/{max_score}",
            'percentage': f"{percentage}%",
            'level': level,
            'risk': risk
        }
