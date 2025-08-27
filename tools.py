# tools.py
import os
from typing import Optional

from dotenv import load_dotenv
load_dotenv()

from crewai_tools import SerperDevTool
from langchain_community.document_loaders import PyPDFLoader
from crewai_tools import (
    FileReadTool,
    SerperDevTool,
)

# --- Web search tool (requires SERPER_API_KEY in .env) ---
search_tool = SerperDevTool()

# --- PDF Reader Tool ---
# This tool can read PDF files dynamically by passing the path at runtime
financial_pdf_tool = FileReadTool(
    name="Financial Document Reader",
    description="Reads and returns text from a PDF financial document at the provided path.",
    path=None  # Path will be passed dynamically when agents run
)

# --- Proper CrewAI BaseTool subclass for reading PDFs ---
class FinancialDocumentReadTool:
    """
    Reads and returns normalized text from a PDF located at `path`.
    Usage inside tasks/agents: call with `path=<file_path>`.
    """
    name: str = "Financial Document Reader"
    description: str = (
        "Reads and returns text from a PDF financial document at the provided file path."
    )

    def _run(self, path: Optional[str] = None) -> str:
        if not path:
            return "Error: No path provided to FinancialDocument Reader."
        if not os.path.exists(path):
            return f"Error: File not found at path: {path}"

        try:
            loader = PyPDFLoader(path)
            docs = loader.load()
        except Exception as e:
            return f"Error reading PDF: {e}"

        # Normalize whitespace and concatenate pages
        pages = []
        for d in docs:
            content = " ".join(d.page_content.split())
            pages.append(content)
        return "\n".join(pages)



## Creating Investment Analysis Tool
class InvestmentTool:
    @staticmethod
    def analyze_investment_tool(financial_document_data: str):
        """Analyze financial document data and extract simple insights"""
        if not financial_document_data:
            return "No data to analyze."

        # Simple placeholder analysis
        word_count = len(financial_document_data.split())
        return f"Document analyzed. Word count: {word_count}. (Detailed investment analysis logic pending.)"


## Creating Risk Assessment Tool
class RiskTool:
    @staticmethod
    def create_risk_assessment_tool(financial_document_data: str):
        """Basic risk assessment placeholder"""
        if not financial_document_data:
            return "No data available for risk assessment."

        # Simple placeholder
        return "Risk assessment complete. (Detailed risk logic pending.)"
