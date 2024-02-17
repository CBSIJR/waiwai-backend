
from fastapi import status, APIRouter, Depends

from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

from backend.configs.database import get_async_session
from backend.repositories import Users
from backend.schemas import Message, Token, UserCreate, UserLogin

router = APIRouter(
    prefix="/auth",
    tags=["Autenticação"],
    # dependencies=[Depends(get_token_header)],
)


@router.post("/signup", status_code=status.HTTP_201_CREATED, response_model=Token, tags=["Autenticação"],
             responses={400: {'model': Message}})
async def signup(user: UserCreate, session: AsyncSession = Depends(get_async_session)):
    result = await Users(session).create(user)
    return result


# TODO: Delete account
# TODO: Change email
# TODO: Forgot password

@router.post("/signin", status_code=status.HTTP_200_OK, response_model=Token, tags=["Autenticação"],
             responses={400: {'model': Message}})
async def signin(user: UserLogin, session: AsyncSession = Depends(get_async_session)):
    result = await Users(session).create_jwt(user)
    return result
