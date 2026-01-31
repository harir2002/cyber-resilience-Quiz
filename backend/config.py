"""
Configuration file for Cyber Resilience Questionnaire Application
Centralizes all app settings, branding, and database configurations
"""

import os
from pathlib import Path

# ==============================
# APPLICATION SETTINGS
# ==============================
APP_TITLE = "Cyber Resilience Maturity Assessment"
APP_SUBTITLE = "Enterprise Cybersecurity Assessment Platform"
COMPANY_NAME = "SBA Info Solutions"
COMPANY_TAGLINE = "Powered by SBA Info Solutions"
VERSION = "1.0.0"

# ==============================
# BRANDING & COLORS (STRICT)
# ==============================
COLORS = {
    "primary": "#000000",      # Black
    "secondary": "#e7000b",    # Red
    "text": "#ffffff",         # White
    "background": "#000000",   # Black
    "card_bg": "#1a1a1a",     # Slightly lighter black for cards
    "border": "#e7000b",       # Red borders
    "success": "#00ff00",      # Green for success states
    "warning": "#ffa500",      # Orange for warnings
    "error": "#e7000b"         # Red for errors
}

# ==============================
# PATHS
# ==============================
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
CHROMADB_PATH = DATA_DIR / "chromadb"
ASSETS_DIR = BASE_DIR / "assets"
LOGO_PATH = ASSETS_DIR / "sba_logo.png"

# Create directories if they don't exist
DATA_DIR.mkdir(exist_ok=True)
ASSETS_DIR.mkdir(exist_ok=True)

# ==============================
# CHROMADB COLLECTIONS
# ==============================
COLLECTIONS = {
    "companies": "companies_collection",
    "questions": "questions_collection",
    "responses": "responses_collection",
    "assessments": "assessments_collection"
}

# ==============================
# COMPANY SIZE OPTIONS
# ==============================
COMPANY_SIZES = [
    "1-50 employees",
    "51-200 employees",
    "201-500 employees",
    "501-1000 employees",
    "1001-5000 employees",
    "5000+ employees"
]

# ==============================
# INDUSTRY OPTIONS
# ==============================
INDUSTRIES = [
    "Banking & Financial Services",
    "Insurance",
    "Healthcare",
    "Government",
    "Energy & Utilities",
    "Telecommunications",
    "Manufacturing",
    "Retail & E-commerce",
    "Technology",
    "Transportation & Logistics",
    "Education",
    "Other"
]

# ==============================
# REGIONS/COUNTRIES
# ==============================
REGIONS = [
    "India",
    "United States",
    "United Kingdom",
    "Canada",
    "Australia",
    "Singapore",
    "United Arab Emirates",
    "Germany",
    "France",
    "Japan",
    "China",
    "South Korea",
    "Brazil",
    "South Africa",
    "Other - Asia Pacific",
    "Other - Europe",
    "Other - Middle East",
    "Other - Americas",
    "Other - Africa"
]

# ==============================
# RESPONSE TYPES
# ==============================
RESPONSE_TYPES = {
    "yes_no_partial": ["Yes", "No", "Partial"],
    "maturity_level": ["Not Started", "Initial", "Developing", "Defined", "Managed", "Optimized"],
    "likert_5": ["1 - Strongly Disagree", "2 - Disagree", "3 - Neutral", "4 - Agree", "5 - Strongly Agree"],
    "frequency": ["Never", "Rarely", "Sometimes", "Often", "Always"]
}

# ==============================
# QUESTIONNAIRE SECTIONS
# ==============================
QUESTIONNAIRE_SECTIONS = [
    "Governance & Risk Management",
    "Asset Management",
    "Access Control & Identity Management",
    "Security Operations & Monitoring",
    "Incident Response & Recovery",
    "Data Protection & Privacy",
    "Third-Party Risk Management",
    "Security Awareness & Training"
]

# ==============================
# AI/SCORING CONFIGURATION
# ==============================
AI_CONFIG = {
    "enabled": os.getenv("AI_ENABLED", "false").lower() == "true",
    "scoring_weights": {
        "Governance & Risk Management": 0.15,
        "Asset Management": 0.10,
        "Access Control & Identity Management": 0.15,
        "Security Operations & Monitoring": 0.15,
        "Incident Response & Recovery": 0.15,
        "Data Protection & Privacy": 0.15,
        "Third-Party Risk Management": 0.10,
        "Security Awareness & Training": 0.05
    }
}

# ==============================
# SESSION STATE KEYS
# ==============================
SESSION_KEYS = {
    "current_page": "current_page",
    "company_info": "company_info",
    "responses": "responses",
    "assessment_id": "assessment_id",
    "completed_sections": "completed_sections"
}
