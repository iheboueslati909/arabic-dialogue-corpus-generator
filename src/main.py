import os
from prefect import flow, task
from src.extractor import extract_text
from src.generator import generate_dialogues
from src.output_writer import save_output

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
    save_output(output_path, dialogues)
    return output_path

@flow(name="Arabic Dialogue Corpus Generation")
def dialogue_flow(input_dir: str = "sample_docs"):
    files = [os.path.join(input_dir, f) for f in os.listdir(input_dir) if os.path.isfile(os.path.join(input_dir, f))]
    all_text = extract_all_texts(files)
    result = generate_and_save_dialogues(all_text)
    return result

if __name__ == "__main__":
    dialogue_flow()
