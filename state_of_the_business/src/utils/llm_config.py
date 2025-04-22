import os
from typing import Optional
from dotenv import load_dotenv
from crewai import LLM


class LLMConfig:
    """Configuration class for managing LLM settings and interactions."""

    _instance: Optional["LLMConfig"] = None
    _llm: Optional[LLM] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LLMConfig, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        """Initialize the LLM configuration."""
        if self._llm is None:
            load_dotenv()  # Load environment variables

            base_url = os.getenv("LAMBDA_API_BASE")
            api_key = os.getenv("LAMBDA_API_KEY")
            model = os.getenv("LAMBDA_MODEL")

            if not base_url or not api_key:
                raise ValueError(
                    "Missing required environment variables. "
                    "Please set LAMBDA_API_BASE and LAMBDA_API_KEY."
                )

            self._llm = LLM(
                base_url=base_url, model=model, api_key=api_key
            )

    @property
    def llm(self) -> LLM:
        """Get the configured LLM instance."""
        if self._llm is None:
            raise RuntimeError("LLM not initialized. Please call __init__ first.")
        return self._llm

    def get_llm(self) -> LLM:
        """Get the LLM instance (alternative to property)."""
        return self.llm


# llm = LLM(
#     base_url=os.getenv("LAMBDA_API_BASE"),
#     model="openai/llama-4-maverick",
#     api_key=os.getenv("LAMBDA_API_KEY"),
# )
