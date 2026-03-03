import json
import logging
from datetime import datetime
from typing import Optional

from google.adk.agents.callback_context import CallbackContext
from google.genai import types

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("LocationStrategyPipeline")


def before_market_research(callback_context: CallbackContext) -> Optional[types.Content]:
    """Log start of market research phase and initialize pipeline tracking."""
    logger.info("=" * 60)
    logger.info("STAGE 1: MARKET RESEARCH - Starting")
    logger.info(f"  Target Location: {callback_context.state.get('target_location', 'Not set')}")
    logger.info(f"  Business Type: {callback_context.state.get('business_type', 'Not set')}")
    logger.info("=" * 60)

    # Set current date for state injection in agent instruction
    callback_context.state["current_date"] = datetime.now().strftime("%Y-%m-%d")

    # Initialize pipeline tracking
    callback_context.state["pipeline_stage"] = "market_research"
    callback_context.state["pipeline_start_time"] = datetime.now().isoformat()
    
    if "stages_completed" not in callback_context.state:
        callback_context.state["stages_completed"] = []

    return None  # Allow agent to proceed


def after_market_research(callback_context: CallbackContext) -> Optional[types.Content]:
    """Log completion of market research and update tracking."""
    findings = callback_context.state.get("market_research_findings", "")
    findings_len = len(findings) if isinstance(findings, str) else 0

    logger.info(f"STAGE 1: COMPLETE - Market research findings: {findings_len} characters")

    # Update stages completed
    stages = callback_context.state.get("stages_completed", [])
    stages.append("market_research")
    callback_context.state["stages_completed"] = stages

    return None

