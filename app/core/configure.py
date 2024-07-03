from typing import List
from pydantic import AnyHttpUrl
from decouple import config
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    API_V1_STR : str = '/api/v1'
    JWT_SECRET_KEY : str = config('JWT_SECRET_KEY', cast = str)
    JWT_REFRESH_SECRET_KEY : str = config('JWT_REFRESH_SECRET_KEY', cast = str)
    ALGORITHM : str = 'HS256'
    BACKEND_CORS_ORIGINS : List[AnyHttpUrl] = []
    ACCESS_TOKEN_EXPIRE_MINUTES : int = 30  # 30 minutes
    REFRESH_TOKEN_EXPIRE_MINUTES : int = 60 * 24 * 7 # 7 days
    PROJECT_NAME : str = 'TODOLIST'

    MONGO_CONNECTION_STRING : str = config('MONGO_CONNECTION_STRING', cast = str)

    class Config:
        case_sensitive = True 

settings = Settings()