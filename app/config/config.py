
from pydantic_settings import BaseSettings
from pathlib import Path


class Settings(BaseSettings):
    url : str 
    attempts : int = 100
    max_concurrency_limit: int = 10


    class Config:
        env_file = str(Path(__file__).parents[2] /".env")
        env_file_encoding = "utf-8"

setting = Settings()
