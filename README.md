# Financial Document Analyzer

## Project Overview
The **Financial Document Analyzer** is an AI-powered system designed to process financial documents, corporate reports, and statements. It uses intelligent agents to extract key financial metrics, analyze risks, and provide investment recommendations. This project leverages CrewAI agents and integrates PDF reading, financial analysis, investment insights, and risk assessment.

---

## Features
- Upload financial documents (PDF format)
- AI-powered financial analysis with agents
- Investment recommendations (Buy/Hold/Sell)
- Risk assessment (liquidity, regulatory, market, operational)
- Market insights extraction
- Seamless API interface for integration

---

## Bugs Found and Fixes
During the initial development, the following issues were identified and fixed:

| File | Bug / Issue | Fix Implemented |
|------|-------------|----------------|
| `agents.py` | Incorrect or missing tool references; some agents lacked proper LLM configuration | Fixed agent definitions, ensured all agents use `financial_pdf_tool` and `search_tool`, and properly configured `ChatOpenAI` LLM instance |
| `financial_tasks.py` | Tasks were using inconsistent inputs and unclear expected outputs | Standardized all tasks with clear `description` and `expected_output`, ensured correct agent and tool references for each task |
| `tools.py` | PDF reader tools were inconsistent; some methods were async without proper handling | Created a consistent `financial_pdf_tool` using `FileReadTool`, added a `FinancialDocumentReadTool` class for normalization, fixed placeholder analysis methods |
| `app.py` | File upload handling and CrewAI kickoff logic had issues; some functions were not re-usable | Refactored `analyze_document` endpoint, added proper file saving and cleanup, created a reusable `build_financial_crew` function, ensured `run_crew` handles structured results |

> ✅ These fixes ensure the system works end-to-end: file upload → agent processing → analysis → investment/risk output.

---

## Setup Instructions

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd Financial-Document-Analyzer
Install dependencies

bash
Copy code
pip install -r requirement.txt
Environment Variables

Create a .env file in the root directory.

Add API keys for LLMs and search tools:

ini
Copy code
OPENAI_API_KEY=your_openai_api_key
SERPER_API_KEY=your_serper_api_key
Add Sample Financial Document

Download a sample document, e.g., Tesla Q2 2025 update:

ruby
Copy code
https://www.tesla.com/sites/default/files/downloads/TSLA-Q2-2025-Update.pdf
Save as data/sample.pdf in the project directory.

Usage Instructions
1. Run API
bash
Copy code
uvicorn app:app --reload
Open http://127.0.0.1:8000 to verify the health endpoint.

2. Analyze Financial Document
Endpoint: POST /analyze

Form parameters:

file: PDF financial document

query (optional): Analysis instruction

Example using cURL:

bash
Copy code
curl -X POST "http://127.0.0.1:8000/analyze" \
  -F "file=@data/sample.pdf" \
  -F "query=Analyze Tesla Q2 2025 financials for investment insights"
Response includes:

AI analysis summary

Investment recommendation

Risk assessment

Processed file information

Debugging & Testing Tips
Make sure uploaded PDFs are valid financial documents.

If agents return errors, check .env for API keys.

To test locally, replace data/sample.pdf with other financial PDFs.

Logs are visible in the terminal for agent processing steps.

Optional Enhancements
Integrate Celery for asynchronous task processing.

Use Kafka for real-time financial event streaming.

Add frontend dashboard for visualization of analysis and recommendations.

