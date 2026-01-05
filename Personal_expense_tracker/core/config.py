from pydantic import PostgresDsn, Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: PostgresDsn = Field(
        default="postgresql+asyncpg://finance:password@localhost/finance_db"
    )
    model_config = {
        "env_file": ".env",
        "extra": "ignore",
    }

settings = Settings()


