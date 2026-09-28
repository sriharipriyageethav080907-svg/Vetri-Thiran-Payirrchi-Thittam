from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "PocketSmart AI"

    secret_key: str = "change-this-in-production"

    database_url: str = "sqlite:///./pocketsmart.db"

    gemini_api_key: str = ""

    gemini_model: str = "gemini-2.5-flash"

    access_token_expire_minutes: int = 1440

    max_image_bytes: int = 5 * 1024 * 1024

    allowed_image_types: str = (
        "image/jpeg,image/png,image/webp"
    )

    cookie_secure: bool = False

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore",
    )

    @property
    def allowed_image_type_set(self) -> set[str]:
        return {
            item.strip().lower()
            for item in self.allowed_image_types.split(",")
            if item.strip()
        }


@lru_cache
def get_settings() -> Settings:
    return Settings()
    