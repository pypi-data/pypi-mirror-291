import os

from pydantic import BaseSettings


class Settings(BaseSettings):

    SERVICE_NAME: str
    HOST: str
    IN_PORT: int

    class Config:
        case_sensitive = True
        env_prefix = os.getenv('KF_CLIENT_PREFIX')
        env_file = os.path.expanduser("~/.env")


settings = Settings()
