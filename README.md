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

![image.png](https://ibb.co/yB0Ppbn5)
![image2.png](https://ibb.co/hRdMYSZ5)

## 🧰 Dependencies

Install required dependencies:

```bash
pip install markitdown[PPT,DOCX,PDF]
pip install ratelimit
pip install google-generativeai
pip install -U prefect prefect-cloud
pip install python-dotenv

