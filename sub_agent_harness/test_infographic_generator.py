import logging
import asyncio
import sys
import os

# Add project root to sys path to ensure imports resolve
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sub_agent_harness.utils import run_agent_test
from retail_location_strategy.sub_agents.infographic_generator.agent import infographic_generator_agent

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def run_infographic_generator_test():
    await run_agent_test(
        app_name="retail_location_strategy",
        agent=infographic_generator_agent,
        session_file_name="session3.json",
        prompt="Please evaluate this location and generate an infographic.",
        output_keys=["infographic_result"]
    )

if __name__ == "__main__":
    asyncio.run(run_infographic_generator_test())
