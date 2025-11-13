# 🗣️ Dialogue Generator

A lightweight workflow that extracts text from documents and generates structured dialogues using **Gemini 2.5 Flash**, orchestrated with **Prefect**, and optionally integrated with **FastAPI + Next.js** for a complete full-stack experience.

---

## 🚀 Overview

The **Dialogue Generator** automates:

1. **Extracting content** from uploaded documents (`.docx`, `.pdf`, `.pptx`)
2. **Generating dialogues** using `gemini-2.5-flash`
3. **Enforcing rate limits** (Gemini Free Tier)
4. **Orchestrating tasks** via **Prefect**
5. *(Optional)* Serving results via a FastAPI backend and Next.js frontend
NEXT.js: https://github.com/iheboueslati909/aralects-assessment-next-js
---

## ⚙️ Features

- ✅ Supports **DOCX**, **PDF**, and **PPTX** files  
- ⚡ Uses **Gemini 2.5 Flash** for dialogue generation  
- 🔒 Built-in rate limiter for gemini-2.5-flash Free Tier
- ☁️ Integrated with **Prefect 3** for local orchestration and UI dashboard  
- 🌐 Optional **FastAPI + Next.js** integration for full-stack use  

---
![ezcv logo](https://raw.githubusercontent.com/iheboueslati909/arabic-dialogue-corpus-generator/refs/heads/main/ss1.png)
![ezcv logo](https://raw.githubusercontent.com/iheboueslati909/arabic-dialogue-corpus-generator/refs/heads/main/ss2.png)

---

## 🧰 Dependencies

Install required dependencies:

```bash
pip install markitdown[PPT,DOCX,PDF]
pip install ratelimit
pip install google-generativeai
pip install -U prefect prefect-cloud
pip install python-dotenv
pip install fastAPI
```
---

## 🔑 Environment Configuration

GEMINI_API_KEY=your_api_key_here
---

## ⚡ Prefect Setup

To run Prefect locally:

1. Start the local Prefect server
prefect server start

2. Create a local profile
prefect profile create local

3. Configure the Prefect API URL
prefect config set PREFECT_API_URL=http://127.0.0.1:4200/api

4. Verify your configuration
prefect config view


Once running, open the Prefect dashboard in your browser:
👉 http://127.0.0.1:4200/dashboard
---

## 🧪 Running the Script

Activate your virtual environment:

.venv\Scripts\activate


Then execute the main Prefect flow:

python -m src.flow


This process will:

Extract text from all supported documents in your input directory.

Use Gemini to generate dialogues.

Save structured output locally /outputs.
---

## 🌍 Full-Stack Integration (Optional)

For an end-to-end setup, you can connect your Prefect flow with the backend and frontend layers.

🖥️ Run the FastAPI Backend
uvicorn app:app --reload --port 8000

💻 Run the Next.js Frontend
pnpm run dev

