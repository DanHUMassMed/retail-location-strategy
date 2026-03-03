from typing import Optional
from google.adk.agents.callback_context import CallbackContext
from google.genai import types

def after_intake(callback_context: CallbackContext) -> Optional[types.Content]:
    """After intake, copy the parsed values to state for other agents."""
    parsed = callback_context.state.get("parsed_request", {})

    if isinstance(parsed, dict):
        # Extract values from parsed request
        callback_context.state["target_location"] = parsed.get("target_location", "")
        callback_context.state["business_type"] = parsed.get("business_type", "")
        callback_context.state["additional_context"] = parsed.get("additional_context", "")
    elif hasattr(parsed, "target_location"):
        # Handle Pydantic model
        callback_context.state["target_location"] = parsed.target_location
        callback_context.state["business_type"] = parsed.business_type
        callback_context.state["additional_context"] = parsed.additional_context or ""

    # Track intake stage completion
    stages = callback_context.state.get("stages_completed", [])
    stages.append("intake")
    callback_context.state["stages_completed"] = stages

    # Note: current_date is set in each agent's before_callback to ensure it's always available
    return None

