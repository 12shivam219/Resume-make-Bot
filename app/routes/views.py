from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from werkzeug.utils import secure_filename
from app.services.document_service import DocumentService
from app.services.email_service import EmailService
from app.utils.file_utils import FileUtils
import os
import concurrent.futures

main_bp = Blueprint('main', __name__)

@main_bp.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            # Step 1: Save uploaded resumes
            resume_files = []
            for i in range(1, 4):
                file = request.files.get(f'resume{i}')
                if not file:
                    flash(f'Resume {i} is required', 'error')
                    return redirect(request.url)
                
                if not FileUtils.validate_file_type(file.filename, ['doc', 'docx']):
                    flash('Only .doc or .docx files are allowed', 'error')
                    return redirect(request.url)
                
                file_path = FileUtils.secure_save(
                    file,
                    current_app.config['UPLOAD_FOLDER'],
                    ['doc', 'docx']
                )
                resume_files.append(file_path)

            # Step 2: Process JDs (simplified example)
            jd_data = {}
            for i in range(1, 4):
                jd_data[f'jd{i}'] = {
                    'tech_stacks': {
                        request.form.get(f'jd{i}_stack1'): {
                            'bullets': request.form.get(f'jd{i}_stack1_bullets').split('\n')[:6]
                        },
                        # Similar for stack2 and stack3
                    }
                }

            # Step 3: Process resumes
            anchor_method = request.form.get('anchor_method', 'placeholders')
            processed_files = []
            
            with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
                futures = []
                for i in range(3):
                    futures.append(executor.submit(
                        DocumentService.inject_bullet_points,
                        resume_files[i],
                        os.path.join(current_app.config['UPLOAD_FOLDER'], f"processed_{i}.docx"),
                        jd_data[f'jd{i+1}']['tech_stacks'],
                        anchor_method
                    ))
                
                for future in concurrent.futures.as_completed(futures):
                    processed_files.append(future.result())

            # Step 4: Send emails
            email_config = {
                'subject': request.form.get('email_subject', 'Your Tailored Resume'),
                'body': request.form.get('email_body', 'Please find attached your tailored resume.'),
                'recipients': [
                    request.form.get('email1'),
                    request.form.get('email2'),
                    request.form.get('email3')
                ],
                'smtp_config': {
                    'host': current_app.config['SMTP_HOST'],
                    'port': current_app.config['SMTP_PORT'],
                    'username': current_app.config['SMTP_USERNAME'],
                    'password': current_app.config['SMTP_PASSWORD'],
                    'sender_email': current_app.config['SENDER_EMAIL']
                }
            }

            with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
                futures = []
                for i in range(3):
                    if email_config['recipients'][i]:
                        futures.append(executor.submit(
                            EmailService.send_email,
                            email_config['recipients'][i],
                            email_config['subject'],
                            email_config['body'],
                            [processed_files[i]],
                            email_config['smtp_config']
                        ))
                
                concurrent.futures.wait(futures)

            return render_template('results.html', files=processed_files)

        except Exception as e:
            flash(f'An error occurred: {str(e)}', 'error')
            return redirect(request.url)
    
    return render_template('index.html')

@main_bp.route('/download/<filename>')
def download_file(filename):
    return FileUtils.send_download(
        os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    )