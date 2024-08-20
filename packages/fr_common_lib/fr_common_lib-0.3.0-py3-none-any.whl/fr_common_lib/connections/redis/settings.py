from pydantic import BaseSettings


class Settings(BaseSettings):

    HOST: str
    IN_PORT: int

    @property
    def URL(self):
        return f'redis://{self.HOST}:{self.IN_PORT}'

    class Config:
        case_sensitive = True
        env_prefix = 'RS_'


settings = Settings()
