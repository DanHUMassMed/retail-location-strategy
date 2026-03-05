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

def before_strategy_advisor(callback_context: CallbackContext) -> Optional[types.Content]:
    """Log start of strategy synthesis phase."""
    logger.info("=" * 60)
    logger.info("STAGE 3: STRATEGY SYNTHESIS - Starting")
    logger.info("  Using extended reasoning with thinking mode...")
    logger.info("  Generating structured LocationIntelligenceReport...")
    logger.info("=" * 60)

    # Set current date for state injection in agent instruction
    callback_context.state["current_date"] = datetime.now().strftime("%Y-%m-%d")
    callback_context.state["pipeline_stage"] = "strategy_synthesis"

    return None


async def after_strategy_advisor(callback_context: CallbackContext) -> Optional[types.Content]:
    """Log completion and save JSON artifact."""
    report = callback_context.state.get("strategic_report", {})
    logger.info("STAGE 3: COMPLETE - Strategic report generated")

    # Save JSON artifact
    if report:
        try:
            # Handle both dict and Pydantic model
            if hasattr(report, "model_dump"):
                report_dict = report.model_dump()
            else:
                report_dict = report

            json_str = json.dumps(report_dict, indent=2, default=str)
            json_artifact = types.Part.from_bytes(
                data=json_str.encode('utf-8'),
                mime_type="application/json"
            )
            await callback_context.save_artifact("intelligence_report.json", json_artifact)
            logger.info("  Saved artifact: intelligence_report.json")
        except Exception as e:
            logger.warning(f"  Failed to save JSON artifact: {e}")

    stages = callback_context.state.get("stages_completed", [])
    stages.append("strategy_synthesis")
    callback_context.state["stages_completed"] = stages

    return None    