import os
import sys
from pathlib import Path

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Add app directory to path for imports
# Structure: app/frontend/backend/main.py
app_dir = Path(__file__).parent.parent.parent  # app/
project_root = app_dir.parent  # retail-ai-location-strategy/
sys.path.insert(0, str(project_root))

# Import AG-UI middleware (CopilotKit official package)
from ag_ui_adk import ADKAgent, add_adk_fastapi_endpoint

# Import the EXISTING root_agent - no modifications needed
from .agent import root_agent

# Create AG-UI wrapper around the existing ADK agent
# Increase timeout for Strategy Synthesis which uses extended thinking
adk_agent = ADKAgent(
    adk_agent=root_agent,
    app_name="retail_location_strategy",
    user_id="demo_user",
    execution_timeout_seconds=1800,  # 30 minutes for full pipeline
    tool_timeout_seconds=600,  # 10 minutes for individual tools
)

# Create FastAPI app
app = FastAPI(
    title="Retail Location Strategy API",
    description="AG-UI compatible API for the Retail AI Location Strategy agent",
    version="1.0.0",
)

# CORS configuration for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "agent": "LocationStrategyPipeline"}


# Add AG-UI endpoint at root path
# This handles all AG-UI protocol communication
add_adk_fastapi_endpoint(app, adk_agent, path="/")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    print(f"Starting AG-UI server at http://0.0.0.0:{port}")
    print("Frontend should connect to this URL")
    uvicorn.run(app, host="0.0.0.0", port=port)
