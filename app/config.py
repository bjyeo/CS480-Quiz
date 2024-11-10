from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    SUPABASE_URL: str
    SUPABASE_KEY: str
    SUPABASE_DB_PASSWORD: str
    OPENAI_API_KEY: str
    
    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
