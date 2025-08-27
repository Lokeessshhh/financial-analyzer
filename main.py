# app.py
import os
import uuid
import shutil
from typing import Dict, Any

from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from dotenv import load_dotenv
from crewai import Crew, Process

from agents import financial_analyst, verifier, investment_advisor, risk_assessor
from financial_tasks import (
    verification,
    analyze_financial_document,
    investment_analysis,
    risk_assessment,
)

load_dotenv()

app = FastAPI(title="Financial Document Analyzer")


def build_financial_crew() -> Crew:
    """
    Assemble the full verification → analysis → investment → risk pipeline.
    """
    return Crew(
        agents=[verifier, financial_analyst, investment_advisor, risk_assessor],
        tasks=[
            verification,
            analyze_financial_document,
            investment_analysis,
            risk_assessment,
        ],
        process=Process.sequential,
        verbose=True,
    )


def run_crew(query: str, file_path: str) -> Dict[str, Any]:
    """
    Run the financial analysis crew with shared inputs: query + file_path.
    All tasks/agents can reference {file_path} and {query}.
    """
    financial_crew = build_financial_crew()

    # These inputs are available in task descriptions as {file_path} and {query}
    result = financial_crew.kickoff(inputs={"query": query, "file_path": file_path})

    # Crew returns a structured object. Convert to a simple dict/string as you need.
    # Some Crew versions return a string; others a richer type. Safely stringify here.
    try:
        return result.to_dict() if hasattr(result, "to_dict") else {"result": str(result)}
    except Exception:
        return {"result": str(result)}


@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "Financial Document Analyzer API is running"}


@app.post("/analyze")
async def analyze_document(
    file: UploadFile = File(...),
    query: str = Form(default="Analyze this financial document for investment insights"),
):
    """
    Analyze a PDF financial document and provide investment recommendations.
    """
    if not query or not query.strip():
        query = "Analyze this financial document for investment insights"

    file_id = str(uuid.uuid4())
    os.makedirs("data", exist_ok=True)
    file_path = f"data/financial_document_{file_id}.pdf"

    try:
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        result = run_crew(query=query.strip(), file_path=file_path)

        return {
            "status": "success",
            "query": query.strip(),
            "analysis": result,
            "file_processed": file.filename,
            "file_path": file_path,  # kept for traceability/debug (remove if sensitive)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing financial document: {str(e)}")

    # NOTE: If you want to auto-clean after agents finish reading,
    # move cleanup into a background-safe workflow. Left disabled intentionally.
    # finally:
    #     try:
    #         if os.path.exists(file_path):
    #             os.remove(file_path)
    #     except Exception:
    #         pass


if __name__ == "__main__":
    import uvicorn
    # Run: uvicorn app:app --reload
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
