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

def before_report_generator(callback_context: CallbackContext) -> Optional[types.Content]:
    """Log start of report generation phase."""
    logger.info("=" * 60)
    logger.info("STAGE 4: REPORT GENERATION - Starting")
    logger.info("  Generating McKinsey/BCG style HTML executive report...")
    logger.info("=" * 60)

    # Set current date for state injection in agent instruction
    callback_context.state["current_date"] = datetime.now().strftime("%Y-%m-%d")
    callback_context.state["pipeline_stage"] = "report_generation"

    return None


def after_report_generator(callback_context: CallbackContext) -> Optional[types.Content]:
    """Log completion of report generation.

    Note: This callback just logs completion.
    """
    # The report_generation_result from output_key contains the LLM's text response,
    # not the tool's return dict. The artifact is saved directly in the tool.
    logger.info("STAGE 4: COMPLETE - HTML report generation finished")
    logger.info("  (Artifact saved directly by generate_html_report tool)")

    stages = callback_context.state.get("stages_completed", [])
    stages.append("report_generation")
    callback_context.state["stages_completed"] = stages

    return None