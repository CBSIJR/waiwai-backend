from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.auth import Authorization, JWTBearer, get_current_user
from backend.configs import get_async_session
from backend.repositories import Words,Meanings
from backend.schemas import (
    BaseResponsePage,
    ErrorResponse,
    ParamsPageQuery,
    PermissionType,
    UserAuth,
    WordPublic,
    MeaningPublic,
)
router = APIRouter(
    prefix='/me',
    tags=['Meu'],
    responses={
        '401': {'model': ErrorResponse},
        '403': {'model': ErrorResponse}}

)

security = JWTBearer()

@router.get(
    '/words',
    status_code=status.HTTP_200_OK,
    response_model=BaseResponsePage[List[WordPublic]],
    dependencies=[
        Depends(security),
        Authorization([PermissionType.USER, PermissionType.ADMIN]),
    ]
)
async def me_words(
    params: ParamsPageQuery = Depends(),
    current_user: UserAuth = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
):
    words = await Words(session).get_list(params, current_user)
    total = await Words(session).count(params, current_user)
    return BaseResponsePage[WordPublic](data=words, total_items=total)


@router.get(
    '/meanings',
    status_code=status.HTTP_200_OK,
    response_model=BaseResponsePage[List[MeaningPublic]],
    dependencies=[
        Depends(security),
        Authorization([PermissionType.USER, PermissionType.ADMIN]),
    ]
)
async def me_meanings(
    params: ParamsPageQuery = Depends(),
    current_user: UserAuth = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
):
    meanings = await Meanings(session).get_list(params, current_user)
    total = await Meanings(session).count(params, current_user)
    return BaseResponsePage[MeaningPublic](data=meanings, total_items=total)


@router.get(
    '/attachments',
    status_code=status.HTTP_204_NO_CONTENT,
    # response_model=BaseResponsePage[List[MeaningPublic]],
    dependencies=[
        Depends(security),
        Authorization([PermissionType.USER, PermissionType.ADMIN]),
    ]
)
async def me_attachments(
    params: ParamsPageQuery = Depends(),
    current_user: UserAuth = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
):
    pass
    # meanings = await Meanings(session).get_list(params, current_user)
    # total = await Meanings(session).count(params, current_user)
    # return BaseResponsePage[MeaningPublic](data=meanings, total_items=total)
