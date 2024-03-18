from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.auth import Authorization, JWTBearer, get_current_user
from backend.configs import get_async_session
from backend.repositories import Words
from backend.schemas import (
    WordExport,
    Message,
    Params,
    PermissionType,
    UserAuth,
    WordCreate,
    WordPublic,
    WordUpdate,
)
from typing import List
router = APIRouter(
    prefix='/words',
    tags=['Palavras'],
)
security = JWTBearer()


@router.get(
    '/', status_code=status.HTTP_200_OK, response_model=List[WordPublic]
)
async def list_words(
    params: Params = Depends(),
    session: AsyncSession = Depends(get_async_session),
):
    words = await Words(session).get_list(params)
    return words


@router.get(
    '/{word_id}',
    status_code=status.HTTP_200_OK,
    responses={'404': {'model': Message}},
    response_model=WordPublic,
)
async def get_word(
    word_id: int, session: AsyncSession = Depends(get_async_session)
):
    word = await Words(session).get_by_id(word_id)

    return word


@router.post(
    '/',
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[
        Depends(security),
        Authorization([PermissionType.USER, PermissionType.ADMIN]),
    ],
    responses={'403': {'model': Message}, '409': {'model': Message}},
)
async def create_word(
    word: WordCreate,
    current_user: UserAuth = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
) -> None:
    await Words(session).create(word, current_user)


@router.put(
    '/{word_id}',
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
async def update_word(
    word_id: int,
    word: WordUpdate,
    current_user: UserAuth = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
):
    await Words(session).update_by_id(word_id, word, current_user)


@router.delete(
    '/{word_id}',
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
async def delete_word(
    word_id: int,
    current_user: UserAuth = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
):
    await Words(session).delete_by_id(word_id, current_user)


@router.get(
    '/export/all',
    status_code=status.HTTP_200_OK,
    response_model=List[WordExport],
)
async def get_export(
    session: AsyncSession = Depends(get_async_session)
):
    words = await Words(session).all()
    return words
