import json
from datetime import datetime
from typing import List, Dict, Any
from prefect import flow, task
from pathlib import Path
from .utils.config import (
    INPUT_DIR,
    OUTPUT_DIR,
    DOC_BREAK,
    TIMESTAMP_FORMAT,
    EXTRACT_TEXT_RETRIES,
    EXTRACT_TEXT_RETRY_DELAY,
    COMBINE_TEXTS_RETRIES,
    GENERATE_DIALOGUES_RETRIES,
    GENERATE_DIALOGUES_RETRY_DELAY,
    SAVE_DIALOGUES_RETRIES
)
from .utils.extractor import extract_text
from .utils.generator import generate_dialogues


# -------------------- TASKS --------------------

@task(retries=EXTRACT_TEXT_RETRIES, retry_delay_seconds=EXTRACT_TEXT_RETRY_DELAY, result_serializer="json")
def extract_single_document(file_path: Path) -> str:
    """Extract text from a single document."""
    text = extract_text(file_path)
    return text.strip()


@task(retries=COMBINE_TEXTS_RETRIES, result_serializer="json")
def combine_all_texts(extracted_texts: List[str]) -> str:
    """Combine all extracted texts with document breaks."""
    return DOC_BREAK.join(extracted_texts)


@task(retries=GENERATE_DIALOGUES_RETRIES, retry_delay_seconds=GENERATE_DIALOGUES_RETRY_DELAY, result_serializer="json")
def generate_dialogues_task(combined_text: str) -> List[Dict[str, Any]]:
    """Generate dialogues from combined text."""
    if not combined_text.strip():
        raise ValueError("Combined text is empty, cannot generate dialogues")
    
    dialogues = generate_dialogues(combined_text)
    
    if not dialogues:
        raise ValueError("No dialogues were generated")
    
    return dialogues


@task(retries=SAVE_DIALOGUES_RETRIES)
def save_dialogues(dialogues: List[Dict[str, Any]], output_dir: Path = OUTPUT_DIR) -> Path:
    """Save generated dialogues to a JSON file."""
    if not dialogues:
        raise ValueError("No dialogues to save")
    
    output_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime(TIMESTAMP_FORMAT)
    filename = f"generated_dialogues_{timestamp}.json"
    output_path = output_dir / filename

    try:
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(dialogues, f, ensure_ascii=False, indent=2)
        
        print(f"[INFO] Dialogues successfully saved to: {output_path}")
        return output_path
        
    except Exception as e:
        raise IOError(f"Failed to save dialogues to {output_path}: {str(e)}")


@task
def validate_input_directory(input_dir: Path = INPUT_DIR) -> List[Path]:
    """Validate input directory and return list of file paths."""
    if not input_dir.exists():
        raise ValueError(f"Input directory {input_dir} does not exist")
    
    files = [f for f in input_dir.iterdir() if f.is_file()]
    
    if not files:
        raise ValueError(f"No files found in input directory: {input_dir}")
    
    print(f"[INFO] Found {len(files)} files to process")
    return files


# -------------------- FLOW --------------------

@flow(name="Arabic Dialogue Corpus Generation")
def dialogue_flow(input_dir: Path = INPUT_DIR):
    """
    Main flow for Arabic Dialogue Corpus Generation.
    
    Args:
        input_dir: Directory containing input documents
        
    Returns:
        Path to the generated dialogues JSON file
    """
    # Validate input and get file list
    file_paths = validate_input_directory(input_dir)
    print(file_paths)
    # Extract text from each document individually (parallel)
    extracted_texts = extract_single_document.map([str(p) for p in file_paths])
    
    # Combine all extracted texts
    combined_text = combine_all_texts.submit(extracted_texts)
    
    # Generate dialogues from combined text
    dialogues = generate_dialogues_task.submit(combined_text)
    
    # Save dialogues to file
    result_path = save_dialogues.submit(dialogues)
    
    return result_path


if __name__ == "__main__":
    dialogue_flow()
