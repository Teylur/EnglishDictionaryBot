from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    BOT_TOKEN: str
    BACKEND_URL: str
    # Говорим Pydantic читать из файла .env
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

# Создаем один экземпляр настроек, который будет использоваться везде
settings = Settings()