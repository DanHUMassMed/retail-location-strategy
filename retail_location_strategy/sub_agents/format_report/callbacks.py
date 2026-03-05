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


def before_format_report(callback_context: CallbackContext) -> Optional[types.Content]:
    """Log start of format report phase and initialize pipeline tracking."""

    callback_context.state["current_date"] = datetime.now().strftime("%Y-%m-%d")
    return None  # Allow agent to proceed

async def after_format_report(callback_context: CallbackContext) -> Optional[types.Content]:
    """After format report, copy the parsed values to state for other agents."""
    html_report_content = callback_context.state.get("html_report_content", {})

    html_code = html_report_content
    # Strip markdown code fences if present
    if html_code.startswith("```"):
        # Remove opening fence (```html or ```)
        if html_code.startswith("```html"):
            html_code = html_code[7:]
        elif html_code.startswith("```HTML"):
            html_code = html_code[7:]
        else:
            html_code = html_code[3:]

        # Remove closing fence
        if html_code.rstrip().endswith("```"):
            html_code = html_code.rstrip()[:-3]

        html_code = html_code.strip()

    # Save as artifact with proper MIME type so it appears in ADK web UI
    html_artifact = types.Part.from_bytes(
        data=html_code.encode('utf-8'),
        mime_type="text/html"
    )
    artifact_filename = "executive_report.html"

    version = await callback_context.save_artifact(
        filename=artifact_filename,
        artifact=html_artifact
    )

    # Also store in state for AG-UI frontend display
    callback_context.state["html_report_content"] = html_code
    logger.info(f"html_report_content: {html_report_content}")
    logger.info(f"Saved HTML report artifact: {artifact_filename} (version {version})")

    return None