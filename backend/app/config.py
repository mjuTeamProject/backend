from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    APP_NAME: str = "Soulmatch"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    ENVIRONMENT: str = "development"
    
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    DATABASE_URL: str
    SYNC_DATABASE_URL: str = ""
    DB_ECHO: bool = False
    
    REDIS_URL: str = "redis://localhost:6379/0"
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: str = ""
    
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    MODEL_PATH: str = "./models"
    SKY_MODEL_PATH: str = "./models/sky3000.h5"
    EARTH_MODEL_PATH: str = "./models/earth3000.h5"
    CALENDAR_FILE_PATH: str = "./models/cal.csv"
    
    IMAGE_CACHE_DIR: str = "./cache/images"
    IMAGE_CACHE_TTL: int = 3600
    
    RANKING_CACHE_TTL: int = 300
    DAILY_RANKING_LIMIT: int = 100
    WEEKLY_RANKING_LIMIT: int = 100
    
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8080"]
    
    MAX_UPLOAD_SIZE: int = 5242880
    ALLOWED_IMAGE_TYPES: List[str] = ["image/jpeg", "image/png", "image/gif"]
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "allow"


settings = Settings()