import pytest
from unittest.mock import patch, MagicMock
from app.services.email_service import EmailService
from email.mime.multipart import MIMEMultipart

class TestEmailService:
    @patch('smtplib.SMTP')
    def test_send_email(self, mock_smtp):
        # Setup mock SMTP
        mock_server = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_server
        
        # Test data
        test_config = {
            'host': 'smtp.test.com',
            'port': 587,
            'username': 'user',
            'password': 'pass',
            'sender_email': 'from@test.com'
        }
        
        # Call method
        EmailService.send_email(
            recipient='to@test.com',
            subject='Test',
            body='Test body',
            attachments=['test.txt'],
            smtp_config=test_config
        )
        
        # Verify SMTP calls
        mock_smtp.assert_called_with('smtp.test.com', 587)
        mock_server.starttls.assert_called_once()
        mock_server.login.assert_called_with('user', 'pass')
        mock_server.send_message.assert_called_once()

    @patch('app.services.email_service.EmailService.send_email')
    def test_send_bulk_emails(self, mock_send):
        test_config = {
            'host': 'smtp.test.com',
            'port': 587,
            'username': 'user',
            'password': 'pass',
            'sender_email': 'from@test.com'
        }
        
        EmailService.send_bulk_emails(
            recipients=['a@test.com', 'b@test.com'],
            subject='Test',
            body='Test body',
            attachments_list=[['a.txt'], ['b.txt']],
            smtp_config=test_config
        )
        
        assert mock_send.call_count == 2
        assert mock_send.call_args_list[0][0][0] == 'a@test.com'
        assert mock_send.call_args_list[1][0][0] == 'b@test.com'