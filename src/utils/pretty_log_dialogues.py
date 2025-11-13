import json
import re
import sys
import io
from .config import (
    DIALOGUE_JSON_REGEX,
    DIALOGUE_TOPIC_LINE,
    DIALOGUE_TOPIC_ICON,
    SPEAKER_A_ICON,
    SPEAKER_B_ICON
)

# UTF-8 fix
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', line_buffering=True)

def parse_and_print_dialogues(llm_response):
    try:
        json_match = re.search(DIALOGUE_JSON_REGEX, llm_response, re.DOTALL)
        json_str = json_match.group(1) if json_match else llm_response
        data = json.loads(json_str)
        print_dialogues(data)
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}\nRaw response:\n{llm_response}")
    except Exception as e:
        print(f"Error: {e}")

def print_dialogues(data):
    for i, conversation in enumerate(data, 1):
        topic = conversation["topic"]
        dialogue = conversation["dialogue"]

        print(f"\n{DIALOGUE_TOPIC_LINE}")
        print(f"{DIALOGUE_TOPIC_ICON} Conversation {i}: {topic}")
        print(f"{DIALOGUE_TOPIC_LINE}")

        for exchange in dialogue:
            for speaker, text in exchange.items():
                icon = SPEAKER_A_ICON if speaker == "A" else SPEAKER_B_ICON
                print(f"{icon} {speaker}: {text}")

        print()
