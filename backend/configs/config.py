from enum import Enum

from pydantic import Field, IPvAnyAddress, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

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
    # https://github.com/pydantic/pydantic/issues/8061
    db_url: PostgresDsn = Field(alias='DB_URL')
    jwt_secret_key_access_token: str = Field(
        alias='JWT_SECRET_KEY_ACCESS_TOKEN'
    )
    jwt_secret_key_refresh_token: str = Field(
        alias='JWT_SECRET_KEY_REFRESH_TOKEN'
    )
    jwt_expiration_access_token: int = Field(
        alias='JWT_EXPIRATION_ACCESS_TOKEN', default=30
    )  # 30 minutos
    jwt_expiration_refresh_token: int = Field(
        alias='JWT_EXPIRATION_REFRESH_TOKEN', default=60 * 24 * 7
    )  # 7 dias
    jwt_algorithm: str = Field(alias='JWT_ALGORITHM', default='HS256')
    model_config = SettingsConfigDict(
        env_file=('.env.prod', '.env.dev', '.env'), env_file_encoding='utf-8'
    )
    static_path: str = Field(alias='STATIC_PATH', default='backend/static')

    def __init__(self) -> None:
        super().__init__()
        if self.environment.DEVELOPMENT:
            self.workers: int = 1

    def deployment(self) -> dict:
        return dict(
            host=str(self.host),
            port=self.port,
            log_level=self.log_level,
            reload=self.reload,
            workers=self.workers,
        )
