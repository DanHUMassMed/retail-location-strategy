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

def before_gap_analysis(callback_context: CallbackContext) -> Optional[types.Content]:
    """Log start of gap analysis phase."""
    logger.info("=" * 60)
    logger.info("STAGE 2B: GAP ANALYSIS - Starting")
    logger.info("  Executing Python code for quantitative market analysis...")
    logger.info("=" * 60)

    # Set current date for state injection in agent instruction
    callback_context.state["current_date"] = datetime.now().strftime("%Y-%m-%d")
    callback_context.state["pipeline_stage"] = "gap_analysis"

    # Workaround for AG-UI middleware issue: initialize state variable
    callback_context.state["gap_analysis"] = "Gap analysis being computed..."

    return None

def after_gap_analysis(callback_context: CallbackContext) -> Optional[types.Content]:
    """Log completion of gap analysis and extract executed Python code."""
    gap = callback_context.state.get("gap_analysis", "")
    gap_len = len(gap) if isinstance(gap, str) else 0

    logger.info(f"STAGE 2B: COMPLETE - Gap analysis: {gap_len} characters")

    # Extract Python code from the gap_analysis content first
    extracted_code = _extract_python_code_from_content(gap)

    # Try to extract from invocation context (BuiltInCodeExecutor uses executable_code parts)
    if not extracted_code:
        extracted_code = _extract_code_from_invocation(callback_context)

    if extracted_code:
        callback_context.state["gap_analysis_code"] = extracted_code
        logger.info(f"  Extracted Python code: {len(extracted_code)} characters")
    else:
        logger.info("  No Python code blocks found to extract")

    stages = callback_context.state.get("stages_completed", [])
    stages.append("gap_analysis")
    callback_context.state["stages_completed"] = stages

    return None    


def _extract_python_code_from_content(content: str) -> str:
    """Extract Python code blocks from markdown content."""
    import re

    if not content:
        return ""

    # Match fenced code blocks with python language specifier
    code_blocks = []
    pattern = r'```(?:python|py)\s*\n(.*?)```'
    matches = re.findall(pattern, content, re.DOTALL | re.IGNORECASE)

    for match in matches:
        code = match.strip()
        if code:
            code_blocks.append(code)

    return "\n\n# ---\n\n".join(code_blocks)

# Try to extract from invocation context (BuiltInCodeExecutor uses executable_code parts)
def _extract_code_from_invocation(callback_context: CallbackContext) -> str:
    """Extract Python code from invocation context session events."""
    code_blocks = []

    try:
        # Access via the private _invocation_context as shown in ADK docs
        invocation = getattr(callback_context, '_invocation_context', None) or \
                     getattr(callback_context, 'invocation_context', None)

        if not invocation:
            logger.debug("No invocation context available")
            return ""

        # Access session from invocation context
        session = getattr(invocation, 'session', None)
        if not session:
            logger.debug("No session in invocation context")
            return ""

        # Get events from session
        events = getattr(session, 'events', None) or []
        logger.debug(f"Found {len(events)} events in session")

        for event in events:
            # Get content from event
            content = getattr(event, 'content', None)
            if not content:
                continue

            # Get parts from content
            parts = getattr(content, 'parts', None) or []
            for part in parts:
                # Check for executable_code (Gemini native code execution)
                exec_code = getattr(part, 'executable_code', None)
                if exec_code:
                    code = getattr(exec_code, 'code', None)
                    if code and code.strip():
                        code_blocks.append(code.strip())
                        logger.debug(f"Found executable_code: {len(code)} chars")

        if code_blocks:
            logger.info(f"  Found {len(code_blocks)} code blocks from session events")

    except Exception as e:
        logger.warning(f"Error extracting code from invocation context: {e}")
        import traceback
        logger.debug(traceback.format_exc())

    return "\n\n# --- Next Code Block ---\n\n".join(code_blocks)
