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


class LogLevel(str, Enum):
    CRITICAL = 'critical'
    ERROR = 'error'
    WARNING = 'warning'
    INFO = 'info'
    DEBUG = 'debug'
    TRACE = 'trace'


class Settings(BaseSettings):
    host: IPvAnyAddress = Field(alias='HOST')
    port: int = Field(alias='PORT', minimum=1023, maximum=65535)
    pg_url: PostgresDsn = Field(alias='DB_URL')
    pg_user: str = Field(alias='DB_USER')
    pg_password: str = Field(alias='DB_PASSWORD')
    log_level: LogLevel = Field(alias='LOG_LEVEL')
    reload: bool = False

    @classmethod
    def load(cls) -> dict:
        pass


class Production(Settings):
    workers: int = Field(alias='WORKERS')
    model_config = SettingsConfigDict(
        env_file='.env.prod',
        env_file_encoding='utf-8')

    def load(self) -> dict:
        return dict(host=str(self.host), port=self.port, log_level=self.log_level, reload=self.reload,
                    workers=self.workers)


class Development(Settings):
    reload: bool = Field(alias='RELOAD')
    model_config = SettingsConfigDict(
        env_file='.env.dev',
        env_file_encoding='utf-8')

    def load(self) -> dict:
        return dict(host=str(self.host), port=self.port, log_level=self.log_level, reload=self.reload)
