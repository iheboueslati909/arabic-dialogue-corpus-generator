import json
import typer
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
    SAVE_DIALOGUES_RETRIES,
    DEFAULT_LLM_MODEL
)
from .utils.extractor import extract_text
from .utils.generator import generate_dialogues
from .utils.pretty_log_dialogues import parse_and_print_dialogues


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
def generate_dialogues_task(combined_text: str, model_key: str = DEFAULT_LLM_MODEL) -> List[Dict[str, Any]]:
    """Generate dialogues from combined text."""
    if not combined_text.strip():
        raise ValueError("Combined text is empty, cannot generate dialogues")
    
    dialogues = generate_dialogues(combined_text, model_key=model_key)
    
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

app = typer.Typer()

@app.command()
def run(
    model: str = typer.Option(DEFAULT_LLM_MODEL, "--model", "-m")
):
    """
    Run the Prefect flow from the CLI using Typer.
    """
    model = model.strip()
    result = dialogue_flow(model_key=model)
    typer.echo(f"[DONE] Output saved at: {result}")
    
    
@flow(name="Arabic Dialogue Corpus Generation")
def dialogue_flow(model_key: str = DEFAULT_LLM_MODEL, input_dir: Path = INPUT_DIR):
    # Validate input
    file_paths = validate_input_directory(input_dir)
    
    # Extract text (parallel)
    extracted_texts = extract_single_document.map([str(p) for p in file_paths])
    
    # Combine texts
    combined_text = combine_all_texts.submit(extracted_texts)
    
    # Generate dialogues
    dialogues_future = generate_dialogues_task.submit(combined_text, model_key=model_key)
    
    # Save dialogues
    save_future = save_dialogues.submit(dialogues_future)
    
    # ✅ Wait for all tasks to finish before printing
    dialogues = dialogues_future.result()
    save_path = save_future.result()
    
    # Print dialogues in one go
    parse_and_print_dialogues(dialogues)
    
    return save_path


if __name__ == "__main__":
    app()