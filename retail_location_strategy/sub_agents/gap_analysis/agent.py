from google.adk.agents import LlmAgent
from google.genai import types

from ...config import config
from google.adk.code_executors.container_code_executor import ContainerCodeExecutor
from .callbacks import before_gap_analysis, after_gap_analysis
from .prompt import gap_analysis_instruction


class GapAnalysisAgent(LlmAgent):
    """LlmAgent with lazy ContainerCodeExecutor creation to avoid deepcopy/pickle issues.

    NOTE: The deepcopy issue is with the AG-UI framework. The framework is copying the full 
    root_agent state to the frontend. Since the ContainerCodeExecutor uses a socket connection, 
    it is not serializable and is causing the deepcopy/pickle issue."""

    def __init__(self, *args, **kwargs):
        # Remove code_executor from kwargs to prevent storing it on the agent
        kwargs.pop("code_executor", None)
        super().__init__(*args, **kwargs)

    def get_executor(self) -> ContainerCodeExecutor:
        """Create a new ContainerCodeExecutor on demand."""
        return ContainerCodeExecutor(image="docker-sandbox")

    # Override run method to inject the executor
    async def run(self, *args, **kwargs):
        executor = self.get_executor()
        # Use the executor in your code execution
        return await super().run(*args, code_executor=executor, **kwargs)


# Instantiate the agent
gap_analysis_agent = GapAnalysisAgent(
    name="GapAnalysisAgent",
    model=config.CODE_EXEC_MODEL,
    description="Performs quantitative gap analysis using Python code execution for zone rankings and viability scores",
    instruction=gap_analysis_instruction(),
    output_key="gap_analysis",
    before_agent_callback=before_gap_analysis,
    after_agent_callback=after_gap_analysis,
)