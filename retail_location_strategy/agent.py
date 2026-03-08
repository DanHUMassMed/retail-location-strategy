

"""Retail Location Strategy Agent - Root Agent Definition.

This module defines the root agent for the Location Strategy Pipeline.
It uses a SequentialAgent to orchestrate 6 specialized sub-agents:

1. MarketResearchAgent - Live web research with Google Search
2. CompetitorMappingAgent - Competitor mapping with Maps Places API
3. GapAnalysisAgent - Quantitative analysis with Python code execution
4. StrategyAdvisorAgent - Strategic synthesis with extended reasoning
5. ReportGeneratorAgent - HTML executive report generation
6. InfographicGeneratorAgent - Visual infographic generation

The pipeline analyzes a target location for a specific business type and
produces comprehensive location intelligence including recommendations,
an HTML report, and an infographic.

Usage:
    Run with: adk web retail_ai_location_strategy_adk

    The agent expects initial state variables:
    - target_location: The geographic area to analyze (e.g., "Bangalore, India")
    - business_type: Type of business to open (e.g., "coffee shop")

"""

from google.adk.agents import SequentialAgent
from google.adk.agents.llm_agent import Agent
from google.adk.tools.agent_tool import AgentTool


from .sub_agents.intake_agent.agent import intake_agent
from .sub_agents.market_research.agent import market_research_agent
from .sub_agents.competitor_analysis.agent import competitor_analysis_agent
from .sub_agents.gap_analysis.agent import gap_analysis_agent
from .sub_agents.strategy_advisor.agent import strategy_advisor_agent
from .sub_agents.report_generator.agent import report_generation_pipeline
from .sub_agents.infographic_generator.agent import infographic_generator_agent

from .config import config
#from .trace import instrument_adk_with_phoenix
from .prompt import retail_location_strategy_instruction

# Run Phoenix UI: phoenix serve
#_ = instrument_adk_with_phoenix()

# location_strategy_pipeline
location_strategy_pipeline = SequentialAgent(
    name="LocationStrategyPipeline",
    description="""Comprehensive retail location strategy analysis pipeline.

This agent analyzes a target location for a specific business type and produces:
1. Market research findings from live web data
2. Competitor mapping from Google Maps Places API
3. Quantitative gap analysis with zone rankings
4. Strategic recommendations with structured JSON output
5. Professional HTML executive report
6. Visual infographic summary

To use, get the following details:
- target_location: {target_location}
- business_type: {business_type}

The analysis runs automatically through all stages and produces artifacts
including JSON report, HTML report, and infographic image.
""",
    sub_agents=[
        market_research_agent,      # Part 1: Market research with search
        competitor_analysis_agent,   # Part 2A: Competitor mapping with Maps
        gap_analysis_agent,         # Part 2B: Gap analysis with code exec
        strategy_advisor_agent,     # Part 3: Strategy synthesis
        report_generation_pipeline,     # Part 4: HTML report generation
        #infographic_generator_agent,  # Part 5: Infographic generation
    ],
)

# Root agent orchestrating the complete location strategy pipeline
root_agent = Agent(
    model=config.FAST_MODEL,
    name="retail_location_strategy",
    description='A strategic partner for retail businesses, guiding them to optimal physical locations that foster growth and profitability.',
    instruction=retail_location_strategy_instruction(),
    sub_agents=[location_strategy_pipeline],
    tools = [AgentTool(intake_agent)], # Part 0: Parse user request
)
