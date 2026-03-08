import logging
import asyncio
import sys
import os

# Add project root to sys path to ensure imports resolve
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sub_agent_harness.utils import run_agent_test
from retail_location_strategy.sub_agents.report_generator.agent import report_generation_pipeline

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def run_report_generator_test():
    await run_agent_test(
        app_name="report_generation_pipeline",
        agent=report_generation_pipeline,
        session_file_name="session3.json",
        prompt="Please call the report generation pipeline.",
        output_keys=["report_generation_result"]
    )

if __name__ == "__main__":
    asyncio.run(run_report_generator_test())
