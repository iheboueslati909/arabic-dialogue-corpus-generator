from dotenv import load_dotenv
import os
from pathlib import Path

load_dotenv()

LOG_INFO = "[INFO]"
LOG_WARNING = "[WARNING]"
LOG_ERROR = "[ERROR]"

# INPUT EXTENSIONS
SUPPORTED_EXTENSIONS = {".pdf", ".docx", ".ppt", ".pptx"}

# PROMPT
LLM_ROLE_INSTRUCTION = (
    "You are an Arabic language tutor. Based on the following lesson content, "
    "generate {num_dialogues} short dialogues in Modern Standard Arabic."
)
LLM_NUM_DIALOGUES = 10
LLM_OUTPUT_FORMAT = """
Output as JSON:
[
  {{"topic": "Topic", "dialogue": [{{"A": "..."}}, {{"B": "..."}}]}}
]
"""
LLM_SECTION_SEPARATOR = "---"

# LLM / API
LLM_MODEL_NAME = "gemini-2.5-flash-lite"
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
# Rate limiting
CALLS_PER_MINUTE = 10
PERIOD_SECONDS = 60
# Retry / Backoff
LLM_RETRIES = 3
BACKOFF_BASE = 1
BACKOFF_CAP = 30  # max seconds for exponential backoff

# Dialogue printing / parsing settings
DIALOGUE_JSON_REGEX = r'```json\n(.*?)\n```'  # regex to extract JSON from LLM markdown
DIALOGUE_TOPIC_LINE = "=" * 70                 # line separator for topic header
DIALOGUE_TOPIC_ICON = "🎯"                     # icon for topic
SPEAKER_A_ICON = "👤"
SPEAKER_B_ICON = "👥"

# Paths
INPUT_DIR = Path("./data/sample_docs")
OUTPUT_DIR = Path("./data/outputs")

# File formatting
DOC_BREAK = "\n---DOC BREAK---\n"
TIMESTAMP_FORMAT = "%Y%m%d_%H%M%S"

# Task retry settings
EXTRACT_TEXT_RETRIES = 2
EXTRACT_TEXT_RETRY_DELAY = 10

COMBINE_TEXTS_RETRIES = 1

GENERATE_DIALOGUES_RETRIES = 2
GENERATE_DIALOGUES_RETRY_DELAY = 15

SAVE_DIALOGUES_RETRIES = 1