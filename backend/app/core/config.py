from pydantic_settings import BaseSettings
from typing import Optional
from functools import lru_cache


class Settings(BaseSettings):
    """Application configuration settings"""
    
    # App Settings
    APP_NAME: str = "DataOps Copilot"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # API Settings
    API_V1_PREFIX: str = "/api/v1"
    
    # CORS Settings
    ALLOWED_ORIGINS: list = [
        "http://localhost:3000",
        "http://localhost:3001",
        "https://www.dataopscopilot.com",
        "https://dataops-copilot.vercel.app"
    ]
    
    # Database
    DATABASE_URL: str = "postgresql://dataops_postgres_user:2h41a5HgDWJECmnWvUv0ya2K4N0XyN7Q@dpg-d4hlsvkhg0os738heq90-a/dataops_postgres"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # LLM API Keys
    ANTHROPIC_API_KEY: Optional[str] = None
    OPENAI_API_KEY: Optional[str] = None
    GOOGLE_API_KEY: Optional[str] = None
    AZURE_API_KEY: Optional[str] = None
    AZURE_API_BASE: Optional[str] = None
    AZURE_API_VERSION: str = "2024-02-15-preview"
    
    # Model Configurations
    DEFAULT_MODEL: str = "claude-sonnet-4-5-20250929"  # Claude Sonnet 4.5
    FALLBACK_MODEL: str = "gpt-4o-mini"  # GPT-5 mini (latest!)
    VISION_MODEL: str = "gemini-1.5-pro"  # Gemini 2.0 Flash (newest!)
    
    # LiteLLM Settings
    LITELLM_DROP_PARAMS: bool = True
    LITELLM_MAX_RETRIES: int = 3
    LITELLM_TIMEOUT: int = 300
    
    # File Upload Settings
    MAX_UPLOAD_SIZE: int = 100 * 1024 * 1024  # 100MB
    ALLOWED_EXTENSIONS: set = {".csv", ".xlsx", ".xls", ".json", ".pdf", ".png", ".jpg", ".jpeg"}
    UPLOAD_DIR: str = "/tmp/uploads"
    
    # DuckDB Settings
    DUCKDB_PATH: str = ":memory:"  # In-memory for now
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"  # Allow extra fields in .env file


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()


settings = get_settings()