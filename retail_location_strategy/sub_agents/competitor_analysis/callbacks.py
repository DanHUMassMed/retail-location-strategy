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

def before_competitor_mapping(callback_context: CallbackContext) -> Optional[types.Content]:
    """Log start of competitor mapping phase."""
    logger.info("=" * 60)
    logger.info("STAGE 2A: COMPETITOR MAPPING - Starting")
    logger.info("  Using Google Maps Places API for real competitor data...")
    logger.info("=" * 60)

    # Set current date for state injection in agent instruction
    callback_context.state["current_date"] = datetime.now().strftime("%Y-%m-%d")
    callback_context.state["pipeline_stage"] = "competitor_mapping"

    # Workaround for AG-UI middleware issue: initialize state variable
    # The middleware may end agent prematurely after tool calls, preventing output_key from being set
    if "competitor_analysis" not in callback_context.state:
        callback_context.state["competitor_analysis"] = "Competitor data being collected via Google Maps API..."

    return None


def after_competitor_mapping(callback_context: CallbackContext) -> Optional[types.Content]:
    """Log completion of competitor mapping."""
    analysis = callback_context.state.get("competitor_analysis", "")
    analysis_len = len(analysis) if isinstance(analysis, str) else 0

    logger.info(f"STAGE 2A: COMPLETE - Competitor analysis: {analysis_len} characters")

    stages = callback_context.state.get("stages_completed", [])
    stages.append("competitor_mapping")
    callback_context.state["stages_completed"] = stages

    return None

