import os
from prefect import flow, task
from src.extractor import extract_text
from src.generator import generate_dialogues
from src.output_writer import save_output
import json
import os
from datetime import datetime

@task(retries=1, result_serializer="json")
def extract_all_texts(file_paths):
    texts = []
    for file_path in file_paths:
        text = extract_text(file_path)
        texts.append(text)
    return "\n---DOC BREAK---\n".join(texts)

@task(result_serializer="json")
def generate_and_save_dialogues(all_text, output_path="outputs/generated_dialogues.json"):
    dialogues = generate_dialogues(all_text)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    
    basename = os.path.basename("outputs/generated_dialogues.json").split(".")[0]
    filename = f"{timestamp}_{basename}.json"
    
    output_dir = "outputs"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, filename)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(dialogues, f, ensure_ascii=False, indent=2)

    return output_path

@flow(name="Arabic Dialogue Corpus Generation")
def dialogue_flow(input_dir: str = "sample_docs"):
    files = [os.path.join(input_dir, f) for f in os.listdir(input_dir) if os.path.isfile(os.path.join(input_dir, f))]
    all_text = extract_all_texts(files)
    result = generate_and_save_dialogues(all_text)
    return result

if __name__ == "__main__":
    dialogue_flow()
