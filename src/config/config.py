from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str
    # DEBUG: bool = False
    LOCAL_LLM_URL: str = "http://localhost:11434/api/generate"

    REDIS_URL: str 
    LLM_REQUESTS_LIMIT: int
    LLM_REQUESTS_TTL: int
    OLLAMA_MODEL: str
    
    # Говорим Pydantic читать из файла .env
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

# Создаем один экземпляр настроек, который будет использоваться везде
settings = Settings()