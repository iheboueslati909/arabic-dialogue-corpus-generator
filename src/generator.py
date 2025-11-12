from src.utils.llm_client import call_llm

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
    return call_llm(prompt)
