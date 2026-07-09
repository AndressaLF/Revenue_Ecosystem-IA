"""Centralized settings loaded from environment / .env file."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Secrets and config — never log SecretStr values."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # --- Obrigatório para automação com IA (produce, auto-select desempate) ---
    gemini_api_key: SecretStr | None = Field(default=None, alias="GEMINI_API_KEY")

    # --- Reddit (opcional: ingest público funciona sem OAuth) ---
    reddit_client_id: SecretStr | None = Field(default=None, alias="REDDIT_CLIENT_ID")
    reddit_client_secret: SecretStr | None = Field(default=None, alias="REDDIT_CLIENT_SECRET")

    # --- Afiliados (IDs públicos em hoplinks — não são secretos críticos) ---
    amazon_associate_tag: str = Field(default="", alias="AMAZON_ASSOCIATE_TAG")
    digistore24_affiliate_id: str = Field(default="", alias="DIGISTORE24_AFFILIATE_ID")
    clickbank_nickname: str = Field(default="", alias="CLICKBANK_NICKNAME")

    # --- Digistore24 API (opcional — scout automático de catálogo) ---
    digistore24_api_key: SecretStr | None = Field(default=None, alias="DIGISTORE24_API_KEY")

    # --- ClickBank API (opcional — estatísticas / notificações) ---
    clickbank_api_key: SecretStr | None = Field(default=None, alias="CLICKBANK_API_KEY")

    # --- Publicação semi-automática (opcional) ---
    medium_integration_token: SecretStr | None = Field(
        default=None, alias="MEDIUM_INTEGRATION_TOKEN"
    )
    pinterest_access_token: SecretStr | None = Field(
        default=None, alias="PINTEREST_ACCESS_TOKEN"
    )

    # --- Pesquisa SaaS (opcional) ---
    producthunt_token: SecretStr | None = Field(default=None, alias="PRODUCTHUNT_TOKEN")

    # --- Ingest locale ---
    ingest_locale: str = Field(default="en-US", alias="INGEST_LOCALE")
    ingest_geo: str = Field(default="US", alias="INGEST_GEO")
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")

    # --- Paths ---
    storage_dir: Path = Field(default=Path("storage"))

    def gemini_configured(self) -> bool:
        return self.gemini_api_key is not None and bool(
            self.gemini_api_key.get_secret_value().strip()
        )

    def reddit_oauth_configured(self) -> bool:
        return (
            self.reddit_client_id is not None
            and self.reddit_client_secret is not None
            and bool(self.reddit_client_id.get_secret_value().strip())
            and bool(self.reddit_client_secret.get_secret_value().strip())
        )


@lru_cache
def get_settings() -> Settings:
    return Settings()
