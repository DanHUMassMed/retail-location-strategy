"""Market Research Agent - Part 1 of the Location Strategy Pipeline.

This agent validates macro market viability using live web data from Google Search.
It researches demographics, market trends, and commercial viability.
"""

from google.adk.agents import LlmAgent
from google.adk.tools import google_search
from google.genai import types

from ...config import config
from ...tools.searxng_search import searxng_search
from .callbacks import before_market_research, after_market_research
from .prompt import market_research_instruction


market_research_agent = LlmAgent(
    name="MarketResearchAgent",
    model=config.FAST_MODEL,
    description="Researches market viability using SearXNG for real-time demographics, trends, and commercial data",
    instruction=market_research_instruction(),
    tools=[searxng_search],
    output_key="market_research_findings",
    before_agent_callback=before_market_research,
    after_agent_callback=after_market_research,
)
