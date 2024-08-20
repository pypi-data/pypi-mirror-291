import os

from pydantic import BaseSettings


class Settings(BaseSettings):

    USER: str
    PASSWORD: str
    HOST: str
    IN_PORT: int
    NAME: str
    ECHO: bool
    POOL_SIZE: int
    OUT_PORT: int
    MAX_OVERFLOW: int

    @property
    def ASYNC_URI(self):
        return f"postgresql+asyncpg://{self.USER}:" \
               f"{self.PASSWORD}@{self.HOST}:{self.IN_PORT}/{self.NAME}"

    @property
    def SYNC_URI(self):
        return f"postgresql://{self.USER}:" \
               f"{self.PASSWORD}@{self.HOST}:{self.IN_PORT}/{self.NAME}"

    class Config:
        case_sensitive = True
        env_prefix = os.getenv("DB_PREFIX")


settings = Settings()
