"""Intake Agent - Extracts target location and business type from user request.

This agent parses the user's natural language request and extracts the
required parameters (target_location, business_type) into session state
for use by subsequent agents in the pipeline.
"""

from google.adk.agents import LlmAgent
from .prompt import format_report_instruction
from .callbacks import before_format_report, after_format_report
from ...config import config

format_report_agent = LlmAgent(
    name="FormatReportAgent",
    model=config.FAST_MODEL,
    description="Formats location strategy report into a McKinsey/BCG style HTML presentation",
    instruction=format_report_instruction(),
    output_key="html_report_content",
    before_agent_callback=before_format_report,
    after_agent_callback=after_format_report,
)