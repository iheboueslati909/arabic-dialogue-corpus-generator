# 🗣️ Dialogue Generator

A lightweight workflow that extracts text from documents and generates structured dialogues using **Gemini 2.5 Flash**, orchestrated with **Prefect**, and optionally integrated with **FastAPI + Next.js** for a complete full-stack experience.

---

## 🚀 Overview

The **Dialogue Generator** automates:

1. **Extracting content** from uploaded documents (`.docx`, `.pdf`, `.pptx`)
2. **Generating dialogues** using `gemini-2.5-flash-lite`
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
pip install markitdown[PPT,DOCX,PDF,PPTX]
pip install ratelimit
pip install google-generativeai
pip install -U prefect prefect-cloud
pip install python-dotenv
pip install fastAPI
```
---

## 🔑 Environment Configuration
- create a .env file the put the following:
     
     GEMINI_API_KEY=you_api_key_here

 - `config.py` centralizes all hardcoded values and constants

---

## ⚡ Prefect Setup

To setup Prefect locally ( assuming you installed the dependencies above ), run the following commands:


1. Create a local profile:
`prefect profile create local`
2. Configure the Prefect API URL:
`prefect config set PREFECT_API_URL=http://127.0.0.1:4200/api`
3. Verify your configuration:
`prefect config view`
4.  Start the local Prefect server:
`prefect server start`

Once running, open the Prefect dashboard in the browser:
http://127.0.0.1:4200/dashboard

---

## 🧪 Running the project

1. Activate your virtual environment:
`.venv\Scripts\activate`
2. Execute the main Prefect flow:
`python -m src.flow`

This process will:
1. Extract text from all supported documents in the input directory.
2. Use Gemini to generate dialogues.
3. Log & save structured output locally in `data/outputs` .

---

## 🌍 Full-Stack Integration (Optional)

For an end-to-end setup, you can connect your Prefect flow with the backend and frontend layers. This project comes with FastAPI integration too ( app.py located at the root ).

🖥️ Run the FastAPI Backend:
`uvicorn app:app --reload --port 8000`

💻 Run the Next.js Frontend:
`pnpm run dev`

---

## ★ Workflow Orchestration: Evaluation & Recommendation
When evaluating orchestration tools, I start by understanding the problem each tool was designed to solve:
- Airflow: Built for scheduled batch ETL jobs running on external systems (Hadoop/Spark era)
- Prefect: Designed for flexible, code-first orchestration with minimal operational overhead
- Dagster: Architected for data platforms where asset lineage and software engineering practices are important

For this assignment, Prefect is the clear choice because:
- Zero infrastructure overhead: Prefect Cloud's free tier eliminates setup complexity, letting me focus on the AI pipeline rather than DevOps
- Dynamic workflow generation: Since document count varies at runtime, Prefect's dynamic task creation (@task decorators) handles this naturally without the DAG constraints of Airflow
- Developer velocity: Native Python with local-to-cloud deployment means faster iteration and testing
- Built-in resilience: First-class retry logic and failure handling for LLM API calls (rate limits, timeouts)

However, the "best" tool depends entirely on context. Below is my comparative analysis:

| **Criterion** | **Prefect** | **Dagster** | **Airflow** |
|---------------|-------------|-------------|-------------|
| **Primary Use Case** | Task orchestration with event-driven flexibility | Data asset management & lineage tracking | Scheduled batch processing at enterprise scale |
| **Best Fit For** | • Greenfield projects<br>• Small-to-medium teams<br>• Fast iteration cycles<br>• Variable/dynamic workflows | • Data platforms<br>• Teams prioritizing testability & software engineering practices<br>• Complex data lineage requirements | • Established enterprises<br>• 100+ workflows<br>• Heavy compliance/governance needs |
| **Setup Complexity** | ✅ **Minimal** – Cloud-native, works immediately with free tier | ⚠️ **Moderate** – Requires upfront configuration and mental model shift to "assets" | ❌ **High** – Requires scheduler, webserver, database, worker infrastructure |
| **Dynamic Workflows** | ✅ Tasks created at runtime (`submit()` pattern) | ⚠️ Partitions-based – Dynamic partitions allow flexibility but require pre-registration step | ❌ Static DAGs defined upfront (workarounds exist but are hacky) |
| **Data Passing** | ✅ Native Python returns between tasks | ✅ Explicit I/O managers with type checking | ⚠️ XComs (limited to metadata, not data-heavy) |
| **Local Development** | ✅ Excellent – run locally, deploy seamlessly | ✅ Strong testing framework built-in | ❌ Difficult – production-coupled, hard to replicate locally |
| **Community & Ecosystem** | ⚠️ Growing but smaller than Airflow | ⚠️ Smallest community of the three | ✅ Massive – integrations with everything, extensive docs |
| **Operational Overhead** | ✅ **Low** (cloud-managed) to ⚠️ **Medium** (self-hosted) | ⚠️ **Medium** – More hands-on infrastructure than Prefect | ❌ **High** – Significant DevOps investment required |
| **Cost** | Free tier sufficient for most small projects; paid plans scale predictably | Core open-source; Cloud options available with hybrid/serverless models | Open-source but infrastructure have costs for managed options |
| **Learning Curve** | ✅ **Gentle** – If you know Python, you know Prefect | ⚠️ **Steep** – Requires rethinking workflows as data assets | ⚠️ **Moderate-to-Steep** – Lots of configuration, gotchas around DAG execution |
| **Avoid When** | • Large orgs requiring strict governance<br>• Need maximum control over infrastructure | • Simple use cases with tight deadlines<br>• Team not ready for asset-first thinking | • Heavy inter-task data communication<br>• Small team without DevOps capacity<br>• Need for dynamic task generation |

---

Decision Framework
Choose Prefect if: 
- You're a small team that needs to ship fast Workflow structure varies at runtime (like variable document counts)
- You want cloud-first deployment without infrastructure management

Choose Dagster if:
- You're building a long-term data platform (not just pipelines)
- Data lineage and quality are critical business requirements
- Your team values strong typing, testability, and software engineering rigor
- You have DBT models (Dagster's integration is best-in-class)

Choose Airflow if:
- You're at enterprise scale (large number of workflows)
- Workflows are static, scheduled batch jobs
- You have dedicated DevOps support
