"""
Email Service Module

This module handles sending emails for various NGO events:
- Donation confirmations
- Volunteer application notifications
- Contact form responses
- Admin notifications

Configuration:
Add the following environment variables to .env:
- EMAIL_PROVIDER: 'smtp' or 'sendgrid' (default: 'smtp')
- SMTP_SERVER: 'smtp.gmail.com' (for Gmail)
- SMTP_PORT: 587 (for Gmail)
- SENDER_EMAIL: your-email@gmail.com
- SENDER_PASSWORD: your-app-password (use App Passwords for Gmail)
- SENDGRID_API_KEY: your-sendgrid-api-key
"""

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional, List
from dotenv import load_dotenv

load_dotenv()


class EmailService:
    """Email service for sending notifications"""
    
    def __init__(self):
        self.provider = os.getenv("EMAIL_PROVIDER", "smtp").lower()
        self.sender_email = os.getenv("SENDER_EMAIL")
        self.sender_password = os.getenv("SENDER_PASSWORD")
        self.smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", 587))
        self.sendgrid_api_key = os.getenv("SENDGRID_API_KEY")
    
    def send_email(
        self,
        to_email: str,
        subject: str,
        html_content: str,
        text_content: Optional[str] = None,
        cc: Optional[List[str]] = None,
        bcc: Optional[List[str]] = None
    ) -> bool:
        """
        Send email using configured provider
        
        Args:
            to_email: Recipient email address
            subject: Email subject
            html_content: HTML body of email
            text_content: Plain text fallback (optional)
            cc: CC recipients (optional)
            bcc: BCC recipients (optional)
            
        Returns:
            True if email sent successfully, False otherwise
        """
        try:
            if self.provider == "sendgrid":
                return self._send_via_sendgrid(to_email, subject, html_content, text_content)
            else:
                return self._send_via_smtp(to_email, subject, html_content, text_content, cc, bcc)
        except Exception as e:
            print(f"❌ Email send failed: {str(e)}")
            return False
    
    def _send_via_smtp(
        self,
        to_email: str,
        subject: str,
        html_content: str,
        text_content: Optional[str],
        cc: Optional[List[str]],
        bcc: Optional[List[str]]
    ) -> bool:
        """Send email via SMTP (Gmail, etc.)"""
        if not self.sender_email or not self.sender_password:
            print("❌ SMTP credentials not configured")
            return False
        
        try:
            # Create message
            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = self.sender_email
            msg["To"] = to_email
            
            if cc:
                msg["Cc"] = ", ".join(cc)
            
            # Add text and HTML parts
            if text_content:
                msg.attach(MIMEText(text_content, "plain"))
            msg.attach(MIMEText(html_content, "html"))
            
            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                
                recipients = [to_email]
                if cc:
                    recipients.extend(cc)
                if bcc:
                    recipients.extend(bcc)
                
                server.sendmail(self.sender_email, recipients, msg.as_string())
            
            print(f"✅ Email sent to {to_email}")
            return True
            
        except Exception as e:
            print(f"❌ SMTP error: {str(e)}")
            return False
    
    def _send_via_sendgrid(
        self,
        to_email: str,
        subject: str,
        html_content: str,
        text_content: Optional[str]
    ) -> bool:
        """Send email via SendGrid API"""
        if not self.sendgrid_api_key:
            print("❌ SendGrid API key not configured")
            return False
        
        try:
            from sendgrid import SendGridAPIClient
            from sendgrid.helpers.mail import Mail, Email, To, Content
            
            message = Mail(
                from_email=Email(self.sender_email),
                to_emails=To(to_email),
                subject=subject,
                plain_text_content=text_content,
                html_content=html_content
            )
            
            sg = SendGridAPIClient(self.sendgrid_api_key)
            response = sg.send(message)
            
            print(f"✅ Email sent to {to_email} via SendGrid")
            return response.status_code in [200, 201, 202]
            
        except ImportError:
            print("❌ SendGrid not installed. Install with: pip install sendgrid")
            return False
        except Exception as e:
            print(f"❌ SendGrid error: {str(e)}")
            return False
    
    @staticmethod
    def create_donation_email(donor_name: str, amount: float, receipt_url: str) -> tuple:
        """Create donation confirmation email"""
        subject = "Thank You for Your Donation 🙏"
        
        html_content = f"""
        <html>
            <body style="font-family: Arial, sans-serif;">
                <div style="max-width: 600px; margin: 0 auto;">
                    <h2>Thank You for Your Support!</h2>
                    <p>Dear {donor_name},</p>
                    <p>We have successfully received your generous donation of <strong>₹{amount}</strong>.</p>
                    <p>Your contribution will help us create positive change in our community.</p>
                    <p>
                        <a href="{receipt_url}" style="background-color: #007bff; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">
                            Download Receipt
                        </a>
                    </p>
                    <p style="margin-top: 30px; color: #666;">
                        Warm regards,<br>
                        <strong>Shri Krishna Udhav Memorial Trust</strong>
                    </p>
                </div>
            </body>
        </html>
        """
        
        text_content = f"""
        Thank You for Your Support!
        
        Dear {donor_name},
        
        We have successfully received your generous donation of ₹{amount}.
        
        Your contribution will help us create positive change in our community.
        
        Download Receipt: {receipt_url}
        
        Warm regards,
        Shri Krishna Udhav Memorial Trust
        """
        
        return subject, html_content, text_content
    
    @staticmethod
    def create_volunteer_email(volunteer_name: str, status: str) -> tuple:
        """Create volunteer application response email"""
        if status == "approved":
            subject = "Your Volunteer Application Has Been Approved! 🎉"
            message = "We are excited to welcome you to our volunteer team! You will hear from us soon with next steps."
            color = "#28a745"
        else:
            subject = "Update on Your Volunteer Application"
            message = "Thank you for your interest in volunteering with us. We appreciate your enthusiasm!"
            color = "#ffc107"
        
        html_content = f"""
        <html>
            <body style="font-family: Arial, sans-serif;">
                <div style="max-width: 600px; margin: 0 auto;">
                    <h2>Hello {volunteer_name},</h2>
                    <div style="background-color: {color}; padding: 20px; border-radius: 5px; margin: 20px 0;">
                        <p style="margin: 0; color: white; font-size: 18px; font-weight: bold;">
                            Application Status: {status.upper()}
                        </p>
                    </div>
                    <p>{message}</p>
                    <p style="margin-top: 30px; color: #666;">
                        Best regards,<br>
                        <strong>Shri Krishna Udhav Memorial Trust</strong>
                    </p>
                </div>
            </body>
        </html>
        """
        
        text_content = f"""
        Hello {volunteer_name},
        
        Application Status: {status.upper()}
        
        {message}
        
        Best regards,
        Shri Krishna Udhav Memorial Trust
        """
        
        return subject, html_content, text_content
    
    @staticmethod
    def create_contact_response_email(contact_name: str, message: str) -> tuple:
        """Create contact form response email"""
        subject = "We Received Your Message 📨"
        
        html_content = f"""
        <html>
            <body style="font-family: Arial, sans-serif;">
                <div style="max-width: 600px; margin: 0 auto;">
                    <h2>Thank You for Reaching Out!</h2>
                    <p>Dear {contact_name},</p>
                    <p>We have received your message and will get back to you soon.</p>
                    <div style="background-color: #f5f5f5; padding: 15px; border-radius: 5px; margin: 20px 0;">
                        <p><strong>Your Message:</strong></p>
                        <p>{message}</p>
                    </div>
                    <p style="margin-top: 30px; color: #666;">
                        Best regards,<br>
                        <strong>Shri Krishna Udhav Memorial Trust Team</strong>
                    </p>
                </div>
            </body>
        </html>
        """
        
        text_content = f"""
        Thank You for Reaching Out!
        
        Dear {contact_name},
        
        We have received your message and will get back to you soon.
        
        Your Message:
        {message}
        
        Best regards,
        Shri Krishna Udhav Memorial Trust Team
        """
        
        return subject, html_content, text_content


# Singleton instance
email_service = EmailService()
