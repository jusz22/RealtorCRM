from pydantic_settings import BaseSettings, SettingsConfigDict
from decouple import config as cfg


class BaseConfig(BaseSettings):
    model_config = SettingsConfigDict(extra="ignore")

class AppConfig(BaseConfig):
    DB_CONN_STR: str = cfg("DB_CONN_STR", cast=str)
    ALGORITHM: str = cfg("ALGORITHM", cast=str)
    SECRET_KEY: str = cfg("SECRET_KEY", cast=str)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = cfg("ACCESS_TOKEN_EXPIRE_MINUTES", cast=int)
    API_STR: str = cfg("API_STR", cast=str)


config = AppConfig()