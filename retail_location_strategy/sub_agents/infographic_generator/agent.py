"""Infographic Generator Agent - Part 5 (Bonus) of the Location Strategy Pipeline.

This agent creates a visual infographic summary using Gemini's image generation
capabilities to provide an executive-ready visual summary of the analysis.
"""

from google.adk.agents import LlmAgent
from google.genai import types

from ...config import config

from .callbacks import before_infographic_generator, after_model_callback, after_infographic_generator
from .prompt import infographic_generator_instruction



infographic_generator_agent = LlmAgent(
    name="InfographicGeneratorAgent",
    model=config.MULTI_MODAL_MODEL,
    description="Generates visual infographic summary using Gemini image generation",
    instruction=infographic_generator_instruction(),
    generate_content_config=types.GenerateContentConfig(
        response_modalities=["TEXT", "IMAGE"],
        image_config=types.ImageConfig(
            aspect_ratio="16:9",
        )
    ),
    output_key="infographic_result",
    after_model_callback=after_model_callback,
    before_agent_callback=before_infographic_generator,
    after_agent_callback=after_infographic_generator,
)
