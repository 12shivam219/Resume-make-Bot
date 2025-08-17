from flask import Blueprint, request, jsonify, current_app
from app.services.document_service import DocumentService
from app.services.email_service import EmailService
from app.utils.file_utils import FileUtils
from app.models import JobDescription, Resume, EmailConfig
import concurrent.futures
import os

api_bp = Blueprint('api', __name__)

@api_bp.route('/process', methods=['POST'])
def process_resumes():
    """API endpoint for resume processing"""
    try:
        # Validate input
        if 'resumes[]' not in request.files:
            return jsonify({'error': 'No resume files uploaded'}), 400
        
        resumes = request.files.getlist('resumes[]')
        if len(resumes) != 3:
            return jsonify({'error': 'Exactly 3 resumes required'}), 400

        # Save uploaded files
        saved_files = []
        for resume in resumes:
            if not FileUtils.validate_file_type(resume.filename, ['doc', 'docx']):
                return jsonify({'error': 'Invalid file type. Only .doc/.docx allowed'}), 400
            file_path = FileUtils.secure_save(
                resume,
                current_app.config['UPLOAD_FOLDER'],
                ['doc', 'docx']
            )
            saved_files.append(file_path)

        # Process JDs (example - would come from request in real implementation)
        jds = [
            JobDescription(
                raw_text="JD 1 content",
                tech_stacks={
                    "Python": ["bullet1", "bullet2", "bullet3", "bullet4", "bullet5", "bullet6"],
                    "Flask": ["bullet1", "bullet2", "bullet3", "bullet4", "bullet5", "bullet6"],
                    "AWS": ["bullet1", "bullet2", "bullet3", "bullet4", "bullet5", "bullet6"]
                }
            ),
            # JD 2 and 3 would be similar
        ]

        # Process resumes in parallel
        processed_files = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            futures = []
            for i in range(3):
                futures.append(executor.submit(
                    DocumentService.inject_bullet_points,
                    saved_files[i],
                    os.path.join(current_app.config['UPLOAD_FOLDER'], f"processed_{i}.docx"),
                    jds[i].tech_stacks,
                    request.form.get('anchor_method', 'placeholders')
                ))
            
            for future in concurrent.futures.as_completed(futures):
                processed_files.append(future.result())

        return jsonify({
            'message': 'Processing complete',
            'files': processed_files
        }), 200

    except Exception as e:
        FileUtils.cleanup_files(saved_files + processed_files)
        return jsonify({'error': str(e)}), 500

@api_bp.route('/send-emails', methods=['POST'])
def send_emails():
    """API endpoint for sending processed resumes"""
    try:
        data = request.get_json()
        email_config = EmailConfig(
            recipients=data['recipients'],
            subject=data.get('subject', 'Your Tailored Resume'),
            body=data.get('body', 'Please find attached your tailored resume.')
        )

        # Validate we have 3 recipients and 3 files
        if len(email_config.recipients) != 3:
            return jsonify({'error': 'Exactly 3 recipients required'}), 400

        if 'files[]' not in data or len(data['files[]']) != 3:
            return jsonify({'error': 'Exactly 3 files required'}), 400

        # Send emails in parallel
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            futures = []
            for i in range(3):
                futures.append(executor.submit(
                    EmailService.send_email,
                    email_config.recipients[i],
                    email_config.subject,
                    email_config.body,
                    [data['files[]'][i]],
                    {
                        'host': current_app.config['SMTP_HOST'],
                        'port': current_app.config['SMTP_PORT'],
                        'username': current_app.config['SMTP_USERNAME'],
                        'password': current_app.config['SMTP_PASSWORD'],
                        'sender_email': current_app.config['SENDER_EMAIL']
                    }
                ))
            
            # Wait for all emails to complete
            concurrent.futures.wait(futures)

        return jsonify({'message': 'Emails sent successfully'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500