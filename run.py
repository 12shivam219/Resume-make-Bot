#!/usr/bin/env python
"""
Resume Injector App - Main Entry Point
"""

from app import create_app
from app.utils.logging_utils import configure_logging
import os
import logging
from werkzeug.middleware.proxy_fix import ProxyFix

def configure_application():
    """Configure and return the Flask application"""
    
    # Create application instance
    app = create_app(os.getenv('FLASK_CONFIG', 'config.DevelopmentConfig'))
    
    # Configure logging
    log_dir = os.path.join(app.instance_path, 'logs')
    configure_logging(log_dir=log_dir)
    
    # Apply proxy fix if behind reverse proxy
    if os.getenv('BEHIND_PROXY', 'false').lower() == 'true':
        app.wsgi_app = ProxyFix(
            app.wsgi_app,
            x_for=1,
            x_proto=1,
            x_host=1,
            x_prefix=1
        )
    
    # Ensure upload folder exists
    upload_folder = app.config['UPLOAD_FOLDER']
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)
        logging.info(f"Created upload directory: {upload_folder}")
    
    return app

if __name__ == '__main__':
    # Configure and run application
    app = configure_application()
    
    # Run in development mode
    host = os.getenv('FLASK_HOST', '0.0.0.0')
    port = int(os.getenv('FLASK_PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'true').lower() == 'true'
    
    logging.info(f"Starting Resume Injector App on {host}:{port}")
    app.run(host=host, port=port, debug=debug)
else:
    # For WSGI/Gunicorn
    app = configure_application()