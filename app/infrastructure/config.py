from pydantic_settings import BaseSettings, SettingsConfigDict
from decouple import config as cfg


class BaseConfig(BaseSettings):
    model_config = SettingsConfigDict(extra="ignore")

class AppConfig(BaseConfig):
    DB_CONN_STR: str = cfg("DB_CONN_STR", cast=str)


config = AppConfig()