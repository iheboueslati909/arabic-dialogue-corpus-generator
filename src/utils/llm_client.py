import os
import time
import requests
import google.generativeai as genai
from ratelimit import limits, sleep_and_retry

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Gemini 2.5 Flash free tier: 10 requests per minute
CALLS_PER_MINUTE = 10
PERIOD = 60  # seconds

@sleep_and_retry
@limits(calls=CALLS_PER_MINUTE, period=PERIOD)
def call_llm(prompt: str, retries: int = 3, backoff: float = 2.0):
    """
    Calls Gemini LLM with rate limiting (10 RPM) and retry on 429 errors.
    """
    print(f"Starting LLM call - Attempt 1/{retries}")
    print(f"Prompt length: {len(prompt)} characters")
    
    for attempt in range(retries):
        try:
            print(f"Calling Gemini API...")
            model = genai.GenerativeModel("gemini-2.5-flash")
            response = model.generate_content(prompt)
            print(f"API call successful - Response received")
            return response.text
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 429:
                wait_time = backoff ** attempt
                print(f"Rate limit hit. Retrying in {wait_time:.1f}s... (Attempt {attempt + 1}/{retries})")
                time.sleep(wait_time)
            else:
                print(f"HTTP Error {e.response.status_code}: {e}")
                raise
        except Exception as e:
            print(f"Unexpected error: {e}")
            if attempt == retries - 1:
                raise
            wait_time = backoff ** attempt
            print(f"Retrying in {wait_time:.1f}s... (Attempt {attempt + 1}/{retries})")
            time.sleep(wait_time)
    
    print("Failed to call LLM after all retries")
    raise Exception("Failed to call LLM after retries.")