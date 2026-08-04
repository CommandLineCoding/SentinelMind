
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Central application configuration managed via environment variables and .env file.
    """

    # Server Settings
    PROJECT_NAME: str = Field(default="Sentil Mind", description="Application name")
    ENV: str = Field(default="development", description="Environment stage: development, testing, or production")
    DEBUG: bool = Field(default=True, description="Enable debug mode")
    HOST: str = Field(default="0.0.0.0", description="Backend server host")
    PORT: int = Field(default=8000, description="Backend server port")

    # CORS Configuration
    CORS_ORIGINS: list[str] = Field(
        default=["http://localhost:5173", "http://localhost:3000"],
        description="Allowed CORS origin URLs for frontend access",
    )

    # Gemini LLM Credentials
    GEMINI_API_KEY: str = Field(default="", description="Google Gemini API key for natural language query generation")
    GEMINI_MODEL: str = Field(default="gemini-1.5-pro", description="Gemini model version to use")

    # SIEM / Elasticsearch Settings
    ELASTICSEARCH_HOST: str = Field(default="http://localhost:9200", description="Elasticsearch cluster URL")
    ELASTICSEARCH_API_KEY: str = Field(default="", description="Base64 encoded API key for Elastic SIEM connection")
    ELASTICSEARCH_INDEX_PATTERN: str = Field(default="logs-*", description="Default log index pattern scope")
    ELASTICSEARCH_VERIFY_SSL: bool = Field(default=False, description="Verify SSL certs for local Elastic cluster")

    # Optional Wazuh SIEM Settings
    WAZUH_HOST: str = Field(default="https://localhost:55000", description="Wazuh API endpoint host")
    WAZUH_API_KEY: str = Field(default="", description="Wazuh REST API credentials")

    # Session / Context Settings
    SESSION_TTL_SECONDS: int = Field(default=3600, description="In-memory chat session expiration time")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",  # Ignore extra environment variables
        case_sensitive=True,
    )


# Instantiate singleton settings instance across the backend
settings = Settings()