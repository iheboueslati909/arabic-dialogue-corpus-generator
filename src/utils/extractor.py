import os
from markitdown import MarkItDown
from .config import SUPPORTED_EXTENSIONS, LOG_INFO, LOG_WARNING, LOG_ERROR

def extract_text(file_path: str) -> str:
    if not file_path or not isinstance(file_path, str):
        raise ValueError("File path must be a non-empty string")

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    if not os.path.isfile(file_path):
        raise ValueError(f"Path is not a file: {file_path}")

    _, ext = os.path.splitext(file_path)
    ext = ext.lower()

    if ext not in SUPPORTED_EXTENSIONS:
        print(f"{LOG_WARNING} Skipping unsupported file type: {file_path} (ext={ext})")
        return ""

    print(f"{LOG_INFO} Extracting text from: {file_path}")

    try:
        md = MarkItDown()
        result = md.convert(file_path)

        if not result.text_content:
            print(f"{LOG_WARNING} No text content extracted from: {file_path}")
            return ""

        print(f"{LOG_INFO} Extraction successful — {len(result.text_content)} characters from {file_path}")
        return result.text_content

    except Exception as e:
        print(f"{LOG_ERROR} Failed to extract text from {file_path}: {e}")
        raise RuntimeError(f"Text extraction failed for {file_path}") from e
