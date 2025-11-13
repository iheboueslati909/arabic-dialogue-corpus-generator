# app.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.flow import dialogue_flow

app = FastAPI()

# Allow your Next.js frontend to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/generate-dialogues")
def generate_dialogues_api():
    # This triggers the Prefect flow
    output_path = dialogue_flow()
    with open(output_path, "r", encoding="utf-8") as f:
        data = f.read()
    return {"dialogues": data}
