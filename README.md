# Financial Document Analyzer

## Project Overview

The **Financial Document Analyzer** is an AI-powered system designed to process financial documents, corporate reports, and statements using CrewAI agents. The system extracts key financial metrics, analyzes investment opportunities, and provides comprehensive risk assessments to support informed decision-making.

## Features

- 📄 **PDF Document Processing**: Upload and analyze financial documents in PDF format
- 🤖 **AI-Powered Analysis**: Multi-agent system for comprehensive financial analysis
- 💰 **Investment Recommendations**: Buy/Hold/Sell recommendations based on financial data
- ⚠️ **Risk Assessment**: Analysis of liquidity, regulatory, market, and operational risks
- 📊 **Market Insights**: Extract key market trends and financial indicators
- 🔌 **RESTful API**: Clean API interface for easy integration

---

## Bugs Found and How They Were Fixed

During development, several critical issues were identified and resolved to ensure a robust, production-ready system:

### 1. **Agent Configuration Issues** (`agents.py`)
**Problem**: Agents had inconsistent tool references and missing LLM configurations, causing initialization failures.

**Symptoms**:
- Agents couldn't access required tools
- Missing or incorrect LLM instances
- Inconsistent tool naming across agents

**Fix Implemented**:
```python
# Before: Inconsistent tool references
agent = Agent(
    role="Financial Analyst",
    tools=[pdf_tool, search]  # Inconsistent naming
)

# After: Standardized tool configuration
agent = Agent(
    role="Financial Analyst",
    tools=[financial_pdf_tool, search_tool],
    llm=ChatOpenAI(model="gpt-4"),
    verbose=True
)
```

### 2. **Task Definition Problems** (`financial_tasks.py`)
**Problem**: Tasks had unclear inputs/outputs and inconsistent agent-task linkage.

**Symptoms**:
- Tasks failing due to undefined expected outputs
- Inconsistent data flow between tasks
- Agent-task mismatches

**Fix Implemented**:
```python
# Before: Vague task definition
task = Task(
    description="Analyze the document",
    agent=financial_analyst
)

# After: Clear, structured task definition
task = Task(
    description="Extract and analyze key financial metrics from the uploaded document, including revenue, profit margins, cash flow, and debt ratios.",
    expected_output="Structured financial analysis with key metrics, trends, and preliminary insights in JSON format",
    agent=financial_analyst,
    tools=[financial_pdf_tool]
)
```

### 3. **Tool Implementation Issues** (`tools.py`)
**Problem**: PDF reading tools were inconsistent with async/sync mixing and placeholder methods.

**Symptoms**:
- Async methods without proper handling
- Inconsistent PDF reading results
- Missing tool normalization

**Fix Implemented**:
```python
# Before: Mixed async/sync issues
async def read_pdf(file_path):
    # Async method without proper handling
    pass

# After: Consistent sync implementation
from crewai_tools import FileReadTool

financial_pdf_tool = FileReadTool(
    file_path="./data/",
    description="Tool for reading financial PDF documents and extracting text content"
)

class FinancialDocumentReadTool(BaseModel):
    """Normalized financial document reader"""
    def process_document(self, file_path: str) -> dict:
        # Consistent processing logic
        return {"content": extracted_text, "metadata": file_info}
```

### 4. **API Endpoint Issues** (`app.py`)
**Problem**: File upload handling was unreliable and CrewAI integration had execution issues.

**Symptoms**:
- File uploads failing
- Crew execution not returning structured results
- No proper cleanup of temporary files

**Fix Implemented**:
```python
# Before: Basic file handling
@app.post("/analyze")
async def analyze_document(file: UploadFile):
    content = await file.read()
    # No proper file saving or cleanup

# After: Robust file handling with cleanup
@app.post("/analyze")
async def analyze_document(file: UploadFile, query: str = "Analyze financial document"):
    file_path = None
    try:
        # Save uploaded file
        file_path = f"./temp/{file.filename}"
        with open(file_path, "wb") as f:
            f.write(await file.read())
        
        # Process with crew
        crew = build_financial_crew(file_path)
        result = crew.kickoff(inputs={"query": query, "file_path": file_path})
        
        return {
            "status": "success",
            "analysis": result,
            "file_info": {"name": file.filename, "size": file.size}
        }
    finally:
        # Cleanup temporary file
        if file_path and os.path.exists(file_path):
            os.remove(file_path)
```

---

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- OpenAI API key
- Serper API key (for web search functionality)

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd Financial-Document-Analyzer
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

**Key Dependencies:**
- `crewai`: Multi-agent framework
- `fastapi`: Web framework
- `python-multipart`: File upload support
- `openai`: LLM integration
- `PyPDF2`: PDF processing
- `python-dotenv`: Environment management

### 3. Environment Configuration

Create a `.env` file in the root directory:

```env
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Serper Search API (for market research)
SERPER_API_KEY=your_serper_api_key_here

# Optional: Model configurations
OPENAI_MODEL=gpt-4
OPENAI_TEMPERATURE=0.1
```

### 4. Directory Structure Setup

Create necessary directories:

```bash
mkdir -p data temp logs
```

**Project Structure:**
```
Financial-Document-Analyzer/
├── agents.py              # CrewAI agent definitions
├── financial_tasks.py     # Task configurations
├── tools.py              # Custom tools and utilities
├── app.py                # FastAPI application
├── requirements.txt      # Dependencies
├── .env                  # Environment variables
├── data/                 # Sample documents
├── temp/                 # Temporary file storage
└── README.md            # Project documentation
```

### 5. Add Sample Financial Documents

Download sample financial documents for testing:

```bash
# Example: Tesla Q2 2024 Financial Report
wget "https://www.tesla.com/sites/default/files/downloads/TSLA-Q2-2024-Update.pdf" -O data/tesla_q2_2024.pdf
```

Or manually add any corporate financial PDF to the `data/` directory.

---

## Usage Instructions

### 1. Start the API Server

```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://127.0.0.1:8000`

### 2. Verify Installation

Check the health endpoint:

```bash
curl http://127.0.0.1:8000/
```

Expected response:
```json
{
  "status": "healthy",
  "message": "Financial Document Analyzer API is running",
  "version": "1.0.0"
}
```

---

## API Documentation

### Base URL
```
http://127.0.0.1:8000
```

### Endpoints

#### 1. Health Check
**GET** `/`

Returns the API status and version information.

**Response:**
```json
{
  "status": "healthy",
  "message": "Financial Document Analyzer API is running",
  "version": "1.0.0"
}
```

#### 2. Analyze Financial Document
**POST** `/analyze`

Analyzes an uploaded financial PDF document using AI agents.

**Parameters:**
- `file` (required): Financial document in PDF format (multipart/form-data)
- `query` (optional): Specific analysis instructions or focus areas

**Content-Type:** `multipart/form-data`

**Example Request (cURL):**
```bash
curl -X POST "http://127.0.0.1:8000/analyze" \
  -F "file=@data/tesla_q2_2024.pdf" \
  -F "query=Analyze Tesla's Q2 2024 financials for investment potential and risk factors"
```

**Example Request (Python):**
```python
import requests

url = "http://127.0.0.1:8000/analyze"

with open("data/tesla_q2_2024.pdf", "rb") as f:
    files = {"file": ("tesla_q2_2024.pdf", f, "application/pdf")}
    data = {"query": "Analyze for investment potential"}
    
    response = requests.post(url, files=files, data=data)
    result = response.json()
```

**Response Format:**
```json
{
  "status": "success",
  "analysis": {
    "financial_summary": {
      "revenue": "$24.9B",
      "profit_margin": "19.3%",
      "cash_flow": "$2.5B",
      "debt_ratio": "0.12"
    },
    "investment_recommendation": {
      "decision": "Buy",
      "confidence": "High",
      "reasoning": "Strong financial performance with improving margins",
      "target_price": "$280"
    },
    "risk_assessment": {
      "overall_risk": "Medium",
      "liquidity_risk": "Low",
      "market_risk": "Medium", 
      "regulatory_risk": "Low",
      "operational_risk": "Low"
    },
    "market_insights": [
      "EV market growth continues strong",
      "Regulatory environment favorable",
      "Supply chain improvements visible"
    ]
  },
  "file_info": {
    "name": "tesla_q2_2024.pdf",
    "size": 2048576,
    "processed_at": "2024-03-15T10:30:00Z"
  }
}
```

**Error Response:**
```json
{
  "status": "error",
  "message": "Failed to process document",
  "error_details": {
    "type": "ValidationError",
    "description": "Invalid PDF format or corrupted file"
  }
}
```

### Response Codes

| Code | Description |
|------|-------------|
| 200 | Success - Document analyzed successfully |
| 400 | Bad Request - Invalid file format or parameters |
| 413 | Payload Too Large - File size exceeds limit (10MB) |
| 422 | Unprocessable Entity - Invalid request format |
| 500 | Internal Server Error - Processing failed |

---

## Testing

### Local Testing

1. **Basic Functionality Test:**
```bash
# Test with sample document
curl -X POST "http://127.0.0.1:8000/analyze" \
  -F "file=@data/sample.pdf" \
  -F "query=Basic financial analysis"
```

2. **Integration Test:**
```python
# test_api.py
import requests
import os

def test_analyze_endpoint():
    url = "http://127.0.0.1:8000/analyze"
    file_path = "data/tesla_q2_2024.pdf"
    
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            files = {"file": (file_path, f, "application/pdf")}
            response = requests.post(url, files=files)
            
        assert response.status_code == 200
        data = response.json()
        assert "analysis" in data
        assert "investment_recommendation" in data["analysis"]
    else:
        print(f"Test file {file_path} not found")

if __name__ == "__main__":
    test_analyze_endpoint()
```

### Debugging Tips

1. **Check API Keys:** Verify `.env` file contains valid API keys
2. **File Format:** Ensure uploaded files are valid PDFs with readable text
3. **Logs:** Monitor terminal output for agent processing steps
4. **Memory:** Large PDF files may require increased memory allocation

---

## Troubleshooting

### Common Issues

1. **"OpenAI API key not found"**
   - Solution: Check `.env` file and restart the server

2. **"PDF parsing failed"**
   - Solution: Ensure PDF contains extractable text (not scanned images)

3. **"Agent execution timeout"**
   - Solution: Check internet connection for API calls and reduce document size

4. **"File too large"**
   - Solution: Current limit is 10MB. Split large documents or increase limit in `app.py`

### Performance Optimization

- Use GPU-enabled instances for faster LLM processing
- Implement caching for repeated document analysis
- Consider async processing for large documents

---

## License

This project is licensed under the MIT License. See LICENSE file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes and test thoroughly
4. Submit a pull request with detailed description

---

**Note:** This system is designed for demonstration and development purposes. For production use, implement additional security measures, rate limiting, and error handling.
