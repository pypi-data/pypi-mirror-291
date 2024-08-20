from pydantic import BaseSettings


class Settings(BaseSettings):

    HOST: str
    PORT: int
    EMAIL: str
    PASSWORD: str

    class Config:
        case_sensitive = True
        env_prefix = 'SM_'


settings = Settings()
