"""Strategy Advisor Agent - Part 3 of the Location Strategy Pipeline.

This agent synthesizes all findings into actionable recommendations using
extended reasoning (thinking mode) and outputs a structured JSON report.
"""

from google.adk.agents import LlmAgent
from google.adk.planners import BuiltInPlanner
from google.genai import types
from google.genai.types import ThinkingConfig

from ...config import config
from .callbacks import before_strategy_advisor, after_strategy_advisor
from .prompt import strategy_advisor_instruction
from .schema import LocationIntelligenceReport



strategy_advisor_agent = LlmAgent(
    name="StrategyAdvisorAgent",
    model=config.FAST_MODEL,
    description="Synthesizes findings into strategic recommendations using extended reasoning and structured output",
    instruction=strategy_advisor_instruction(),
    planner=BuiltInPlanner(
        thinking_config=ThinkingConfig(
            include_thoughts=False,  # Must be False when using output_schema
            thinking_budget=-1,  # -1 means unlimited thinking budget
        )
    ),
    output_schema=LocationIntelligenceReport,
    output_key="strategic_report",
    before_agent_callback=before_strategy_advisor,
    after_agent_callback=after_strategy_advisor,
)
