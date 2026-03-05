import logging
import asyncio
import json
import sys
import os

# Add project root to sys path to ensure imports resolve
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sub_agent_harness.harness import TestHarness
from retail_location_strategy.sub_agents.strategy_advisor.agent import strategy_advisor_agent

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def run_strategy_advisor_test():
    logger.info("Starting Strategy Advisor Sub-Agent Test...")
    
    # 1. Initialize Harness
    harness = TestHarness(app_name="retail_location_strategy")
    
    # 2. Create Session from predefined state file
    session_file_path = os.path.join(os.path.dirname(__file__), "session2.json")
    await harness.create_session(session_file=session_file_path)
    
    # Optional: seed additional state dynamically if needed
    # await harness.seed_state({"foo": "bar"})
    
    # 3. Instantiate Sub-Agent
    await harness.instantiate_sub_agent(strategy_advisor_agent)
    
    # 4. Execute
    logger.info("Executing Strategy Advisor...")
    # Passing no prompt message as the agent should trigger off the current state 
    # and we want to resume exactly from this state. If a message is required to trigger 
    # the LlmAgent, we can add "Please perform the gap analysis".
    events = await harness.execute("Please evaluate this location and generate strategy_advisor.")
    
    logger.info(f"Execution completed. Collected {len(events)} events.")
    
    # 5. Inspect Results
    final_state = await harness.inspect_results()
    
    logger.info("\n--- FINAL SESSION STATE ---")
    if "strategic_report" in final_state:
        logger.info("Strategic report was successfully populated in the state!")
        strategic_report = final_state["strategic_report"]
        if isinstance(strategic_report, (dict, list)):
            print(json.dumps(strategic_report, indent=2))
        elif isinstance(strategic_report, str):
            try:
                parsed = json.loads(strategic_report)
                print(json.dumps(parsed, indent=2))
            except json.JSONDecodeError:
                print(strategic_report)
        else:
            print(str(strategic_report))
    else:
        logger.warning("Strategic report output not found in the final state. Check agent configuration or instructions.")

    # Print the keys in the state to verify
    logger.info(f"Available State Keys: {list(final_state.keys())}")

    try:
        with open("session.json", "w") as f:
            json.dump(final_state, f, indent=2)
        logger.info("Successfully saved final session state to session.json")
    except Exception as e:
        logger.error(f"Failed to save session to file: {e}")


if __name__ == "__main__":
    asyncio.run(run_strategy_advisor_test())
