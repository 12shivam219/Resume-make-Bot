from flask import Flask
from flask_wtf.csrf import CSRFProtect
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

csrf = CSRFProtect()

def create_app(config_class='config.Config'):
    """Application factory pattern for Flask"""
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions
    csrf.init_app(app)
    
    # Register blueprints
    from app.routes.views import main_bp
    from app.routes.api import api_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp, url_prefix='/api')
    
    # Ensure upload folder exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    return app