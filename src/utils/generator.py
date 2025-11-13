from src.utils.llm_client import call_llm
from .config import (
    LLM_ROLE_INSTRUCTION,
    LLM_NUM_DIALOGUES,
    LLM_OUTPUT_FORMAT,
    LLM_SECTION_SEPARATOR,
    DEFAULT_LLM_MODEL
)
    
def generate_dialogues(lesson_text: str, model_key: str = DEFAULT_LLM_MODEL):

    prompt = f"""
{LLM_ROLE_INSTRUCTION.format(num_dialogues=LLM_NUM_DIALOGUES)}
{LLM_OUTPUT_FORMAT}
{LLM_SECTION_SEPARATOR}
{lesson_text}
"""
    return call_llm(prompt,model_key)
