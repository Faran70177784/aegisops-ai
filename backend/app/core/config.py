from pydantic import Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "AegisOps AI"
    app_version: str = "0.1.0"
    environment: str = "development"
    debug: bool = False

    api_v1_prefix: str = "/api/v1"

    database_url: str = "sqlite:///./aegisops.db"

    jwt_secret_key: str = "CHANGE_THIS_IN_DEVELOPMENT"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = Field(default=30, ge=1, le=1440)

    llm_provider: str = "ollama"
    llm_model: str = "qwen2.5:3b"

    log_level: str = "INFO"

    vector_db_provider: str = "qdrant"
    qdrant_url: str = "http://localhost:6333"
    qdrant_collection: str = "enterprise_knowledge"

    redis_url: str = "redis://localhost:6379/0"

    cors_origins: str = ""
    allowed_hosts: str = ""
    docs_enabled: bool = True

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    @property
    def cors_origin_list(self) -> list[str]:
        return [item.strip() for item in self.cors_origins.split(",") if item.strip()]

    @property
    def allowed_host_list(self) -> list[str]:
        return [item.strip() for item in self.allowed_hosts.split(",") if item.strip()]

    @model_validator(mode="after")
    def validate_production_security(self) -> "Settings":
        if self.environment.lower() == "production":
            if self.debug:
                raise ValueError("DEBUG must be false in production.")
            if len(self.jwt_secret_key) < 32 or self.jwt_secret_key == "CHANGE_THIS_IN_DEVELOPMENT":
                raise ValueError("JWT_SECRET_KEY must be a strong secret of at least 32 characters in production.")
            if self.database_url.startswith("sqlite"):
                raise ValueError("SQLite is not recommended for production; configure DATABASE_URL for PostgreSQL.")
        return self


settings = Settings()
