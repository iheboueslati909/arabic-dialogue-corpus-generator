from src.utils.llm_client import call_llm
from src.utils.pretty_log_dialogues import parse_and_print_dialogues
 
def generate_dialogues(lesson_text: str):
    prompt = f"""
    You are an Arabic language tutor. Based on the following lesson content,
    generate 10 short dialogues in Modern Standard Arabic.
    Output as JSON:
    [
      {{"topic": "Topic", "dialogue": [{{"A": "..."}}, {{"B": "..."}}]}}
    ]
    ---
    {lesson_text}
    """
    
    result = call_llm(prompt)
    parse_and_print_dialogues(result)
    return result
