from google.adk.agents import LlmAgent
from google.genai import types

from ...config import config
from google.adk.code_executors import BuiltInCodeExecutor
from .callbacks import before_gap_analysis, after_gap_analysis
from .prompt import gap_analysis_instruction

gap_analysis_agent = LlmAgent(
    name="GapAnalysisAgent",
    model=config.CODE_EXEC_MODEL,
    description="Performs quantitative gap analysis using Python code execution for zone rankings and viability scores",
    instruction=gap_analysis_instruction(),
    code_executor=BuiltInCodeExecutor(),
    output_key="gap_analysis",
    before_agent_callback=before_gap_analysis,
    after_agent_callback=after_gap_analysis,
)
