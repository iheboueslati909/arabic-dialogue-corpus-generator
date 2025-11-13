import os
import time
import random
import google.generativeai as genai
import google.api_core.exceptions as gerrors

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
CALLS_PER_MINUTE = 10
PERIOD = 60

def backoff_delay(attempt, base=1, cap=30):
    """Exponential backoff with jitter."""
    return min(base * (2 ** attempt) + random.uniform(0, 1), cap)

def is_transient_error(e):
    """Check if error is transient and worth retrying."""
    return isinstance(e, (gerrors.ServiceUnavailable, gerrors.ResourceExhausted, gerrors.InternalServerError))

def call_llm(prompt: str, retries: int = 3):
    """Call Gemini LLM with retries and exponential backoff."""
    model = genai.GenerativeModel("gemini-2.5-flash-lite")

    for attempt in range(retries):
        try:
            start = time.time()
            print(f"[INFO] Attempt {attempt+1}/{retries}: calling Gemini...")
            response = model.generate_content(prompt)
            duration = time.time() - start
            text_len = len(response.text or "")
            print(f"[INFO] Success in {duration:.2f}s, len={text_len}")
            return response.text

        except gerrors.GoogleAPICallError as e:
            if is_transient_error(e):
                delay = backoff_delay(attempt)
                print(f"[WARNING] Transient error: {type(e).__name__} — retrying in {delay:.1f}s")
                time.sleep(delay)
                continue
            else:
                print(f"[ERROR] Non-retryable error: {type(e).__name__} — {getattr(e, 'message', str(e))}")
                raise

        except Exception as e:
            print(f"[ERROR] Unexpected error: {e}")
            raise

    raise RuntimeError("[ERROR] Failed after max retries")
