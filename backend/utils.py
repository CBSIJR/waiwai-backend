import logging
import uuid
from datetime import datetime, timedelta

from jose import jwt
from pydantic_settings import BaseSettings

from backend.schemas import Subject

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s %(name)s - %(message)s',
    handlers=[logging.StreamHandler()],
)
logging.getLogger('passlib').setLevel(logging.ERROR)


iss = 'waiwaitapota-api'


def get_logger(logger_name='uvicorn.error') -> logging.Logger:
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)
    return logger


def generate_jti():
    return str(uuid.uuid4())


def create_access_token(
    subject: Subject, settings: BaseSettings, expires_delta: timedelta = None
) -> str:
    now = datetime.utcnow()

    if expires_delta is not None:
        expires_delta = now + expires_delta
    else:
        expires_delta = now + timedelta(
            minutes=settings.jwt_expiration_access_token
        )
    payload = {
        'iss': iss,
        'sub': str(subject.email),
        'iat': now,
        'exp': expires_delta,
        'jti': generate_jti(),
        'data': subject.model_dump(),
    }
    encoded_jwt = jwt.encode(
        payload, settings.jwt_secret_key_access_token, settings.jwt_algorithm
    )
    return encoded_jwt


def create_refresh_token(
    subject: Subject, settings: BaseSettings, expires_delta: timedelta = None
) -> str:
    now = datetime.utcnow()

    if expires_delta is not None:
        expires_delta = now + expires_delta
    else:
        expires_delta = now + timedelta(
            minutes=settings.jwt_expiration_refresh_token
        )
    payload = {
        'iss': iss,
        'sub': str(subject.email),
        'iat': now,
        'exp': expires_delta,
        'jti': generate_jti(),
        'data': subject.model_dump(),
    }
    encoded_jwt = jwt.encode(
        payload, settings.jwt_secret_key_refresh_token, settings.jwt_algorithm
    )
    return encoded_jwt
