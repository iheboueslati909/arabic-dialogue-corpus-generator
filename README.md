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

## 🧰 Dependencies

Install required dependencies:

```bash
pip install markitdown[PPT,DOCX,PDF]
pip install ratelimit
pip install google-generativeai
pip install -U prefect prefect-cloud
pip install python-dotenv

![image.png](https://img.notionusercontent.com/s3/prod-files-secure%2F3e4b640f-2995-4b04-b406-2a714cac3861%2Fbf967a94-5632-4da6-bf68-9e5be29c8434%2Fimage.png/size/w=2000?exp=1762989345&sig=5P4C3RvirXCTHxBaZq9Mb4Q3yuEMy0q-aLyx_HmASIQ&id=2a94de3b-4d14-8059-acfb-c736ad14bd98&table=block&userId=d5f814cb-539c-418a-822c-ca3f3f304fa2)
![image.png](https://img.notionusercontent.com/s3/prod-files-secure%2F3e4b640f-2995-4b04-b406-2a714cac3861%2Fd9d68a9c-29ac-4b5a-80b7-1e3dcb3aae0c%2Fimage.png/size/w=2000?exp=1762989399&sig=XSOa19Hzvs-D296U9y3PCGLwWQ8TzmhvaBPb0zFokRQ&id=2a94de3b-4d14-80e1-9ced-cc660c1f690e&table=block&userId=d5f814cb-539c-418a-822c-ca3f3f304fa2)