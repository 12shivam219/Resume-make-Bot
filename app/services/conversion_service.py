import pythoncom
import subprocess
import os
import logging
from typing import Optional

logger = logging.getLogger(__name__)

class ConversionService:
    @staticmethod
    def convert_to_docx(input_path: str, output_dir: Optional[str] = None) -> str:
        """Convert .doc to .docx using LibreOffice"""
        if not input_path.lower().endswith('.doc'):
            raise ValueError("Input file must be a .doc file")
        
        output_dir = output_dir or os.path.dirname(input_path)
        output_path = os.path.join(
            output_dir,
            f"{os.path.splitext(os.path.basename(input_path))[0]}.docx"
        )
        
        try:
            pythoncom.CoInitialize()
            subprocess.run([
                'soffice',
                '--headless',
                '--convert-to',
                'docx',
                '--outdir',
                output_dir,
                input_path
            ], check=True)
            return output_path
        except subprocess.CalledProcessError as e:
            logger.error(f"LibreOffice conversion failed: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected conversion error: {e}")
            raise

    @staticmethod
    def convert_to_pdf(input_path: str, output_dir: Optional[str] = None) -> str:
        """Convert .docx to .pdf using LibreOffice"""
        if not input_path.lower().endswith('.docx'):
            raise ValueError("Input file must be a .docx file")
        
        output_dir = output_dir or os.path.dirname(input_path)
        output_path = os.path.join(
            output_dir,
            f"{os.path.splitext(os.path.basename(input_path))[0]}.pdf"
        )
        
        try:
            pythoncom.CoInitialize()
            subprocess.run([
                'soffice',
                '--headless',
                '--convert-to',
                'pdf',
                '--outdir',
                output_dir,
                input_path
            ], check=True)
            return output_path
        except subprocess.CalledProcessError as e:
            logger.error(f"LibreOffice PDF conversion failed: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected PDF conversion error: {e}")
            raise