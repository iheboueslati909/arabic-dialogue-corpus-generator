from markitdown import MarkItDown
import os
import logging

# Set up logger for this module
logger = logging.getLogger(__name__)

SUPPORTED_EXTENSIONS = {'.pdf', '.docx', '.ppt', '.pptx'}

def extract_text(file_path: str) -> str:
    # Get file extension (lowercase for case-insensitive comparison)
    _, ext = os.path.splitext(file_path)
    ext = ext.lower()
    
    # Skip unsupported files
    if ext not in SUPPORTED_EXTENSIONS:
        logger.warning(
            f"Skipping unsupported file type: {file_path} (extension: {ext})"
        )
        return ""  # Return empty string instead of raising
    
    # Proceed with extraction
    md = MarkItDown()
    result = md.convert(file_path)
    return result.text_content