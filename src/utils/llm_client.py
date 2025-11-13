import os
import time
import random
import google.generativeai as genai
import google.api_core.exceptions as gerrors
from .config import (
    GEMINI_API_KEY,
    LLM_MODEL_NAME,
    LLM_RETRIES,
    BACKOFF_BASE,
    BACKOFF_CAP,
    LOG_INFO,
    LOG_WARNING,
    LOG_ERROR
)

genai.configure(api_key=GEMINI_API_KEY)

def backoff_delay(attempt, base=BACKOFF_BASE, cap=BACKOFF_CAP):
    """Exponential backoff with jitter."""
    return min(base * (2 ** attempt) + random.uniform(0, 1), cap)

def is_transient_error(e):
    """Check if error is transient and worth retrying."""
    return isinstance(e, (gerrors.ServiceUnavailable, gerrors.ResourceExhausted, gerrors.InternalServerError))

def call_llm(prompt: str, retries: int = LLM_RETRIES):
    """Call Gemini LLM with retries and exponential backoff."""
    model = genai.GenerativeModel(LLM_MODEL_NAME)

    for attempt in range(retries):
        try:
            start = time.time()
            print(f"{LOG_INFO} Attempt {attempt+1}/{retries}: calling Gemini...")
            response = model.generate_content(prompt)
            duration = time.time() - start
            text_len = len(response.text or "")
            print(f"{LOG_INFO} Success in {duration:.2f}s, len={text_len}")
            return response.text

        except gerrors.GoogleAPICallError as e:
            if is_transient_error(e):
                delay = backoff_delay(attempt)
                print(f"{LOG_WARNING} Transient error: {type(e).__name__} — retrying in {delay:.1f}s")
                time.sleep(delay)
                continue
            else:
                print(f"{LOG_ERROR} Non-retryable error: {type(e).__name__} — {getattr(e, 'message', str(e))}")
                raise

        except Exception as e:
            print(f"{LOG_ERROR} Unexpected error: {e}")
            raise

    raise RuntimeError(f"{LOG_ERROR} Failed after max retries")
