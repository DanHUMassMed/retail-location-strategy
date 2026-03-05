"""Intake Agent - Extracts target location and business type from user request.

This agent parses the user's natural language request and extracts the
required parameters (target_location, business_type) into session state
for use by subsequent agents in the pipeline.
"""

from typing import Optional
from google.adk.agents import LlmAgent
from pydantic import BaseModel, Field

from .prompt import intake_instruction
from .callbacks import before_intake, after_intake

from ...config import config


class UserRequest(BaseModel):
    """Structured output for parsing user's location strategy request."""

    target_location: str = Field(
        description="The geographic location/area to analyze (e.g., 'Worcester MA', 'Holden MA')"
    )
    business_type: str = Field(
        description="The type of business the user wants to open (e.g., 'coffee shop', 'bakery', 'gym', 'restaurant')"
    )
    additional_context: Optional[str] = Field(
        default=None,
        description="Any additional context or requirements mentioned by the user"
    )



intake_agent = LlmAgent(
    name="IntakeAgent",
    model=config.FAST_MODEL,
    description="Parses user request to extract target location and business type",
    instruction=intake_instruction(),
    output_schema=UserRequest,
    output_key="parsed_request",
    before_agent_callback=before_intake,
    after_agent_callback=after_intake,
)
