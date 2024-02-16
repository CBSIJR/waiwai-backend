import time

from jose import jwt
from jose.jwt import ExpiredSignatureError, JWTError


from backend.configs import Settings
from backend.schemas import Token
from backend.utils import create_refresh_token, create_access_token

from passlib.context import CryptContext


settings = Settings()
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def sign_jwt(user_id: str) -> Token:
    access_token = create_access_token(user_id, settings)
    refresh_token = create_refresh_token(user_id, settings)

    return Token(access_token=access_token, refresh_token=refresh_token, token_type="Bearer")


def decode_jwt_exp(token: str) -> dict | None:
    try:
        decoded_token = jwt.decode(token, settings.jwt_secret_key_access_token, algorithms=[settings.jwt_algorithm])
        return decoded_token if decoded_token["exp"] >= time.time() else None
    except JWTError:
        return None


def decode_jwt_sub(token: str) -> dict | None:
    payload = jwt.decode(token, settings.jwt_secret_key_access_token, algorithms=[settings.jwt_algorithm])
    return payload["sub"]


def get_password_hash(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)



