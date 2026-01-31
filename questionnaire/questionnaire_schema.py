"""
Cyber Resilience Maturity Assessment Questionnaire Schema
Based on: Cyber Resilience Maturity Assessment.xlsx
12 Strategic Questions - 0-4 Point Scoring Scale
"""

def get_questionnaire_schema():
    """
    Returns the complete questionnaire structure with all 12 questions
    Organized as a single unified assessment
    """
    
    questionnaire = {
        "Cyber Resilience Assessment": [
            {
                "question_id": "q1_rto",
                "domain": "Recovery Time Objective",
                "question_text": "What is the current maximum recovery time your organization can tolerate without material business impact (RTO)?",
                "question_type": "single_select",
                "options": [
                    "Days/Weeks",
                    "Days",
                    "12-24 hours",
                    "Hours",
                    "Minutes"
                ],
                "scoring": {
                    "Days/Weeks": 0,
                    "Days": 1,
                    "12-24 hours": 2,
                    "Hours": 3,
                    "Minutes": 4
                },
                "help_text": "L1: Days/Weeks | L2: Days | L3: 12-24 hrs | L4: Hours | L5: Minutes",
                "required": True
            },
            {
                "question_id": "q2_backup_protection",
                "domain": "Data Protection & Immutability",
                "question_text": "How are your backup systems currently protected from unauthorized access, modification, or deletion by attackers?",
                "question_type": "single_select",
                "options": [
                    "Network isolation only",
                    "Role-based controls",
                    "Immutability + Air-gap",
                    "Immutability + Multi-layer",
                    "Zero-trust immutable"
                ],
                "scoring": {
                    "Network isolation only": 0,
                    "Role-based controls": 1,
                    "Immutability + Air-gap": 2,
                    "Immutability + Multi-layer": 3,
                    "Zero-trust immutable": 4
                },
                "help_text": "L1: Network isolation only | L2: Role-based controls | L3: Immutability + Air-gap | L4: Immutability + Multi-layer | L5: Zero-trust immutable",
                "required": True
            },
            {
                "question_id": "q3_recovery_testing",
                "domain": "Recovery Testing & Validation",
                "question_text": "In the past 12 months, how many unplanned data recovery scenarios has your organization tested end-to-end?",
                "question_type": "single_select",
                "options": [
                    "None",
                    "1 drill in past 12mo",
                    "2-3 drills",
                    "Quarterly + documented",
                    "Continuous automated"
                ],
                "scoring": {
                    "None": 0,
                    "1 drill in past 12mo": 1,
                    "2-3 drills": 2,
                    "Quarterly + documented": 3,
                    "Continuous automated": 4
                },
                "help_text": "L1: None | L2: 1 drill | L3: 2-3 drills | L4: Quarterly + documented | L5: Continuous automated validation",
                "required": True
            },
            {
                "question_id": "q4_incident_response",
                "domain": "Incident Response Orchestration",
                "question_text": "When a potential cyber incident is detected today, how is the incident response coordinated and executed?",
                "question_type": "single_select",
                "options": [
                    "Manual ad-hoc process",
                    "Documented playbook only",
                    "Playbook + assigned roles",
                    "Playbook + monitoring alerts",
                    "Automated orchestrated response"
                ],
                "scoring": {
                    "Manual ad-hoc process": 0,
                    "Documented playbook only": 1,
                    "Playbook + assigned roles": 2,
                    "Playbook + monitoring alerts": 3,
                    "Automated orchestrated response": 4
                },
                "help_text": "L1: Manual ad-hoc process | L2: Documented playbook only | L3: Playbook + assigned roles | L4: Playbook + monitoring alerts | L5: Automated orchestrated response",
                "required": True
            },
            {
                "question_id": "q5_threat_detection",
                "domain": "Threat Detection Capability",
                "question_text": "How is your organization currently detecting signs of compromise BEFORE data loss actually occurs?",
                "question_type": "single_select",
                "options": [
                    "Logs reviewed post-incident",
                    "Basic alerting on backups",
                    "Threat-aware monitoring",
                    "Deception sensors + anomaly",
                    "AI-driven predictive detection"
                ],
                "scoring": {
                    "Logs reviewed post-incident": 0,
                    "Basic alerting on backups": 1,
                    "Threat-aware monitoring": 2,
                    "Deception sensors + anomaly": 3,
                    "AI-driven predictive detection": 4
                },
                "help_text": "L1: Logs reviewed post-incident | L2: Basic alerting on backups | L3: Threat-aware monitoring | L4: Deception sensors + anomaly | L5: AI-driven predictive detection",
                "required": True
            },
            {
                "question_id": "q6_asset_coverage",
                "domain": "Critical Asset Coverage",
                "question_text": "What percentage of your critical data assets are covered under your current recovery capability?",
                "question_type": "single_select",
                "options": [
                    "40-60%",
                    "60-75%",
                    "75-85%",
                    "85-95%",
                    "95-100% + validated"
                ],
                "scoring": {
                    "40-60%": 0,
                    "60-75%": 1,
                    "75-85%": 2,
                    "85-95%": 3,
                    "95-100% + validated": 4
                },
                "help_text": "L1: 40-60% | L2: 60-75% | L3: 75-85% | L4: 85-95% | L5: 95-100% + validated",
                "required": True
            },
            {
                "question_id": "q7_recovery_confidence",
                "domain": "Recovery Confidence",
                "question_text": "If you were to recover your entire organization's data today, how confident are you in the integrity and completeness?",
                "question_type": "single_select",
                "options": [
                    "30-40% confident",
                    "40-60% confident",
                    "60-75% confident",
                    "75-90% confident",
                    "90-100% confident"
                ],
                "scoring": {
                    "30-40% confident": 0,
                    "40-60% confident": 1,
                    "60-75% confident": 2,
                    "75-90% confident": 3,
                    "90-100% confident": 4
                },
                "help_text": "L1: 30-40% | L2: 40-60% | L3: 60-75% | L4: 75-90% | L5: 90-100%",
                "required": True
            },
            {
                "question_id": "q8_coverage_gaps",
                "domain": "System Coverage Gaps",
                "question_text": "Which critical systems or data sources do NOT have a tested, documented recovery procedure?",
                "question_type": "text",
                "options": [],
                "scoring": {
                    # Qualitative - scored based on response analysis
                    # Empty/"None"/"N/A" = 4 points
                    # 1-2 systems = 3 points
                    # 3-5 systems = 2 points
                    # 6-10 systems = 1 point
                    # 10+ systems or vague answer = 0 points
                },
                "help_text": "List specific systems or write 'None' if all systems are covered. Number of systems without coverage indicates maturity gap.",
                "required": True
            },
            {
                "question_id": "q9_recovery_speed",
                "domain": "Recovery Speed",
                "question_text": "In your current setup, how much time would it take to isolate a compromised system and recover to a known-clean state?",
                "question_type": "single_select",
                "options": [
                    "1-2 weeks",
                    "3-7 days",
                    "24-48 hours",
                    "4-12 hours",
                    "Under 1 hour automated"
                ],
                "scoring": {
                    "1-2 weeks": 0,
                    "3-7 days": 1,
                    "24-48 hours": 2,
                    "4-12 hours": 3,
                    "Under 1 hour automated": 4
                },
                "help_text": "L1: 1-2 weeks | L2: 3-7 days | L3: 24-48 hours | L4: 4-12 hours | L5: Under 1 hour automated",
                "required": True
            },
            {
                "question_id": "q10_metrics_reporting",
                "domain": "Metrics & Reporting",
                "question_text": "How are recovery validations and post-incident metrics tracked and reported to leadership?",
                "question_type": "single_select",
                "options": [
                    "Not tracked",
                    "Manual post-mortems",
                    "Recovery reports",
                    "Automated dashboards",
                    "Real-time exec scorecard"
                ],
                "scoring": {
                    "Not tracked": 0,
                    "Manual post-mortems": 1,
                    "Recovery reports": 2,
                    "Automated dashboards": 3,
                    "Real-time exec scorecard": 4
                },
                "help_text": "L1: Not tracked | L2: Manual post-mortems | L3: Recovery reports | L4: Automated dashboards | L5: Real-time exec scorecard",
                "required": True
            },
            {
                "question_id": "q11_infrastructure_investment",
                "domain": "Infrastructure Investment",
                "question_text": "What level of investment has been made in backup infrastructure over the past 24 months?",
                "question_type": "single_select",
                "options": [
                    "Minimal/legacy",
                    "Basic upgrades",
                    "Moderate modernization",
                    "Significant investment",
                    "Enterprise-grade cloud-native"
                ],
                "scoring": {
                    "Minimal/legacy": 0,
                    "Basic upgrades": 1,
                    "Moderate modernization": 2,
                    "Significant investment": 3,
                    "Enterprise-grade cloud-native": 4
                },
                "help_text": "L1: Minimal/legacy | L2: Basic upgrades | L3: Moderate modernization | L4: Significant investment | L5: Enterprise-grade cloud-native",
                "required": True
            },
            {
                "question_id": "q12_ransomware_resilience",
                "domain": "Ransomware Resilience",
                "question_text": "If ransomware locked all your systems today, could your organization recover independently without paying ransom?",
                "question_type": "single_select",
                "options": [
                    "Uncertain",
                    "Possibly with manual effort",
                    "Yes, with 48+ hours",
                    "Yes, within hours",
                    "Yes, verified automated recovery"
                ],
                "scoring": {
                    "Uncertain": 0,
                    "Possibly with manual effort": 1,
                    "Yes, with 48+ hours": 2,
                    "Yes, within hours": 3,
                    "Yes, verified automated recovery": 4
                },
                "help_text": "L1: Uncertain | L2: Possibly with manual effort | L3: Yes, with 48+ hours | L4: Yes, within hours | L5: Yes, verified automated recovery",
                "required": True
            }
        ]
    }
    
    return questionnaire


def get_question_count():
    """Returns total number of questions"""
    schema = get_questionnaire_schema()
    return sum(len(questions) for questions in schema.values())


def get_max_score():
    """Returns maximum possible score (12 questions × 4 points)"""
    return 48


def get_sections():
    """Returns list of section names"""
    return list(get_questionnaire_schema().keys())
