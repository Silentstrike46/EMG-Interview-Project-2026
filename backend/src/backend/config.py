from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # No default: a missing DATABASE_URL must fail at startup rather than
    # silently connect somewhere unexpected.
    database_url: str


settings = Settings()
