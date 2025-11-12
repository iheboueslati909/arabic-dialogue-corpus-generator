import json
import os
from datetime import datetime

def save_output(file_path: str, dialogues: str):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    
    basename = os.path.basename(file_path).split(".")[0]
    filename = f"{timestamp}_{basename}_dialogues.json"
    
    output_dir = "outputs"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, filename)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(dialogues, f, ensure_ascii=False, indent=2)

    return output_path
