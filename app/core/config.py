"""
App Configuration Service
"""
import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    """Application configuration loaded from environment variables."""

    def __init__(self):
        # LLM CONFIGURATION
        self.groq_api_key = os.getenv("GROQ_API_KEY")
        self.llm_model = os.getenv(
                    "LLM_MODEL",
                    "openai/gpt-oss-120b",
                )

        # DATABASE CONFIGURATION - PostgreSQL
        self.db_host = os.getenv("DB_HOST", "localhost")
        self.db_port = int(os.getenv("DB_PORT", "5432"))
        self.db_name = os.getenv("DB_NAME", "ragdb")
        self.db_user = os.getenv("DB_USER", "raguser")
        self.db_password = os.getenv("DB_PASSWORD")
        # EMBEDDING CONFIGURATION
        self.embedding_model = os.getenv(
            "EMBEDDING_MODEL",
            "sentence-transformers/all-MiniLM-L6-v2",
        )

        # LLM GENERATION CONFIGURATION
        self.llm_temperature = float(os.getenv("LLM_TEMPERATURE", "0"))
        self.llm_max_completion_tokens = int(
            os.getenv("LLM_MAX_COMPLETION_TOKENS", "8192")
        )
        self.llm_top_p = float(os.getenv("LLM_TOP_P", "1"))
        self.llm_reasoning_effort = os.getenv("LLM_REASONING_EFFORT", "medium")
        self.llm_stream = os.getenv("LLM_STREAM", "false").lower() == "true"

settings = Settings()
