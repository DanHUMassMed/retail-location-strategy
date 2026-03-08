
from dataclasses import dataclass
from google.adk.models.lite_llm import LiteLlm

@dataclass
class AgentConfiguration:
    """Configuration for agents models and parameters."""

    BASE_MODEL = LiteLlm(model="openai/gpt-oss:20b",
                    api_base="http://localhost:11434/v1", 
                    api_key="no_ollama_key_needed")

    CODE_EXEC_MODEL = LiteLlm(model="openai/qwen3-coder:30b",
                    api_base="http://localhost:11434/v1", 
                    api_key="no_ollama_key_needed")

    MULTI_MODAL_MODEL = LiteLlm(model="openai/qwen3.5:35b",
                    api_base="http://localhost:11434/v1", 
                    api_key="no_ollama_key_needed")

    FAST_MODEL= BASE_MODEL
    
    max_search_results: int = 10


config = AgentConfiguration()
