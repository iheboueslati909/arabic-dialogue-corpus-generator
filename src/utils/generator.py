from src.utils.llm_client import call_llm
from src.utils.pretty_log_dialogues import parse_and_print_dialogues
from .config import (
    LLM_ROLE_INSTRUCTION,
    LLM_NUM_DIALOGUES,
    LLM_OUTPUT_FORMAT,
    LLM_SECTION_SEPARATOR
)

def generate_dialogues(lesson_text: str):
    prompt = f"""
{LLM_ROLE_INSTRUCTION.format(num_dialogues=LLM_NUM_DIALOGUES)}
{LLM_OUTPUT_FORMAT}
{LLM_SECTION_SEPARATOR}
{lesson_text}
"""
    result = call_llm(prompt)
    parse_and_print_dialogues(result)
    return result
