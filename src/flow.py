import os
import json
from datetime import datetime
from prefect import flow, task
from .utils.extractor import extract_text
from .utils.generator import generate_dialogues
from .utils.pretty_log_dialogues import parse_and_print_dialogues

@task(retries=1, result_serializer="json")
def extract_all_texts(file_paths):
    texts = []
    for file_path in file_paths:
        text = extract_text(file_path)
        texts.append(text)
    return "\n---DOC BREAK---\n".join(texts)


@task(result_serializer="json")
def generate_and_save_dialogues(all_text, output_dir="./data/outputs"):
    dialogues = generate_dialogues(all_text)
    
    parse_and_print_dialogues(dialogues)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"generated_dialogues_{timestamp}.json"
    
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, filename)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(dialogues, f, ensure_ascii=False, indent=2)

    return output_path


@flow(name="Arabic Dialogue Corpus Generation")
def dialogue_flow(input_dir: str = "./data/sample_docs"):
    if not os.path.exists(input_dir):
        raise ValueError(f"Input directory {input_dir} does not exist")
    
    files = [
        os.path.join(input_dir, f) 
        for f in os.listdir(input_dir) 
        if os.path.isfile(os.path.join(input_dir, f))
    ]
    
    all_text = extract_all_texts(files)
    result = generate_and_save_dialogues(all_text)

    return result

if __name__ == "__main__":
    dialogue_flow()