import logging
import logging.config

from pydantic_settings import BaseSettings, SettingsConfigDict

logging.config.fileConfig('logging.ini')
logger = logging.getLogger('uvicorn')


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env', env_file_encoding='utf-8', extra='ignore'
    )

    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRES_MINUTES: int
