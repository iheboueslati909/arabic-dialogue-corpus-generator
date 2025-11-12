from markitdown import MarkItDown

def extract_text(file_path: str) -> str:
    md = MarkItDown()
    result = md.convert(file_path)
    return result.text_content
