
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def generate_email_html(company_name, results):
    """
    Generates a clean and neat HTML email body for the assessment report (Question & Answer List)
    """
    total_score = results.get('total_score', 0)
    maturity_label = results.get('maturity_label', 'Unknown')
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 800px; margin: 0 auto; border: 1px solid #ddd; border-radius: 8px; overflow: hidden; }}
            .header {{ background-color: #000; color: #fff; padding: 20px; text-align: center; }}
            .header h1 {{ margin: 0; color: #e7000b; }}
            .content {{ padding: 20px; }}
            .qa-box {{ background-color: #f9f9f9; padding: 15px; border-radius: 8px; margin-bottom: 20px; border-left: 5px solid #e7000b; }}
            .question {{ font-size: 16px; font-weight: bold; margin-bottom: 10px; color: #000; }}
            .answer {{ background-color: #fff; padding: 10px; border: 1px solid #ddd; border-radius: 4px; color: #333; }}
            .footer {{ background-color: #f1f1f1; padding: 15px; text-align: center; font-size: 12px; color: #666; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Assessment Summary</h1>
                <p>SBA Info Solutions</p>
            </div>
            <div class="content">
                <p>Dear {company_name},</p>
                <p>Thank you for completing the Cyber Resilience Assessment. Below is a summary of your responses.</p>
                
    """
    
    # Add rows for each question
    for i, q in enumerate(results.get('question_scores', [])):
        question_text = q.get('question_text', 'Question Text Not Found')
        
        # Handle user_answer which might be a list or string
        user_answer = q.get('user_answer', 'No answer provided')
        if isinstance(user_answer, list):
            user_answer = ", ".join(user_answer)
            
        html += f"""
                <div class="qa-box">
                    <div class="question">{i+1}. {question_text}</div>
                    <div class="answer">{user_answer}</div>
                </div>
        """
        
    html += """
                <p>For further discussion, please contact our security experts.</p>
            </div>
            <div class="footer">
                <p>&copy; 2026 SBA Info Solutions. All rights reserved.</p>
                <p>www.sbainfo.in</p>
            </div>
        </div>
    </body>
    </html>
    """
    return html

def send_assessment_email(to_email, company_name, results):
    """
    Sends the assessment report via email using SBA Info Solutions SMTP or Resend API
    """
    # 1. Generate Content First (fix for 'subject not defined' error)
    subject = f"Assessment Summary - {company_name}"
    html_content = generate_email_html(company_name, results)

    # 2. Check for SendGrid API Key (Priority 1)
    # Check both standard naming and the user's specific naming 'Sendgrid_API'
    SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY") or os.getenv("Sendgrid_API")
    # Also support RESEND_API_KEY just in case user didn't switch
    RESEND_API_KEY = os.getenv("Resend_API")
    
    if SENDGRID_API_KEY:
        try:
            import requests
            logger.info("Sending email using SendGrid API...")
            
            url = "https://api.sendgrid.com/v3/mail/send"
            
            # SendGrid requires a verified sender identity
            verified_sender = "sbacyberressilence@gmail.com" 
            
            payload = {
                "personalizations": [{
                    "to": [{"email": to_email}],
                    "subject": subject
                }],
                "from": {
                    "email": verified_sender,
                    "name": "SBA Info Solutions"
                },
                "content": [{
                    "type": "text/html",
                    "value": html_content
                }]
            }
            
            headers = {
                "Authorization": f"Bearer {SENDGRID_API_KEY}",
                "Content-Type": "application/json"
            }
            
            response = requests.post(url, json=payload, headers=headers)
            
            if response.status_code in [200, 201, 202]:
                logger.info(f"Email sent successfully via SendGrid.")
                return True, "Email sent successfully via SendGrid"
            else:
                error_msg = f"SendGrid API Error {response.status_code}: {response.text}"
                logger.error(error_msg)
                return False, error_msg
                
        except Exception as e:
            logger.error(f"SendGrid Request failed: {str(e)}")
            return False, f"SendGrid Error: {str(e)}"

    # 3. Check for Resend (Priority 2 - Legacy/Backup)
    elif RESEND_API_KEY:
        try:
            import requests
            logger.info("Sending email using Resend API...")
            url = "https://api.resend.com/emails"
            payload = {
                "from": "onboarding@resend.dev",
                "to": [to_email],
                "subject": subject,
                "html": html_content
            }
            headers = {
                "Authorization": f"Bearer {RESEND_API_KEY}",
                "Content-Type": "application/json"
            }
            response = requests.post(url, json=payload, headers=headers)
            if response.status_code in [200, 201, 202]:
                return True, "Email sent via Resend"
            else:
                return False, f"Resend Error: {response.text}"
        except Exception:
            pass

    # 4. Fallback to SMTP
    # Use environment variables for credentials
    SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
    SMTP_USER = os.getenv("EMAIL_USER", "")
    SMTP_PASS = os.getenv("EMAIL_PASS", "")
    
    if not SMTP_USER or not SMTP_PASS:
        logger.error("No valid email configuration found (SendGrid, Resend, or SMTP).")
        return False, "Configuration error: No email credentials found."

    msg = MIMEMultipart()
    msg['From'] = SMTP_USER
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(html_content, 'html'))
    
    try:
        logger.info(f"Connecting to SMTP server: {SMTP_SERVER}:{SMTP_PORT}")
        
        # Use simple timeout to fail fast if blocked
        timeout = 20 # seconds

        if SMTP_PORT == 465:
            # SSL Connection
            server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, timeout=timeout)
        else:
            # TLS Connection
            server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=timeout)
            server.starttls()
            
        server.login(SMTP_USER, SMTP_PASS)
        text = msg.as_string()
        server.sendmail(SMTP_USER, to_email, text)
        server.quit()
        logger.info(f"Email sent successfully to {to_email}")
        return True, "Email sent successfully"
    except Exception as e:
        logger.error(f"Failed to send email: {str(e)}")
        return False, f"Failed to send email: {str(e)}"
