# Cyber Resilience Maturity Assessment Platform

## 🎯 Overview

A production-ready **Cyber Resilience Questionnaire Application** built with **Streamlit** and **ChromaDB** for enterprise cybersecurity assessments. This platform allows organizations to evaluate their cyber resilience maturity across 8 critical security domains and receive actionable insights.

---

## 🚀 Features

### ✅ **Core Functionality**
- **Multi-section questionnaire** covering 8 cybersecurity domains (40+ questions)
- **Company information collection** with validation
- **Real-time progress tracking** across all sections
- **ChromaDB integration** for persistent data storage
- **Automated scoring** with maturity level calculation
- **Interactive results dashboard** with radar chart visualization
- **AI-ready architecture** for future LLM integration

### 🎨 **Premium UI/UX**
- **Custom branding**: Black (#000000), Red (#e7000b), White (#ffffff) color scheme
- **Enterprise-grade design** suitable for BFSI and critical infrastructure
- **Responsive layout** with intuitive navigation
- **Progress indicators** and completion tracking
- **Interactive visualizations** using Plotly

### 🔒 **Security & Compliance**
- **Input validation** for all form fields
- **Session-based state management**
- **Secure data storage** with ChromaDB
- **GDPR-friendly** data handling assumptions
- **No hard-coded secrets**

---

## 📁 Project Structure

```
cyber-resilience-assessment/
├── app.py                          # Main application entry point
├── config.py                       # Configuration and settings
├── requirements.txt                # Python dependencies
├── .env.example                    # Environment variables template
├── .gitignore                      # Git ignore rules
│
├── database/
│   ├── __init__.py
│   └── chromadb_manager.py         # ChromaDB operations manager
│
├── questionnaire/
│   ├── __init__.py
│   └── questionnaire_schema.py     # Assessment questions schema
│
├── utils/
│   ├── __init__.py
│   ├── scoring.py                  # Scoring and analytics engine
│   └── ui_components.py            # Reusable UI components
│
├── pages/
│   ├── __init__.py
│   ├── landing.py                  # Landing page
│   ├── company_info.py             # Company information collection
│   ├── questionnaire.py            # Main questionnaire
│   ├── review.py                   # Response review page
│   └── results.py                  # Results and recommendations
│
├── data/                           # ChromaDB storage (auto-created)
│   └── chromadb/
│
└── assets/                         # Static assets (auto-created)
    └── logo.png
```

---

## 🛠️ Installation & Setup

### **Prerequisites**
- Python 3.8 or higher
- pip package manager

### **Step 1: Install Dependencies**

```bash
pip install -r requirements.txt
```

### **Step 2: Configure Environment (Optional)**

Copy the example environment file:

```bash
copy .env.example .env
```

Edit `.env` to customize settings:
- `CHROMADB_PATH`: Database location (default: `./data/chromadb`)
- `AI_ENABLED`: Enable AI features (default: `false`)

### **Step 3: Run the Application**

```bash
streamlit run app.py
```

The application will launch at `http://localhost:8501`

---

## 📊 Assessment Domains

The questionnaire evaluates cyber resilience across **8 critical domains**:

1. **🏛️ Governance & Risk Management**
   - Cybersecurity strategy and policies
   - Risk assessment programs
   - Executive leadership and oversight

2. **💼 Asset Management**
   - IT asset inventory and classification
   - Lifecycle management
   - Critical asset identification

3. **🔐 Access Control & Identity Management**
   - Multi-factor authentication
   - Role-based access control
   - Privileged access management

4. **🔍 Security Operations & Monitoring**
   - SOC capabilities
   - Threat detection and monitoring
   - Vulnerability management

5. **🚨 Incident Response & Recovery**
   - IR plans and procedures
   - Business continuity and disaster recovery
   - Backup strategies

6. **🔒 Data Protection & Privacy**
   - Data classification and encryption
   - Privacy compliance (GDPR, CCPA)
   - Data loss prevention

7. **🤝 Third-Party Risk Management**
   - Vendor security assessments
   - Supply chain risk management
   - Contract security requirements

8. **🎓 Security Awareness & Training**
   - Employee awareness programs
   - Phishing simulations
   - Role-based security training

---

## 🎯 Scoring Methodology

### **Maturity Levels**
- **Not Started** (0-10%)
- **Initial** (10-30%)
- **Developing** (30-50%)
- **Defined** (50-70%)
- **Managed** (70-85%)
- **Optimized** (85-100%)

### **Risk Levels**
- **Critical** (<25%)
- **High** (25-50%)
- **Medium** (50-75%)
- **Low** (75%+)

### **Weighted Scoring**
Sections are weighted based on industry best practices:
- Governance & Risk Management: 15%
- Access Control & IAM: 15%
- Security Operations: 15%
- Incident Response: 15%
- Data Protection: 15%
- Asset Management: 10%
- Third-Party Risk: 10%
- Security Awareness: 5%

---

## 🔌 ChromaDB Integration

### **Collections**

1. **Companies**: Organization information
2. **Questions**: Questionnaire schema
3. **Responses**: User answers and comments
4. **Assessments**: Assessment metadata and status

### **Data Storage**

All data is persisted locally in the `./data/chromadb` directory. Data includes:
- Company profiles
- Assessment responses with timestamps
- Historical assessments for trend analysis
- Metadata for future AI embeddings

---

## 🤖 AI-Ready Architecture

The application is designed to support future AI/LLM integration:

### **Planned AI Features**
- ✨ **Personalized recommendations** using LLM analysis
- 📈 **Predictive scoring** based on industry trends
- 🔍 **Gap analysis** with peer benchmarking
- 📝 **Automated report generation** (PDF/Word)
- 💬 **Natural language insights**

### **Implementation Hooks**
- Modular scoring engine in `utils/scoring.py`
- ChromaDB vector embeddings support
- Configuration flags in `config.py` (`AI_ENABLED`)
- Response data structured for LLM consumption

---

## 🚢 Deployment

### **Local Deployment**
```bash
streamlit run app.py
```

### **Docker Deployment (Recommended)**

Create a `Dockerfile`:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

Build and run:

```bash
docker build -t cyber-resilience-app .
docker run -p 8501:8501 -v $(pwd)/data:/app/data cyber-resilience-app
```

### **Cloud Deployment**

#### **AWS / Azure / IBM Cloud**

1. **AWS Elastic Beanstalk**: Deploy using Docker configuration
2. **Azure App Service**: Deploy as container or Python web app
3. **IBM Cloud Foundry**: Use Python buildpack
4. **Streamlit Cloud**: Push to GitHub and deploy directly

#### **Environment Variables**
Set the following in your cloud provider:
```
CHROMADB_PATH=/app/data/chromadb
AI_ENABLED=false
```

---

## 🔐 Security Best Practices

### **For Production Deployment**

1. **Enable HTTPS**: Use reverse proxy (Nginx/Apache) with SSL certificates
2. **Authentication**: Add authentication layer (OAuth, SAML, etc.)
3. **Database Encryption**: Encrypt ChromaDB storage at rest
4. **Input Sanitization**: Already implemented in form validation
5. **Rate Limiting**: Implement API rate limiting
6. **Audit Logging**: Enable detailed audit trails
7. **Backup Strategy**: Regular automated backups of ChromaDB data

### **Compliance Considerations**

- **GDPR**: Data minimization, consent management, right to erasure
- **SOC 2**: Access controls, encryption, audit logging
- **ISO 27001**: Information security management alignment
- **NIST CSF**: Framework mapping in questionnaire design

---

## 📈 Usage Workflow

### **For Organizations**

1. **Access Application**: Navigate to the hosted URL
2. **Start Assessment**: Click "Start Assessment" button
3. **Enter Company Details**: Provide organization information
4. **Complete Questionnaire**: Answer questions across 8 domains
5. **Review Responses**: Verify all answers before submission
6. **View Results**: Analyze maturity scores and recommendations
7. **Download Report**: Export results (future feature)

### **For Administrators**

- **Access ChromaDB**: Query assessments and analytics
- **Monitor Usage**: Track assessment completion rates
- **Generate Reports**: Extract insights across organizations
- **Customize Questions**: Modify `questionnaire_schema.py`

---

## 🛠️ Customization

### **Branding**

Edit `config.py` to change colors:

```python
COLORS = {
    "primary": "#000000",      # Your primary color
    "secondary": "#e7000b",    # Your accent color
    "text": "#ffffff",         # Text color
}
```

### **Questions**

Modify `questionnaire/questionnaire_schema.py` to:
- Add/remove sections
- Customize questions
- Change response types
- Update help text

### **Scoring Weights**

Adjust section weights in `config.py`:

```python
"scoring_weights": {
    "Governance & Risk Management": 0.20,  # Increase weight
    # ... other sections
}
```

---

## 📞 Support & Contact

For questions, issues, or enterprise support:

- **Email**: hariktm05@gmail.com
- **GitHub**: [@Hariktm](https://github.com/Hariktm)

---

## 📜 License

This project is proprietary software developed for enterprise use. Contact the author for licensing information.

---

## 🙏 Acknowledgments

- **NIST Cybersecurity Framework** - Question design inspiration
- **ISO 27001** - Security controls mapping
- **CIS Controls** - Best practices alignment
- **Streamlit** - Application framework
- **ChromaDB** - Vector database solution

---

**Built with ❤️ for Enterprise Cyber Resilience**
