from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.configs import get_async_session
from backend.repositories import Users
from backend.schemas import (
    UserExport
)
from typing import List
router = APIRouter(
    prefix='/users',
    tags=['Usuários'],
)


@router.get(
    '/export/all',
    status_code=status.HTTP_200_OK,
    response_model=List[UserExport],
)
async def get_export(
    session: AsyncSession = Depends(get_async_session)
):
    users = await Users(session).all()
    return users
