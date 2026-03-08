import logging
import asyncio
import sys
import os

# Add project root to sys path to ensure imports resolve
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sub_agent_harness.utils import run_agent_test
from retail_location_strategy.sub_agents.strategy_advisor.agent import strategy_advisor_agent

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def run_strategy_advisor_test():
    await run_agent_test(
        app_name="retail_location_strategy",
        agent=strategy_advisor_agent,
        session_file_name="session2.json",
        prompt="Please evaluate this location and generate strategy_advisor.",
        output_keys=["strategic_report"]
    )

if __name__ == "__main__":
    asyncio.run(run_strategy_advisor_test())
