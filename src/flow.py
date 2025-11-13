import os
import json
from datetime import datetime
from typing import List, Dict, Any
from prefect import flow, task
from .utils.extractor import extract_text
from .utils.generator import generate_dialogues


@task(retries=2, retry_delay_seconds=10, result_serializer="json")
def extract_single_document(file_path: str) -> str:
    """Extract text from a single document."""
    text = extract_text(file_path)
    return text.strip()


@task(retries=1, result_serializer="json")
def combine_all_texts(extracted_texts: List[str]) -> str:
    """Combine all extracted texts with document breaks."""
    return "\n---DOC BREAK---\n".join(extracted_texts)


@task(retries=2, retry_delay_seconds=15, result_serializer="json")
def generate_dialogues_task(combined_text: str) -> List[Dict[str, Any]]:
    """Generate dialogues from combined text."""
    if not combined_text or not combined_text.strip():
        raise ValueError("Combined text is empty, cannot generate dialogues")
    
    dialogues = generate_dialogues(combined_text)
    
    if not dialogues:
        raise ValueError("No dialogues were generated")
    
    return dialogues


@task(retries=1)
def save_dialogues(dialogues: List[Dict[str, Any]], output_dir: str = "./data/outputs") -> str:
    """Save generated dialogues to a JSON file."""
    if not dialogues:
        raise ValueError("No dialogues to save")
    
    os.makedirs(output_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"generated_dialogues_{timestamp}.json"
    output_path = os.path.join(output_dir, filename)

    try:
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(dialogues, f, ensure_ascii=False, indent=2)
        
        print(f"Dialogues successfully saved to: {output_path}")
        return output_path
        
    except Exception as e:
        raise IOError(f"Failed to save dialogues to {output_path}: {str(e)}")


@task
def validate_input_directory(input_dir: str) -> List[str]:
    """Validate input directory and return list of file paths."""
    if not os.path.exists(input_dir):
        raise ValueError(f"Input directory {input_dir} does not exist")
    
    files = [
        os.path.join(input_dir, f) 
        for f in os.listdir(input_dir) 
        if os.path.isfile(os.path.join(input_dir, f))
    ]
    
    if not files:
        raise ValueError(f"No files found in input directory: {input_dir}")
    
    print(f"Found {len(files)} files to process")
    return files


@flow(name="Arabic Dialogue Corpus Generation")
def dialogue_flow(input_dir: str = "./data/sample_docs"):
    """
    Main flow for Arabic Dialogue Corpus Generation.
    
    Args:
        input_dir: Directory containing input documents
        
    Returns:
        Path to the generated dialogues JSON file
    """
    # Validate input and get file list
    file_paths = validate_input_directory(input_dir)
    
    # Extract text from each document individually
    extracted_texts = extract_single_document.map(file_paths)
    
    # Combine all extracted texts
    combined_text = combine_all_texts.submit(extracted_texts)
    
    # Generate dialogues from combined text
    dialogues = generate_dialogues_task.submit(combined_text)
    
    # Save dialogues to file
    result_path = save_dialogues.submit(dialogues)
    
    return result_path

if __name__ == "__main__":
    dialogue_flow()