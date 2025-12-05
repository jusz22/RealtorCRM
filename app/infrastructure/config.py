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
    GMAIL_GENERATED_PASSWORD: str = cfg("GMAIL_GENERATED_PASSWORD", cast=str)
    GMAIL_ADDRESS: str = cfg("GMAIL_ADDRESS", cast=str)
    UPLOAD_DIR: str = cfg("UPLOAD_DIR", default="uploads", cast=str)
    MAX_UPLOAD_SIZE_MB: int = cfg("MAX_UPLOAD_SIZE_MB", default=2, cast=int)


config = AppConfig()