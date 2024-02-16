from fastapi import Request, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials, OAuth2PasswordBearer

from backend.auth import decode_jwt_exp, decode_jwt_sub
from backend.configs import get_session
from backend.schemas import TokenData, UserAuth
from backend.models import User

from sqlalchemy import select
from sqlalchemy.orm import Session

from jose.jwt import JWTError
from logging import Logger

from ..utils import get_logger

# https://fastapi.tiangolo.com/reference/security/#fastapi.security.HTTPBearer


def verify_jwt(token: str) -> bool:

    return True if decode_jwt_exp(token) else False


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Esquema de autenticação inválido.")
            if not verify_jwt(credentials.credentials):
                raise HTTPException(status_code=403, detail="Token inválido ou expirado.")
            return credentials
        else:
            raise HTTPException(status_code=403, detail="Código de autorização inválido.")


security = JWTBearer()


async def get_current_user(
    session: Session = Depends(get_session),
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> UserAuth:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Não foi possível validar credenciais.',
        headers={'WWW-Authenticate': 'Bearer'},
    )
    try:
        sub = decode_jwt_sub(credentials.credentials)
        if not sub:
            raise credentials_exception
        token_data = TokenData(subject=sub)
    except JWTError:
        raise credentials_exception

    user: User = session.scalar(
            select(User).where(User.email == token_data.subject)
        )
    # logger.debug(user.permission)
    if user is None:
        raise credentials_exception

    return UserAuth(id=user.id, email=user.email, permission=user.permission)
