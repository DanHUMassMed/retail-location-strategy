import logging
import asyncio
import json
import sys
import os

# Add project root to sys path to ensure imports resolve
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sub_agent_harness.harness import TestHarness
from retail_location_strategy.sub_agents.gap_analysis.agent import gap_analysis_agent

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def run_gap_analysis_test():
    logger.info("Starting Gap Analysis Sub-Agent Test...")
    
    # 1. Initialize Harness
    harness = TestHarness(app_name="retail_location_strategy")
    
    # 2. Create Session from predefined state file
    session_file_path = os.path.join(os.path.dirname(__file__), "session1.json")
    await harness.create_session(session_file=session_file_path)
    
    # Optional: seed additional state dynamically if needed
    # await harness.seed_state({"foo": "bar"})
    
    # 3. Instantiate Sub-Agent
    await harness.instantiate_sub_agent(gap_analysis_agent)
    
    # 4. Execute
    logger.info("Executing Gap Analysis...")
    # Passing no prompt message as the agent should trigger off the current state 
    # and we want to resume exactly from this state. If a message is required to trigger 
    # the LlmAgent, we can add "Please perform the gap analysis".
    events = await harness.execute("Please evaluate this location and generate gap_analysis.")
    
    logger.info(f"Execution completed. Collected {len(events)} events.")
    
    # 5. Inspect Results
    final_state = await harness.inspect_results()
    
    logger.info("\n--- FINAL SESSION STATE ---")
    if "gap_analysis" in final_state:
        logger.info("Gap analysis was successfully populated in the state!")
        gap_data = final_state["gap_analysis"]
        if isinstance(gap_data, (dict, list)):
            print(json.dumps(gap_data, indent=2))
        elif isinstance(gap_data, str):
            try:
                parsed = json.loads(gap_data)
                print(json.dumps(parsed, indent=2))
            except json.JSONDecodeError:
                print(gap_data)
        else:
            print(str(gap_data))
    else:
        logger.warning("Gap analysis output not found in the final state. Check agent configuration or instructions.")

    if "gap_analysis_code" in final_state:
        logger.info("Gap analysis code was successfully populated in the state!")
        gap_data = final_state["gap_analysis_code"]
        print(str(gap_data))
    else:
        logger.warning("gap_analysis_code output not found in the final state.")

    # Print the keys in the state to verify
    logger.info(f"Available State Keys: {list(final_state.keys())}")

    try:
        with open("session.json", "w") as f:
            json.dump(final_state, f, indent=2)
        logger.info("Successfully saved final session state to session.json")
    except Exception as e:
        logger.error(f"Failed to save session to file: {e}")


if __name__ == "__main__":
    asyncio.run(run_gap_analysis_test())
