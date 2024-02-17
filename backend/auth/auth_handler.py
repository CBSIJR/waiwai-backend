from fastapi import HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from backend.auth import auth

# https://fastapi.tiangolo.com/reference/security/#fastapi.security.HTTPBearer


def verify_jwt(token: str) -> bool:

    return True if auth.decode_jwt_exp(token) else False


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(
            JWTBearer, self
        ).__call__(request)
        if credentials:
            if not credentials.scheme == 'Bearer':
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN, detail='Esquema de autenticação inválido.'
                )
            if not verify_jwt(credentials.credentials):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN, detail='Token inválido ou expirado.'
                )
            return credentials
        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail='Código de autorização inválido.'
            )


security = JWTBearer()
