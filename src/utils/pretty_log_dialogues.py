import json
import re
import sys
import io

# UTF-8 FIX - Add this at the top
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def parse_and_print_dialogues(llm_response):
    """
    Parse LLM response and beautifully print dialogues
    Handles the markdown code block format
    """
    try:
        # Extract JSON from the markdown code block
        json_match = re.search(r'```json\n(.*?)\n```', llm_response, re.DOTALL)
        if json_match:
            json_str = json_match.group(1)
        else:
            # If no code block found, try to parse the whole response as JSON
            json_str = llm_response
        
        # Parse the JSON data
        data = json.loads(json_str)
        
        # Print the dialogues
        print_dialogues(data)
        
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        print("Raw response:")
        print(llm_response)
    except Exception as e:
        print(f"Error: {e}")

def print_dialogues(data):
    """
    Beautifully formats and prints dialogues from the parsed data
    """
    for i, conversation in enumerate(data, 1):
        topic = conversation["topic"]
        dialogue = conversation["dialogue"]
        
        # Print topic header
        print(f"\n{'='*70}")
        print(f"🎯 Conversation {i}: {topic}")
        print(f"{'='*70}")
        
        # Print each dialogue exchange
        for exchange in dialogue:
            for speaker, text in exchange.items():
                # Add visual styling based on speaker
                if speaker == "A":
                    print(f"👤 {speaker}: {text}")
                else:
                    print(f"👥 {speaker}: {text}")
        
        print()  # Add space between conversations