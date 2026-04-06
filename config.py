from pydantic_settings import BaseSettings
from pydantic import ConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str
    
    POSTGRES_USER: str = "libuser"
    POSTGRES_PASSWORD: str = "libpass"
    POSTGRES_DB: str = "libdb"
    POSTGRES_HOST: str = "db"
    POSTGRES_PORT: str = "5432"
    
    model_config = ConfigDict(env_file=".env", extra="ignore")

settings = Settings()