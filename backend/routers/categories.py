from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.configs.database import get_async_session
from backend.repositories import Users
from backend.schemas import Message, Token, UserCreate, UserLogin

router = APIRouter(
    prefix='/categories',
    tags=['Categorias'],
    # dependencies=[Depends(get_token_header)],
)



