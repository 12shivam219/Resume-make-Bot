import logging
import os
from logging.handlers import RotatingFileHandler
from datetime import datetime
from typing import Optional

def configure_logging(log_dir: Optional[str] = None, log_level: int = logging.INFO):
    """Configure structured logging for the application"""
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir, exist_ok=True)

    # Main logger configuration
    logger = logging.getLogger()
    logger.setLevel(log_level)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    # File handler (if log directory specified)
    if log_dir:
        log_file = os.path.join(log_dir, f"resume_injector_{datetime.now():%Y-%m-%d}.log")
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=1024 * 1024 * 5,  # 5MB
            backupCount=5
        )
        file_handler.setLevel(log_level)
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(module)s:%(lineno)d - %(message)s')
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

    # Special logger for email events
    email_logger = logging.getLogger('email')
    email_logger.setLevel(logging.INFO)

    # Disable overly verbose logs from libraries
    logging.getLogger('werkzeug').setLevel(logging.WARNING)
    logging.getLogger('PIL').setLevel(logging.WARNING)
    logging.getLogger('docx').setLevel(logging.WARNING)