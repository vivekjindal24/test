from functools import lru_cache
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List

class Settings(BaseSettings):
    project_name: str = Field(default="research-platform")
    environment: str = Field(default="local")
    secret_key: str
    access_token_expire_minutes: int = 60
    refresh_token_expire_minutes: int = 43200
    database_url: str
    redis_url: str | None = None
    s3_endpoint: str
    s3_region: str = "us-east-1"
    s3_bucket: str
    s3_access_key: str
    s3_secret_key: str
    email_from: str
    smtp_host: str
    smtp_port: int = 25
    twilio_account_sid: str | None = None
    twilio_auth_token: str | None = None
    twilio_from_number: str | None = None
    calendar_organizer_email: str | None = None
    allowed_origins: str = ""
    otel_exporter_otlp_endpoint: str | None = None
    otel_service_name: str | None = None

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False
    )

@lru_cache
def get_settings() -> Settings:
    return Settings()
