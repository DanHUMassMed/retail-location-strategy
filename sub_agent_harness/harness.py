import json
import logging
from typing import Dict, Any, Optional
from google.adk.agents import BaseAgent
from google.adk.sessions import InMemorySessionService, Session
from google.adk.artifacts import InMemoryArtifactService
from google.adk.runners import Runner
from google.genai import types

logger = logging.getLogger(__name__)

class TestHarness:
    """
    Test harness to initialize, seed, and run an ADK BaseAgent in isolation for testing.
    """
    def __init__(self, app_name: str = "test_app", user_id: str = "test_user", session_id: str = "test_session"):
        self.app_name = app_name
        self.user_id = user_id
        self.session_id = session_id
        self.session_service = InMemorySessionService()
        self.artifact_service = InMemoryArtifactService()
        self.runner: Optional[Runner] = None
        self.agent: Optional[BaseAgent] = None

    async def create_session(self, initial_state: dict = None, session_file: str = None) -> Session:
        """
        Creates or loads a session. If a file path is provided, it extracts the state from the JSON.
        """
        state = initial_state or {}
        
        if session_file:
            try:
                with open(session_file, 'r', encoding='utf-8') as f:
                    file_data = json.load(f)
                    if "state" in file_data:
                        state.update(file_data["state"])
                    else:
                        state.update(file_data)
                logger.info(f"Loaded session state from {session_file}")
            except Exception as e:
                logger.error(f"Failed to load session file {session_file}: {e}")
                
        session = await self.session_service.create_session(
            app_name=self.app_name, 
            user_id=self.user_id, 
            session_id=self.session_id, 
            state=state
        )
        return session

    async def instantiate_sub_agent(self, agent: BaseAgent):
        """
        Registers an instance of BaseAgent to the Runner.
        """
        self.agent = agent
        self.runner = Runner(
            agent=self.agent,
            app_name=self.app_name,
            session_service=self.session_service,
            artifact_service=self.artifact_service
        )
        logger.info(f"Runner instantiated with agent: {self.agent.name}")

    async def seed_state(self, updates: dict):
        """
        Updates the existing session state with provided updates.
        """
        session = await self.session_service.get_session(
            app_name=self.app_name, 
            user_id=self.user_id, 
            session_id=self.session_id
        )
        if not session:
            logger.warning("Session not found; create_session() must be called first.")
            return

        session.state.update(updates)
        # Note: Depending on ADK version, state is updated via memory service or direct object reference
        # The InMemorySessionService returns the same object reference, so direct update works.
        logger.info("Session state seeded.")

    async def execute(self, message: str = "") -> list:
        """
        Executes the agent via runner.run_async() with the optional prompt.
        """
        if not self.runner:
            logger.error("Runner not instantiated. Call instantiate_sub_agent() first.")
            return []
            
        content = types.Content(role='user', parts=[types.Part(text=message)]) if message else None
        
        logger.info(f"Executing agent {self.agent.name}...")
        
        events_collected = []
        try:
            # For ADK, we yield events from run_async
            events = self.runner.run_async(
                user_id=self.user_id, 
                session_id=self.session_id, 
                new_message=content
            )
            async for event in events:
                events_collected.append(event)
                # If you wish to log specific event types
                if event.is_final_response() and event.content and event.content.parts:
                    part = event.content.parts[0]
                    if getattr(part, 'text', None):
                        logger.info(f"Agent generated a final response: {part.text[:100]}...")
                    elif getattr(part, 'functionCall', None):
                        logger.info(f"Agent generated a function call: {part.functionCall.name}")
        except Exception as e:
            import traceback
            logger.error(f"Execution failed: {e}\n{traceback.format_exc()}")
            
        return events_collected

    async def inspect_results(self) -> dict:
        """
        Returns the final session state.
        """
        session = await self.session_service.get_session(
            app_name=self.app_name, 
            user_id=self.user_id, 
            session_id=self.session_id
        )
        if not session:
            return {}
        return session.state
