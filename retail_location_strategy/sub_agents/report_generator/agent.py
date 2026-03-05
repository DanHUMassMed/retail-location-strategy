"""Report Generator Agent - Part 4 of the Location Strategy Pipeline.

This agent generates a professional HTML executive report from the
structured LocationIntelligenceReport data.
"""

from google.adk.agents import LlmAgent
from google.adk.agents.sequential_agent import SequentialAgent
from google.adk.tools.agent_tool import AgentTool
from google.genai import types

from ...config import config
from ..format_report.agent import format_report_agent
from .callbacks import before_report_generator, after_report_generator
from .prompt import report_generator_instruction



report_generator_agent = LlmAgent(
    name="ReportGeneratorAgent",
    model=config.FAST_MODEL,
    description="Generate professional McKinsey/BCG-style executive report output markdown",
    instruction=report_generator_instruction(),
    output_key="report_generation_result",
    before_agent_callback=before_report_generator,
    after_agent_callback=after_report_generator,
)

report_generation_pipeline = SequentialAgent(
    name="ReportGenerationPipeline",
    sub_agents=[
        report_generator_agent,
        format_report_agent
    ]
)


