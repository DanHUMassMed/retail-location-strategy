import logging
import asyncio
import json
import sys
import os

# Add project root to sys path to ensure imports resolve
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sub_agent_harness.harness import TestHarness
from retail_location_strategy.sub_agents.report_generator.agent import report_generation_pipeline

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def run_report_generator_test():
    logger.info("Starting Report Generator Sub-Agent Test...")
    
    # 1. Initialize Harness
    harness = TestHarness(app_name="report_generation_pipeline")
    
    # 2. Create Session from predefined state file
    session_file_path = os.path.join(os.path.dirname(__file__), "session3.json")
    await harness.create_session(session_file=session_file_path)
    
    # Optional: seed additional state dynamically if needed
    # await harness.seed_state({"foo": "bar"})
    
    # 3. Instantiate Sub-Agent
    await harness.instantiate_sub_agent(report_generation_pipeline)
    
    # 4. Execute
    logger.info("Executing Report Generator...")
    # Passing no prompt message as the agent should trigger off the current state 
    # and we want to resume exactly from this state. If a message is required to trigger 
    # the LlmAgent, we can add "Please perform the gap analysis".
    events = await harness.execute("Please call the report generation pipeline.")
    
    logger.info(f"Execution completed. Collected {len(events)} events.")
    
    # 5. Inspect Results
    final_state = await harness.inspect_results()
    
    logger.info("\n--- FINAL SESSION STATE ---")
    if "report_generation_result" in final_state:
        logger.info("Report generation result was successfully populated in the state!")
        report_generation_result = final_state["report_generation_result"]
        if isinstance(report_generation_result, (dict, list)):
            print(json.dumps(report_generation_result, indent=2))
        elif isinstance(report_generation_result, str):
            try:
                parsed = json.loads(report_generation_result)
                print(json.dumps(parsed, indent=2))
            except json.JSONDecodeError:
                print(report_generation_result)
        else:
            print(str(report_generation_result))
    else:
        logger.warning("Report generation result output not found in the final state. Check agent configuration or instructions.")

    # Print the keys in the state to verify
    logger.info(f"Available State Keys: {list(final_state.keys())}")

    try:
        with open("session.json", "w") as f:
            json.dump(final_state, f, indent=2)
        logger.info("Successfully saved final session state to session.json")
    except Exception as e:
        logger.error(f"Failed to save session to file: {e}")


if __name__ == "__main__":
    asyncio.run(run_report_generator_test())
