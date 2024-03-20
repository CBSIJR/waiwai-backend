from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.auth import Authorization, JWTBearer, get_current_user
from backend.configs import get_async_session
from backend.repositories import Meanings
from backend.schemas import (
    MeaningCreate,
    MeaningPublic,
    Message,
    ParamsMeaning,
    PermissionType,
    UserAuth,
)

router = APIRouter(
    prefix='/words/{word_id}/meanings',
    tags=['Palavras Significados'],
)
security = JWTBearer()


@router.get(
    '/', status_code=status.HTTP_200_OK, response_model=list[MeaningPublic]
)
async def list_meanings(
    word_id: int,
    params: ParamsMeaning = Depends(),
    session: AsyncSession = Depends(get_async_session),
):
    meanings = await Meanings(session).get_list_by_word_id(word_id, params)
    return meanings


@router.post(
    '/',
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[
        Depends(security),
        Authorization([PermissionType.ADMIN, PermissionType.USER]),
    ],
    responses={'403': {'model': Message}, '409': {'model': Message}},
)
async def create_meaning(
    word_id: int,
    meaning: MeaningCreate,
    current_user: UserAuth = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
) -> None:
    await Meanings(session).create(word_id, meaning, current_user)
