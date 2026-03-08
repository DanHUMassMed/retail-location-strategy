import logging
import json
import os
from typing import List

from sub_agent_harness.harness import TestHarness
from google.adk.agents import BaseAgent

logger = logging.getLogger(__name__)

async def run_agent_test(
    app_name: str,
    agent: BaseAgent,
    session_file_name: str,
    prompt: str,
    output_keys: List[str]
):
    """
    Generic execution flow for testing ADK sub-agents.
    """
    logger.info(f"Starting {agent.name} Test...")
    
    # 1. Initialize Harness
    harness = TestHarness(app_name=app_name)
    
    # 2. Create Session from predefined state file
    # Assuming this utility is called from scripts in the same directory
    session_file_path = os.path.join(os.path.dirname(__file__), session_file_name)
    await harness.create_session(session_file=session_file_path)
    
    # 3. Instantiate Sub-Agent
    await harness.instantiate_sub_agent(agent)
    
    # 4. Execute
    logger.info(f"Executing {agent.name}...")
    events = await harness.execute(prompt)
    
    logger.info(f"Execution completed. Collected {len(events)} events.")
    
    # 5. Inspect Results
    final_state = await harness.inspect_results()
    
    logger.info("\n--- FINAL SESSION STATE ---")
    for key in output_keys:
        if key in final_state:
            logger.info(f"Output '{key}' was successfully populated in the state!")
            data = final_state[key]
            if isinstance(data, (dict, list)):
                print(json.dumps(data, indent=2))
            elif isinstance(data, str):
                try:
                    parsed = json.loads(data)
                    print(json.dumps(parsed, indent=2))
                except json.JSONDecodeError:
                    print(data)
            else:
                print(str(data))
        else:
            logger.warning(f"Output '{key}' not found in the final state. Check agent configuration or instructions.")

    # Print the keys in the state to verify
    logger.info(f"Available State Keys: {list(final_state.keys())}")

    try:
        with open("session.json", "w") as f:
            json.dump(final_state, f, indent=2)
        logger.info("Successfully saved final session state to session.json")
    except Exception as e:
        logger.error(f"Failed to save session to file: {e}")
