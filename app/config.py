from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = (
        "postgresql+asyncpg://tournament_user:tournament_pass@localhost:5432/tournament_db"
    )
    debug: bool = False

    class Config:
        env_file = ".env"


settings = Settings()
