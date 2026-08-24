from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "AegisOps AI"
    app_version: str = "0.1.0"
    environment: str = "development"
    debug: bool = True

    api_v1_prefix: str = "/api/v1"

    database_url: str = "sqlite:///./aegisops.db"

    jwt_secret_key: str = "CHANGE_THIS_IN_DEVELOPMENT"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    llm_provider: str = "ollama"
    llm_model: str = "qwen2.5:3b"

    log_level: str = "INFO"

    vector_db_provider: str = "qdrant"
    qdrant_url: str = "http://localhost:6333"
    qdrant_collection: str = "enterprise_knowledge"

    redis_url: str = "redis://localhost:6379/0"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


settings = Settings()