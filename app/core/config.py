from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_env: str
    database_url: str
    database_url_sync: str
    redis_url: str
    ollama_base_url: str
    ollama_model: str
    osrm_base_url: str

    class Config:
        env_file = ".env"

settings = Settings()