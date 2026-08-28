from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Central app configuration, populated from environment variables / .env.
    Nothing here should be hardcoded secrets — see .env.example.
    """

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # --- App ---
    app_name: str = "SecOps Assistant"
    environment: str = "development"

    # --- Database ---
    database_url: str = "postgresql+asyncpg://secops:secops@db:5432/secops"

    # --- Auth ---
    jwt_secret_key: str = "change-me-in-.env-this-is-not-safe-for-prod"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 24  # 24h, fine for a demo project

    # --- CORS ---
    cors_origins: list[str] = ["http://localhost:5173", "http://localhost:3000"]


settings = Settings()
