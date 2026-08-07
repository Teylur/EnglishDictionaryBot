from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str
    # ALLOWED_ORIGINS: list[str] = ["http://localhost:3000"]
    # DEBUG: bool = False
    BOT_TOKEN: str
    
    # Говорим Pydantic читать из файла .env
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

# Создаем один экземпляр настроек, который будет использоваться везде
settings = Settings()