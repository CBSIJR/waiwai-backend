from datetime import datetime, timedelta
from typing import Union, Any
from jose import jwt
from pydantic_settings import BaseSettings
import logging


logger = logging.getLogger("uvicorn.error")
logger.setLevel(logging.DEBUG)
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s %(name)s - %(message)s",
    handlers=[logging.StreamHandler()],
)
logging.getLogger('passlib').setLevel(logging.ERROR)


def get_logger(logger_name="uvicorn.error") -> logging.Logger:
    return logging.getLogger(logger_name)


def create_access_token(subject: Union[str, Any], settings: BaseSettings, expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=settings.jwt_expiration_access_token)

    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.jwt_secret_key_access_token, settings.jwt_algorithm)
    return encoded_jwt


def create_refresh_token(subject: Union[str, Any], settings: BaseSettings, expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=settings.jwt_expiration_refresh_token)

    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.jwt_secret_key_refresh_token, settings.jwt_algorithm)
    return encoded_jwt
