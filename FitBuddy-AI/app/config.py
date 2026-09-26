from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "FitBuddy"
    debug: bool = False
    database_url: str = "sqlite:///./fitbuddy.db"
    gemini_api_key: str | None = None
    gemini_workout_model: str = "gemini-2.5-pro"
    gemini_tip_model: str = "gemini-2.5-flash"
    admin_token: str = "fitbuddy-admin"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


def get_settings() -> Settings:
    return Settings()
