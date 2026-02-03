"""
Cyber Resilience Maturity Assessment Questionnaire Schema
Based on: Cyber Resilience Maturity Assessment - New.xlsx
Generated dynamically
"""

def get_questionnaire_schema():
    """
    Returns the complete questionnaire structure
    Organized as a single unified assessment
    """
    
    questionnaire = {
        "Cyber Resilience Assessment": [
            {
                        "question_id": "q1a",
                        "domain": "Cyber Resilience",
                        "question_text": "What is the current maximum recovery time your organisation can tolerate without material business impact (RTO)?",
                        "question_type": "single_select",
                        "options": [
                                    "Days/Weeks",
                                    "Days",
                                    "12-24 hrs",
                                    "Hours",
                                    "Minutes",
                                    "No idea"
                        ],
                        "scoring": {
                                    "Days/Weeks": 0,
                                    "Days": 1,
                                    "12-24 hrs": 2,
                                    "Hours": 3,
                                    "Minutes": 4,
                                    "No idea": 0
                        },
                        "help_text": "Question 1a (Informational)",
                        "required": True
            },
            {
                        "question_id": "q1b",
                        "domain": "Cyber Resilience",
                        "question_text": "What is the data point in time that the organisation can withstand without business productivity loss (RPO) ?",
                        "question_type": "single_select",
                        "options": [
                                    "0 hrs",
                                    "1 day",
                                    "1 week",
                                    "1 month",
                                    "Not applicable",
                                    "No idea"
                        ],
                        "scoring": {
                                    "0 hrs": 0,
                                    "1 day": 1,
                                    "1 week": 2,
                                    "1 month": 3,
                                    "Not applicable": 0,
                                    "No idea": 0
                        },
                        "help_text": "Question 1b (Informational)",
                        "required": True
            },
            {
                        "question_id": "q2",
                        "domain": "Cyber Resilience",
                        "question_text": "How are your backup systems currently protected from unauthorised access, modification, or deletion by attackers?",
                        "question_type": "multi_select",
                        "options": [
                                    "Network isolation only",
                                    "Role-based controls",
                                    "Immutability + Air-gap",
                                    "Immutability + Tape",
                                    "Zero-trust immutable",
                                    "No idea"
                        ],
                        "scoring": {
                                    "Network isolation only": 0,
                                    "Role-based controls": 1,
                                    "Immutability + Air-gap": 2,
                                    "Immutability + Tape": 3,
                                    "Zero-trust immutable": 4,
                                    "No idea": 0
                        },
                        "help_text": "Question 2 (L3)",
                        "required": True
            },
            {
                        "question_id": "q3",
                        "domain": "Cyber Resilience",
                        "question_text": "In the past 12 months, how many unplanned data recovery scenarios has your organisation tested end-to-end operationally?",
                        "question_type": "single_select",
                        "options": [
                                    "1 drill annually",
                                    "2-3 drills annually",
                                    "Quarterly + documented",
                                    "Continuous automated validation",
                                    "No idea"
                        ],
                        "scoring": {
                                    "1 drill annually": 0,
                                    "2-3 drills annually": 1,
                                    "Quarterly + documented": 2,
                                    "Continuous automated validation": 3,
                                    "No idea": 0
                        },
                        "help_text": "Question 3 (L4)",
                        "required": True
            },
            {
                        "question_id": "q3f",
                        "domain": "Cyber Resilience",
                        "question_text": "Does the above operational drill ensures that the recovered data is threat free.",
                        "question_type": "single_select",
                        "options": [
                                    "Yes",
                                    "No"
                        ],
                        "scoring": {
                                    "Yes": 0,
                                    "No": 1
                        },
                        "help_text": "Question 3f (L5)",
                        "required": True
            },
            {
                        "question_id": "q4",
                        "domain": "Cyber Resilience",
                        "question_text": "When a potential cyber incident is detected today, how is the incident response coordinated and executed?",
                        "question_type": "single_select",
                        "options": [
                                    "Manual ad-hoc process",
                                    "Documented playbook only",
                                    "Playbook + assigned roles",
                                    "Playbook + monitoring alerts",
                                    "Automated orchestrated response",
                                    "No idea"
                        ],
                        "scoring": {
                                    "Manual ad-hoc process": 0,
                                    "Documented playbook only": 1,
                                    "Playbook + assigned roles": 2,
                                    "Playbook + monitoring alerts": 3,
                                    "Automated orchestrated response": 4,
                                    "No idea": 0
                        },
                        "help_text": "Question 4 (Informational)",
                        "required": True
            },
            {
                        "question_id": "q4f",
                        "domain": "Cyber Resilience",
                        "question_text": "Does the above incident response considers ensures that the recovered data is free from threats",
                        "question_type": "single_select",
                        "options": [
                                    "Yes",
                                    "No"
                        ],
                        "scoring": {
                                    "Yes": 0,
                                    "No": 1
                        },
                        "help_text": "Question 4f (L5)",
                        "required": True
            },
            {
                        "question_id": "q5",
                        "domain": "Cyber Resilience",
                        "question_text": "How is your organisation currently detecting signs of compromise BEFORE data breach actually occurs?",
                        "question_type": "multi_select",
                        "options": [
                                    "Logs reviewed post-incident",
                                    "Basic alerting on backups",
                                    "Threat-aware monitoring",
                                    "Deception sensors + anomaly (Honeypots)",
                                    "AI-driven predictive detection",
                                    "No idea"
                        ],
                        "scoring": {
                                    "Logs reviewed post-incident": 0,
                                    "Basic alerting on backups": 1,
                                    "Threat-aware monitoring": 2,
                                    "Deception sensors + anomaly (Honeypots)": 3,
                                    "AI-driven predictive detection": 4,
                                    "No idea": 0
                        },
                        "help_text": "Question 5 (L5)",
                        "required": True
            },
            {
                        "question_id": "q6",
                        "domain": "Cyber Resilience",
                        "question_text": "What percentage of your critical data assets are covered under your current recovery capability?\n(including mail, endpoint, AD, Applications & servers, Cloud, Containers, etc)",
                        "question_type": "single_select",
                        "options": [
                                    "0-60%",
                                    "60-75%",
                                    "75-85%",
                                    "85-95%",
                                    "95-100% + validated",
                                    "No idea"
                        ],
                        "scoring": {
                                    "0-60%": 0,
                                    "60-75%": 1,
                                    "75-85%": 2,
                                    "85-95%": 3,
                                    "95-100% + validated": 4,
                                    "No idea": 0
                        },
                        "help_text": "Question 6 (L1)",
                        "required": True
            },
            {
                        "question_id": "q7",
                        "domain": "Cyber Resilience",
                        "question_text": "If you were to bring your business online quickly, how confident are you in the integrity and completeness with clean data?",
                        "question_type": "single_select",
                        "options": [
                                    "< 40%",
                                    "40-60%",
                                    "60-75%",
                                    "75-90%",
                                    "90-100%",
                                    "No idea"
                        ],
                        "scoring": {
                                    "< 40%": 0,
                                    "40-60%": 1,
                                    "60-75%": 2,
                                    "75-90%": 3,
                                    "90-100%": 4,
                                    "No idea": 0
                        },
                        "help_text": "Question 7 (Informational)",
                        "required": True
            },
            {
                        "question_id": "q7f",
                        "domain": "Cyber Resilience",
                        "question_text": "For the above, to maintain your minimal viable services to bring back your business online, what would be the current timeline",
                        "question_type": "single_select",
                        "options": [
                                    "1-2 weeks",
                                    "3-7 days",
                                    "24-48 hours",
                                    "4-12 hours",
                                    "Under 1 hour automated",
                                    "No idea"
                        ],
                        "scoring": {
                                    "1-2 weeks": 0,
                                    "3-7 days": 1,
                                    "24-48 hours": 2,
                                    "4-12 hours": 3,
                                    "Under 1 hour automated": 4,
                                    "No idea": 0
                        },
                        "help_text": "Question 7f (Informational)",
                        "required": True
            },
            {
                        "question_id": "q8",
                        "domain": "Cyber Resilience",
                        "question_text": "Which critical systems or data sources do NOT have a tested, documented recovery procedure?",
                        "question_type": "text",
                        "options": [
                                    "Scoring: Number of systems without coverage indicates maturity gap"
                        ],
                        "scoring": {},
                        "help_text": "Question 8 (L3)",
                        "required": True
            },
            {
                        "question_id": "q9",
                        "domain": "Cyber Resilience",
                        "question_text": "How are recovery validations and post-incident metrics tracked and reported to leadership?",
                        "question_type": "single_select",
                        "options": [
                                    "Not tracked",
                                    "Manual post-mortems",
                                    "Recovery reports",
                                    "Automated dashboards",
                                    "Real-time exec scorecard",
                                    "No idea"
                        ],
                        "scoring": {
                                    "Not tracked": 0,
                                    "Manual post-mortems": 1,
                                    "Recovery reports": 2,
                                    "Automated dashboards": 3,
                                    "Real-time exec scorecard": 4,
                                    "No idea": 0
                        },
                        "help_text": "Question 9 (L4)",
                        "required": True
            },
            {
                        "question_id": "q10",
                        "domain": "Cyber Resilience",
                        "question_text": "What level of investment has been made in backup infrastructure over the past 24 months?",
                        "question_type": "single_select",
                        "options": [
                                    "Minimal/legacy",
                                    "Basic upgrades",
                                    "Moderate modernisation",
                                    "Significant investment",
                                    "Enterprise-grade cloud-native",
                                    "No idea"
                        ],
                        "scoring": {
                                    "Minimal/legacy": 0,
                                    "Basic upgrades": 1,
                                    "Moderate modernisation": 2,
                                    "Significant investment": 3,
                                    "Enterprise-grade cloud-native": 4,
                                    "No idea": 0
                        },
                        "help_text": "Question 10 (Informational)",
                        "required": True
            },
            {
                        "question_id": "q11",
                        "domain": "Cyber Resilience",
                        "question_text": "What is your current backup strategy in terms of no. Of copies of backup, media used for storing & its storage site",
                        "question_type": "text",
                        "options": [],
                        "scoring": {},
                        "help_text": "Question 11 (L2)",
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
    """Returns maximum possible score (calculated: 44)"""
    return 44


def get_sections():
    """Returns list of section names"""
    return list(get_questionnaire_schema().keys())
