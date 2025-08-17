import os
import uuid
import logging
from werkzeug.utils import secure_filename
from typing import Optional, List

logger = logging.getLogger(__name__)

class FileUtils:
    @staticmethod
    def secure_save(file, upload_folder: str, allowed_extensions: Optional[List[str]] = None) -> str:
        """Securely save uploaded file with unique filename"""
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder, exist_ok=True)

        if allowed_extensions:
            ext = os.path.splitext(file.filename)[1].lower()
            if ext not in allowed_extensions:
                raise ValueError(f"Invalid file extension. Allowed: {allowed_extensions}")

        # Generate unique filename while preserving extension
        filename = secure_filename(file.filename)
        unique_id = uuid.uuid4().hex[:8]
        name, ext = os.path.splitext(filename)
        new_filename = f"{name}_{unique_id}{ext}"
        save_path = os.path.join(upload_folder, new_filename)

        try:
            file.save(save_path)
            logger.info(f"File saved successfully: {save_path}")
            return save_path
        except Exception as e:
            logger.error(f"Failed to save file: {e}")
            raise

    @staticmethod
    def cleanup_files(file_paths: List[str]):
        """Clean up temporary files"""
        for file_path in file_paths:
            try:
                if os.path.exists(file_path):
                    os.remove(file_path)
                    logger.info(f"Cleaned up file: {file_path}")
            except Exception as e:
                logger.error(f"Failed to cleanup file {file_path}: {e}")

    @staticmethod
    def validate_file_type(filename: str, allowed_extensions: List[str]) -> bool:
        """Check if file has allowed extension"""
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in allowed_extensions

    @staticmethod
    def get_file_extension(filename: str) -> str:
        """Get lowercase file extension without dot"""
        return os.path.splitext(filename)[1][1:].lower()