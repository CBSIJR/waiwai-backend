from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.auth import Authorization, security
from backend.configs import get_async_session
from backend.repositories import Meanings
from backend.schemas import (
    MeaningPublic,
    MeaningUpdate,
    Message,
    PermissionType,
)

router = APIRouter(
    prefix='/meanings',
    tags=['Significados'],
)


@router.get(
    '/{meaning_id}',
    status_code=status.HTTP_200_OK,
    responses={'404': {'model': Message}},
    response_model=MeaningPublic,
)
async def get_meaning(
    meaning_id: int, session: AsyncSession = Depends(get_async_session)
):
    meaning = await Meanings(session).get_by_id(meaning_id)
    return meaning


@router.put(
    '/{meaning_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[
        Depends(security),
        Authorization([PermissionType.ADMIN]),
    ],
    responses={
        '403': {'model': Message},
        '404': {'model': Message},
        '409': {'model': Message},
    },
)
async def update_meaning(
    meaning_id: int,
    meaning: MeaningUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    await Meanings(session).update_by_id(meaning_id, meaning)


@router.delete(
    '/{meaning_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[
        Depends(security),
        Authorization([PermissionType.ADMIN]),
    ],
    responses={
        '403': {'model': Message},
        '404': {'model': Message},
        '409': {'model': Message},
    },
)
async def delete_meaning(
    meaning_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    await Meanings(session).delete_by_id(meaning_id)
