import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import logging
from typing import List

logger = logging.getLogger(__name__)

class EmailService:
    @staticmethod
    def send_email(
        recipient: str,
        subject: str,
        body: str,
        attachments: List[str],
        smtp_config: dict
    ):
        """Send email with attachments"""
        msg = MIMEMultipart()
        msg['From'] = smtp_config['sender_email']
        msg['To'] = recipient
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        
        for file_path in attachments:
            with open(file_path, 'rb') as f:
                part = MIMEApplication(f.read(), Name=file_path.split('/')[-1])
                part['Content-Disposition'] = f'attachment; filename="{file_path.split("/")[-1]}"'
                msg.attach(part)
        
        try:
            with smtplib.SMTP(smtp_config['host'], smtp_config['port']) as server:
                server.starttls()
                server.login(smtp_config['username'], smtp_config['password'])
                server.send_message(msg)
            logger.info(f"Email successfully sent to {recipient}")
        except Exception as e:
            logger.error(f"Failed to send email to {recipient}: {e}")
            raise

    @staticmethod
    def send_bulk_emails(
        recipients: List[str],
        subject: str,
        body: str,
        attachments_list: List[List[str]],
        smtp_config: dict
    ):
        """Send emails to multiple recipients with different attachments"""
        if len(recipients) != len(attachments_list):
            raise ValueError("Recipients and attachments lists must be same length")
        
        for recipient, attachments in zip(recipients, attachments_list):
            EmailService.send_email(recipient, subject, body, attachments, smtp_config)