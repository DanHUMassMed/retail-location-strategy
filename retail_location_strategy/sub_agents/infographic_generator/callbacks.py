
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

def before_infographic_generator(
    callback_context: CallbackContext,
) -> types.Content | None:
    """Log start of infographic generation phase."""
    logger.info("=" * 60)
    logger.info("STAGE 5: INFOGRAPHIC GENERATION - Starting")
    logger.info("  Calling Gemini image generation API...")
    logger.info("=" * 60)

    # Set current date for state injection in agent instruction
    callback_context.state["current_date"] = datetime.now().strftime("%Y-%m-%d")
    callback_context.state["pipeline_stage"] = "infographic_generation"

    return None

def after_infographic_generator(
    callback_context: CallbackContext,
) -> types.Content | None:
    """Log completion of infographic generation.

    Note: The artifact is now saved directly in the generate_infographic tool
    using tool_context.save_artifact(). This callback just logs completion.
    """
    # The infographic_result from output_key contains the LLM's text response,
    # not the tool's return dict. The artifact is saved directly in the tool.
    logger.info("STAGE 5: COMPLETE - Infographic generation finished")
    logger.info("  (Artifact saved directly by generate_infographic tool)")

    stages = callback_context.state.get("stages_completed", [])
    stages.append("infographic_generation")
    callback_context.state["stages_completed"] = stages

    # Log final pipeline summary
    logger.info("=" * 60)
    logger.info("PIPELINE COMPLETE")
    logger.info(f"  Stages completed: {stages}")
    logger.info(f"  Total stages: {len(stages)}/7")
    logger.info("=" * 60)

    return None

from google.adk.models import LlmResponse
from google.genai import types
import base64
import os
import json

async def after_model_callback(
    callback_context: CallbackContext, llm_response: LlmResponse
) -> LlmResponse | None:
    """Log model response and save generated image artifact to state."""
    logger.info("=" * 60)
    logger.info("MODEL RESPONSE (Extracting Image)")
    logger.info("=" * 60)

    # 1. DEBUGGING: Dump the entire raw response to a file so we can inspect what the model actually returned
    try:
        debug_path = os.path.join(os.getcwd(), "debug_response.json")
        with open(debug_path, "w") as f:
            f.write(llm_response.model_dump_json(indent=2))
        logger.info(f"DEBUG: Dumped full LlmResponse to {debug_path}")
    except Exception as dump_err:
        logger.warning(f"Failed to dump debug response: {dump_err}")

    try:
        if llm_response.content and llm_response.content.parts:
            found_image = False
            text_content = ""

            for i, part in enumerate(llm_response.content.parts):
                logger.info(f"Inspecting part {i} of response...")

                # Accumulate text in case the model returned a markdown description instead of an image
                if hasattr(part, "text") and part.text:
                    text_content += part.text

                # Check for inline_data (native image bytes)
                if hasattr(part, "inline_data") and part.inline_data:
                    logger.info("Found inline_data in response part. Extracting image...")
                    found_image = True
                    image_bytes = part.inline_data.data
                    mime_type = part.inline_data.mime_type or "image/png"

                    # Save the image directly as an artifact using callback_context
                    image_artifact = types.Part.from_bytes(
                        data=image_bytes,
                        mime_type=mime_type
                    )
                    artifact_filename = "infographic.png"
                    version = await callback_context.save_artifact(
                        filename=artifact_filename,
                        artifact=image_artifact
                    )
                    logger.info(f"Saved infographic artifact: {artifact_filename} (version {version})")

                    # Also store base64 in state for AG-UI frontend display
                    b64_image = base64.b64encode(image_bytes).decode('utf-8')
                    callback_context.state["infographic_base64"] = f"data:{mime_type};base64,{b64_image}"
                    callback_context.state["infographic_result"] = {
                        "status": "success",
                        "message": f"Infographic generated and saved as artifact '{artifact_filename}'",
                        "artifact_saved": True,
                        "artifact_filename": artifact_filename,
                        "artifact_version": version,
                        "mime_type": mime_type,
                    }
                    return None
            
            # If we got through all parts and didn't find an image, it means the model only gave us text
            if not found_image:
                logger.warning(f"No inline_data found. Model returned text only. Text length: {len(text_content)}")
                callback_context.state["infographic_result"] = {
                    "status": "error",
                    "error_message": "No image native bytes (inline_data) were generated in the response. Check debug_response.json.",
                    "fallback_text": text_content[:500] + "..." if len(text_content) > 500 else text_content
                }

        else:
            # llm_response.content or parts is empty
            logger.error("llm_response.content or llm_response.content.parts is empty/None!")
            callback_context.state["infographic_result"] = {
                "status": "error",
                "error_message": "Response content was empty.",
            }

    except Exception as e:
        import traceback
        logger.error(f"Failed to extract infographic: {e}\n{traceback.format_exc()}")
        callback_context.state["infographic_result"] = {
            "status": "error",
            "error_message": f"Exception during extraction: {str(e)}",
        }

    return None