from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="QME_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "Qme"
    env: str = "development"
    # Optional LLM hook for future CV rewriting
    llm_provider: str | None = None


settings = Settings()
