import pytest
from unittest.mock import patch, MagicMock
from app.routes.views import main_bp
from app.routes.api import api_bp
from app import create_app
import os
import tempfile

class TestWorkflowIntegration:
    @pytest.fixture
    def client(self):
        app = create_app(config_class='config.TestConfig')
        app.config['TESTING'] = True
        app.config['UPLOAD_FOLDER'] = tempfile.mkdtemp()
        app.config['WTF_CSRF_ENABLED'] = False
        
        with app.test_client() as client:
            yield client

    @patch('app.services.document_service.DocumentService.inject_bullet_points')
    @patch('app.services.email_service.EmailService.send_email')
    def test_full_workflow(self, mock_send, mock_process, client):
        # Setup mocks
        mock_process.return_value = "processed.docx"
        mock_send.return_value = None
        
        # Create test files
        test_files = []
        for i in range(1, 4):
            path = os.path.join(client.application.config['UPLOAD_FOLDER'], f"test{i}.docx")
            with open(path, 'w') as f:
                f.write("test content")
            test_files.append(('resume'+str(i), (path, 'test'+str(i)+'.docx')))
        
        # Test form submission
        data = {
            'jd1': 'Test JD 1',
            'jd1_stack1': 'Python',
            'jd1_stack1_bullets': '\n'.join([f"py-bullet{i}" for i in range(1,7)]),
            'jd1_stack2': 'Flask',
            'jd1_stack2_bullets': '\n'.join([f"flask-bullet{i}" for i in range(1,7)]),
            'jd1_stack3': 'AWS',
            'jd1_stack3_bullets': '\n'.join([f"aws-bullet{i}" for i in range(1,7)]),
            # Similar for JD2 and JD3...
            'anchor_method': 'placeholders',
            'email1': 'test1@example.com',
            'email2': 'test2@example.com',
            'email3': 'test3@example.com',
            'email_subject': 'Test Subject',
            'email_body': 'Test Body',
            'smtp_host': 'smtp.test.com',
            'smtp_port': '587',
            'smtp_username': 'user',
            'smtp_password': 'pass',
            'sender_email': 'from@test.com'
        }
        
        # Add files to form data
        data.update(test_files)
        
        response = client.post('/', data=data, follow_redirects=True)
        
        assert response.status_code == 200
        assert b"Processing Complete" in response.data
        assert mock_process.call_count == 3
        assert mock_send.call_count == 3