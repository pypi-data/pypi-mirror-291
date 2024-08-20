from pydantic import BaseSettings


class Settings(BaseSettings):

    HOST: str
    IN_PORT: int
    OUT_PORT: int
    VECTORIZE_TOPIC: str

    @property
    def URL(self):
        return f'kafka://{self.HOST}:{self.IN_PORT}'

    class Config:
        case_sensitive = True
        env_prefix = "KF_"


settings = Settings()
