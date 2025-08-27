# agents.py
from dotenv import load_dotenv
load_dotenv()

from crewai import Agent
from langchain_openai import ChatOpenAI  # requires OPENAI_API_KEY in .env

from tools import search_tool, financial_pdf_tool


# --- LLM (adjust model if needed) ---
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.2,
    max_tokens=1500,
)

# --- Agents ---
financial_analyst = Agent(
    role="Senior Financial Analyst",
    goal=(
        "Analyze uploaded financial documents and extract KPIs, trends, and signals to "
        "support informed investment decisions with clear, factual summaries."
    ),
    backstory=(
        "Experienced analyst specializing in corporate statements and earnings reports. "
        "Provides concise, evidence-backed insights."
    ),
    tools=[financial_pdf_tool, search_tool],
    llm=llm,
    verbose=True,
    memory=False,
    max_iter=3,
    max_rpm=3,
    allow_delegation=True,
)

verifier = Agent(
    role="Financial Document Verifier",
    goal=(
        "Verify the uploaded document is a valid financial report and contains credible financial data."
    ),
    backstory=(
        "Validation and compliance expert. Checks presence of statements, revenue data, "
        "and typical financial terminology."
    ),
    tools=[financial_pdf_tool],
    llm=llm,
    verbose=True,
    memory=False,
    max_iter=2,
    max_rpm=3,
    allow_delegation=False,
)

investment_advisor = Agent(
    role="Investment Advisor",
    goal=(
        "Provide risk-adjusted, well-reasoned Buy/Hold/Sell recommendations with supporting evidence."
    ),
    backstory=(
        "Independent advisor with deep market knowledge; balances upside with risks and compliance."
    ),
    tools=[financial_pdf_tool],
    llm=llm,
    verbose=True,
    memory=False,
    max_iter=3,
    max_rpm=3,
    allow_delegation=False,
)

risk_assessor = Agent(
    role="Risk Assessment Expert",
    goal=(
        "Identify and evaluate key risks (liquidity, regulatory, market, operational) with evidence."
    ),
    backstory=(
        "Professional risk manager specializing in risk factors in corporate reports."
    ),
    tools=[financial_pdf_tool],
    llm=llm,
    verbose=True,
    memory=False,
    max_iter=3,
    max_rpm=3,
    allow_delegation=False,
)
