from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import PostgresDsn, field_validator
import os


class Settings(BaseSettings):
    PROJECT_NAME: str = "Payment Gateway"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str = "payment_gateway"
    DATABASE_URL: Optional[str] = None
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    @field_validator("SQLALCHEMY_DATABASE_URI", mode='before')
    @classmethod
    def assemble_db_connection(cls, v: Optional[str], info) -> any:
        if isinstance(v, str):
            return v
        
        # First check if we have a DATABASE_URL environment variable
        database_url = os.getenv("DATABASE_URL")
        if database_url:
            return database_url
            
        # If not, build it from components
        return PostgresDsn.build(
            scheme="postgresql",
            username=info.data.get("POSTGRES_USER"),
            password=info.data.get("POSTGRES_PASSWORD"),
            host=info.data.get("POSTGRES_SERVER"),
            path=f"/{info.data.get('POSTGRES_DB') or ''}",
        )

    BLOCKCYPHER_TOKEN: str
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings() 