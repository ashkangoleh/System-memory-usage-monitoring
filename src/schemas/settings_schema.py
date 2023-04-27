from pydantic import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    DROP_TABLE: bool
    DATABASE_ECHO: bool
    API_TOKEN: str
    CELERY_BROKER_URL: str
    CELERY_RESULT_BACKEND: str
    CELERY_TIMEZONE: str
    LOCAL_EXECUTOR:bool
    
    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


settings = Settings()
