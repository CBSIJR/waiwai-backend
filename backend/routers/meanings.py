from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from backend.auth import Authorization, JWTBearer, get_current_user
from backend.configs import get_async_session
from backend.repositories import Meanings
from backend.schemas import (
    MeaningExport,
    UserAuth,
    MeaningPublic,
    MeaningUpdate,
    Message,
    PermissionType,
)

router = APIRouter(
    prefix='/meanings',
    tags=['Significados'],
)
security = JWTBearer()


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
        Authorization([PermissionType.USER, PermissionType.ADMIN]),
    ],
    responses={
        '403': {'model': Message},
        '404': {'model': Message},
        '409': {'model': Message},
    },
)
async def delete_meaning(
    meaning_id: int,
    current_user: UserAuth = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
):
    await Meanings(session).delete_by_id(meaning_id, current_user)


@router.get(
    '/export/all',
    status_code=status.HTTP_200_OK,
    responses={'404': {'model': Message}},
    response_model=List[MeaningExport],
)
async def get_meaning(
    session: AsyncSession = Depends(get_async_session)
):
    meanings = await Meanings(session).all()
    return meanings