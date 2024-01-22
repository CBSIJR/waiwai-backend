from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import (
    PostgresDsn,
    IPvAnyAddress,
    Field)
from enum import Enum

"""
Objetos para instanciar tipos de arquivos de configurações 
Leia mais: https://www.uvicorn.org/settings/
TODO: Optional env
"""


class Environment(str, Enum):
    PRODUCTION = 'prod'
    DEVELOPMENT = 'dev'


class LogLevel(str, Enum):
    CRITICAL = 'critical'
    ERROR = 'error'
    WARNING = 'warning'
    INFO = 'info'
    DEBUG = 'debug'
    TRACE = 'trace'


class Settings(BaseSettings):
    environment: Environment = Field(alias='ENVIRONMENT')
    host: IPvAnyAddress = Field(alias='HOST', default='127.0.0.1')
    port: int = Field(alias='PORT', minimum=1023, maximum=65535)
    log_level: LogLevel = Field(alias='LOG_LEVEL', default=LogLevel.INFO)
    reload: bool = Field(alias='RELOAD', default=False)
    workers: int = Field(alias='WORKERS', default=1)
    pg_url: PostgresDsn = Field(alias='DB_URL')
    pg_user: str = Field(alias='DB_USER')
    pg_password: str = Field(alias='DB_PASSWORD')
    model_config = SettingsConfigDict(
        env_file=('.env.prod', '.env.dev', '.env'),
        env_file_encoding='utf-8')

    def __init__(self) -> None:
        super().__init__()
        if self.environment.DEVELOPMENT:
            self.workers: int = 1

    def deployment(self) -> dict:
        return dict(host=str(self.host), port=self.port, log_level=self.log_level, reload=self.reload,
                    workers=self.workers)
