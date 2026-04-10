from fastapi import Request, status
from fastapi.security.utils import get_authorization_scheme_param
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from backend.auth import auth
from backend.schemas import CustomHTTPException


# https://fastapi.tiangolo.com/reference/security/#fastapi.security.HTTPBearer
def verify_jwt(token: str) -> bool:
    return True if auth.decode_jwt_exp(token) else False


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = False):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials | None = await super(
            JWTBearer, self
        ).__call__(request)
        
        if credentials:
            if not credentials.scheme == 'Bearer':
                raise CustomHTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail='Esquema de autenticação inválido.',
                )
            if not verify_jwt(credentials.credentials):
                raise CustomHTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail='Token inválido ou expirado.',
                )
            return credentials
        
        # Se auto_error for True, o super() já teria levantado exceção.
        # Se chegamos aqui sem credentials e sem exceção, é porque auto_error é False.
        return None
