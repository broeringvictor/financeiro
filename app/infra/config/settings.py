from functools import lru_cache

from argon2 import PasswordHasher
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    # Config MAP
    ## DB
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = "financeiro"
    POSTGRES_USER: str = "admin"

    # Secrets MAP
    ## DB
    POSTGRES_PASSWORD: str = "financeiro"

    @property
    def database_url(self) -> str:
        return f"postgresql+psycopg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    argon2_time_cost: int = 2  # iterações
    argon2_memory_cost: int = 65536  # (64 MB)
    argon2_parallelism: int = 2  # threads

    @property
    def password_hasher(self) -> PasswordHasher:
        return PasswordHasher(
            time_cost=self.argon2_time_cost,
            memory_cost=self.argon2_memory_cost,
            parallelism=self.argon2_parallelism,
        )


@lru_cache
def get_settings() -> Settings:
    return Settings()
