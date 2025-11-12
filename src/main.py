from prefect import flow, task
from src.extractor import extract_text
from src.generator import generate_dialogues
from src.output_writer import save_output
import os

@task(retries=1,result_serializer="json")
def process_document(file_path: str):
    text = extract_text(file_path)
    dialogues = generate_dialogues(text)
    output_path = save_output(file_path, dialogues)
    return output_path

@flow(name="Arabic Dialogue Corpus Generation")
def dialogue_flow(input_dir: str = "sample_docs"):
    files = [os.path.join(input_dir, f) for f in os.listdir(input_dir)]
    results = []
    for f in files:
        results.append(process_document.submit(f))
    return results

if __name__ == "__main__":
    dialogue_flow()
