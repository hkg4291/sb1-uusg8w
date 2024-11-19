from typing import Optional
from pydantic_settings import BaseSettings
from enum import Enum

class DatabaseType(str, Enum):
    MONGODB = "mongodb"
    IN_MEMORY = "memory"
    SQL = "sql"

class Settings(BaseSettings):
    # API Settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Zoo Management API"
    
    # Database Settings
    DATABASE_TYPE: DatabaseType = DatabaseType.MONGODB
    MONGODB_URL: str = "mongodb://localhost:27017"
    DATABASE_NAME: str = "zoo_management"
    
    # Redis Settings
    REDIS_URL: str = "redis://localhost:6379"
    CACHE_TIMEOUT: int = 3600  # 1 hour
    
    # Elasticsearch Settings
    ELASTICSEARCH_URL: str = "http://localhost:9200"
    ELASTICSEARCH_INDEX_PREFIX: str = "zoo"
    
    # Nginx Settings
    NGINX_WORKER_PROCESSES: int = 4
    NGINX_WORKER_CONNECTIONS: int = 1024
    NGINX_KEEPALIVE_TIMEOUT: int = 65
    
    # Encryption Settings
    ENCRYPTION_KEY: str = "your-secret-key"  # Change in production
    
    # Performance Settings
    PAGE_SIZE: int = 100
    MAX_CONNECTIONS: int = 100
    
    class Config:
        case_sensitive = True

settings = Settings()