from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")
    database_url: str = "sqlite:///./cyberlearn.db"
    jwt_secret: str = "development-only-change-this-secret"
    access_token_minutes: int = 20
    frontend_origins: str = "http://localhost:5173"
    api_allowed_hosts: str = "localhost,127.0.0.1"
    environment: str = "development"
    allow_dev_email_links: bool = False

    @model_validator(mode="after")
    def validate_production_secret(self):
        if self.environment == "production" and len(self.jwt_secret) < 32:
            raise ValueError("JWT_SECRET must be at least 32 characters in production")
        return self

    @property
    def cors_origins(self) -> list[str]:
        return [origin.strip() for origin in self.frontend_origins.split(",") if origin.strip()]

    @property
    def allowed_hosts(self) -> list[str]:
        return [host.strip() for host in self.api_allowed_hosts.split(",") if host.strip()]


settings = Settings()
