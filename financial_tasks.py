# financial_tasks.py
from crewai import Task
from agents import financial_analyst, verifier, investment_advisor, risk_assessor
from tools import search_tool, financial_pdf_tool

# Use the same reader instance everywhere to keep behavior consistent

# 1) Verification (run first)
verification = Task(
    description=(
        "Verify the uploaded document at {file_path} is a financial report. "
        "Use the Financial Document Reader with path={file_path} to inspect contents. "
        "Confirm presence of financial terminology (e.g., revenue, EBITDA, net income, cash flow), "
        "tables, or statements. Reject unrelated files."
    ),
    expected_output="""
{
  "is_financial_document": true,
  "confidence_score": 0.95,
  "reason": "Contains financial statements, revenue/net income data, and earnings commentary."
}
""".strip(),
    agent=verifier,
    tools=[financial_pdf_tool],
    async_execution=False,
)

# 2) Analysis
analyze_financial_document = Task(
    description=(
        "Analyze the financial document at {file_path}. "
        "Use the Financial Document Reader with path={file_path}. "
        "Extract company name, period, KPIs (revenue, net income, margins, EPS, FCF if present), "
        "guidance/outlook, and notable highlights with page references when possible."
    ),
    expected_output="""
{
  "company": "Company Name",
  "period": "e.g., Q2 2025 or FY2024",
  "kpis": [
    {"name": "Revenue", "value": "XX.XB", "unit": "USD", "source_page": 3},
    {"name": "Net Income", "value": "X.XXB", "unit": "USD", "source_page": 4}
  ],
  "highlights": ["Summary point 1", "Summary point 2"],
  "guidance": ["Forward-looking statements or outlook if present"]
}
""".strip(),
    agent=financial_analyst,
    tools=[financial_pdf_tool, search_tool],
    async_execution=False,
)

# 3) Investment Analysis
investment_analysis = Task(
    description=(
        "Using the analysis results, provide investment insights. "
        "Decide Buy/Hold/Sell with clear evidence, both bull and bear cases, "
        "and list near-term catalysts. Consider valuation/risks if mentioned in the document."
    ),
    expected_output="""
{
  "stance": "buy|hold|sell",
  "bull_case": "Reasons supporting upside potential",
  "bear_case": "Risks or reasons for caution",
  "catalysts": ["Upcoming events or trends that may impact performance"],
  "time_horizon_months": 6
}
""".strip(),
    agent=investment_advisor,
    tools=[financial_pdf_tool],
    async_execution=False,
)

# 4) Risk Assessment
risk_assessment = Task(
    description=(
        "Evaluate the key risks evident in the document at {file_path}. "
        "Identify risk categories such as regulatory, liquidity, market, and operational. "
        "Provide a brief justification with page/section reference if possible."
    ),
    expected_output="""
{
  "risks": [
    {
      "category": "Regulatory",
      "description": "Potential compliance or legal issues",
      "evidence": "Section reference or page number"
    },
    {
      "category": "Liquidity",
      "description": "Cash flow or short-term solvency concerns",
      "evidence": "Section reference or page number"
    }
  ]
}
""".strip(),
    agent=risk_assessor,
    tools=[financial_pdf_tool],
    async_execution=False,
)
