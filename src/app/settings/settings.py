from pydantic_settings import BaseSettings
from typing import Literal


class Settings(BaseSettings):

    PROJECT_NAME: str
    PROJECT_VERSION: str
    PROJECT_ENVIRONMENT: Literal["local", "qa", "prod"]

    # FastAPI configurations
    SERVER_HOST:str
    SERVER_PORT: int 
    SERVER_RELOAD: bool 


    # Graylog logging configuration
    GRAYLOG_HOST: str
    GRAYLOG_PORT: int

    # Google OAuth configurations
    CLIENT_ID :str
    CLIENT_SECRET: str
    REDIRECT_URI:str

  
settings = Settings()
