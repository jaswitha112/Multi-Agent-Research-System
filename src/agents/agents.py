import os
from dotenv import load_dotenv

from langchain.agents import create_agent
from langchain_openrouter import ChatOpenRouter
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from src.tools.tools import web_search, scrape_url


# ============================================================
# Load environment variables
# ============================================================

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

if not OPENROUTER_API_KEY:
    raise ValueError(
        "OPENROUTER_API_KEY is not set. "
        "Add it to your .env file or Render Environment Variables."
    )


# ============================================================
# OpenRouter Model
# ============================================================

llm = ChatOpenRouter(
    model="openrouter/free",
    temperature=0,
    api_key=OPENROUTER_API_KEY,
    max_retries=2,
)


# ============================================================
# 1. Search Agent
# ============================================================

def build_search_agent():

    return create_agent(
        model=llm,
        tools=[web_search],
    )


# ============================================================
# 2. Reader Agent
# ============================================================

def build_reader_agent():

    return create_agent(
        model=llm,
        tools=[scrape_url],
    )


# ============================================================
# 3. Writer Chain
# ============================================================

writer_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
You are an expert research writer.

Write clear, structured, factual and professional research reports.

Important rules:
- Use only the research provided.
- Do not invent facts.
- Do not invent URLs.
- Clearly organize the information.
- Give at least 3 key findings.
"""
    ),

    (
        "human",
        """
Write a detailed research report on the topic below.

Topic:
{topic}

Research Gathered:
{research}

Use this structure:

# Introduction

# Key Findings

1. Finding 1
2. Finding 2
3. Finding 3

# Conclusion

# Sources

List all URLs that appear in the research.

Be factual, detailed and professional.
"""
    ),
])


writer_chain = writer_prompt | llm | StrOutputParser()


# ============================================================
# 4. Critic Chain
# ============================================================

critic_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
You are a sharp and constructive research critic.

Evaluate the report for:

- factual quality
- completeness
- clarity
- logical consistency
- source quality

Be honest and specific.
"""
    ),

    (
        "human",
        """
Review the research report below.

Report:

{report}

Respond using exactly this structure:

Score: X/10

Strengths:
- ...
- ...

Areas to Improve:
- ...
- ...

One line verdict:
...
"""
    ),
])


critic_chain = critic_prompt | llm | StrOutputParser()