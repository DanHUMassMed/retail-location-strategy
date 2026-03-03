"""Competitor Analysis Agent - Part 2A of the Location Strategy Pipeline.

This agent maps competitors using the competitor_data tool to get
ground-truth data about existing businesses in the target area.
"""

from google.adk.agents import LlmAgent
from google.genai import types

from ...config import config
from ...tools.competitor_data import competitor_data
from .callbacks import before_competitor_mapping, after_competitor_mapping
from .prompt import competitor_analysis_instruction

competitor_analysis_agent = LlmAgent(
    name="CompetitorAnalysisAgent",
    model=config.FAST_MODEL,
    description="Analyze competitors using web data for ground-truth competitor data",
    instruction=competitor_analysis_instruction(),
    tools=[competitor_data],
    output_key="competitor_analysis",
    before_agent_callback=before_competitor_mapping,
    after_agent_callback=after_competitor_mapping,
)
