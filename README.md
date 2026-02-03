# Cyber Resilience Maturity Assessment Platform

## 🎯 Overview

A production-ready **Cyber Resilience Questionnaire Application** built with a **React (Vite)** frontend and **FastAPI** backend. This platform allows organizations to evaluate their cyber resilience maturity across critical security domains and receive actionable insights via email reports.

---

## 🚀 Features

### ✅ **Core Functionality**
- **Dynamic Questionnaire**: Covering multiple cybersecurity domains with single and multi-select questions.
- **Real-time Progress Tracking**: visual percentage bar and question counter.
- **Company Information Collection**: Securely captures organization details.
- **Automated Email Reports**: instantly sends a summary of responses to the client using SBA Info Solutions SMTP.
- **User Response Review**: Allows users to review all answers before submission.

### 🎨 **Premium UI/UX**
- **Custom Branding**: Professional Black (#000000), Red (#e7000b), and White (#ffffff) color scheme.
- **Responsive Design**: fully responsive layout for all devices.
- **Interactive Elements**: Hover effects, smooth transitions, and dynamic form inputs.
- **Clear Guidance**: "Choose multiple options" indicators for multi-select questions.

### 🔒 **Security & Architecture**
- **Modern Stack**: React 18, Vite, FastAPI, Pydantic.
- **Secure Configuration**: Environment variables for sensitive credentials.
- **Robust Error Handling**: Graceful degradation and user-friendly error messages.

---

## 📁 Project Structure

```
cyber-resilience-assessment/
├── frontend/                       # React Frontend
│   ├── src/
│   │   ├── pages/                  # Application Pages (Landing, Questionnaire, Results)
│   │   ├── components/             # Reusable UI components
│   │   └── config.js               # Frontend configuration
│   ├── package.json                # JS dependencies
│   └── vite.config.js              # Vite configuration
│
├── backend/                        # FastAPI Backend
│   ├── main.py                     # API Entry point
│   ├── questionnaire/
│   │   └── questionnaire_schema.py # Dynamic Question Schema
│   ├── utils/
│   │   ├── email_sender.py         # Email notification logic
│   │   └── scoring.py              # Scoring logic
│   ├── requirements.txt            # Python dependencies
│   └── .env                        # Environment variables (SMTP credentials)
```

---

## 🛠️ Installation & Setup

### **Prerequisites**
- Node.js (v16+)
- Python (v3.9+)

### **1. Backend Setup**

Navigate to the backend directory:
```bash
cd backend
```

Install Python dependencies:
```bash
pip install -r requirements.txt
```

Create a `.env` file in the `backend/` directory with your SMTP credentials:
```env
SMTP_SERVER=mail.sbainfo.in
SMTP_PORT=587
EMAIL_USER=your_email@sbainfo.in
EMAIL_PASS=your_password
```

Run the backend server:
```bash
python main.py
```
*The backend runs on http://localhost:8000*

### **2. Frontend Setup**

Navigate to the frontend directory:
```bash
cd frontend
```

Install Node dependencies:
```bash
npm install
```

Run the development server:
```bash
npm run dev
```
*The frontend runs on http://localhost:5173*

---

## 📧 Email Configuration

The application uses `nodemailer` style SMTP configuration in Python. Ensure your `.env` file credentials are valid for `mail.sbainfo.in`. The system automatically handles TLS encryption.

---

## 🎨 Design System

- **Primary Background**: Black (`#000000`)
- **Secondary Background**: Dark Gray (`#1a1a1a`)
- **Accent Color**: SBA Red (`#e7000b`)
- **Success Color**: Green (`#00ff00`)
- **Text Color**: White (`#ffffff`)

---

## 📞 Support

For support or feature requests, contact SBA Info Solutions.
**Website**: [https://www.sbainfo.in](https://www.sbainfo.in)
