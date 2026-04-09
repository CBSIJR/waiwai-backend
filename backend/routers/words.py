from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
import json

from backend.auth import Authorization, JWTBearer, get_current_user
from backend.utils import get_logger
from backend.configs import get_async_session, async_session_maker
from backend.repositories import Words
from backend.schemas import (
    BaseResponse,
    BaseResponsePage,
    CreatedResponse,
    ErrorResponse,
    ParamsWordQuery,
    PermissionType,
    UserAuth,
    WordCreate,
    WordDetails,
    WordExport,
    WordPublic,
    WordReviewCreate,
    WordReviewPublic,
    WordUpdate,
    LetterStatistic,
)

router = APIRouter(
    prefix='/words',
    tags=['Palavras'],
)
security = JWTBearer()

@router.get(
    '/statistic',
    status_code=status.HTTP_200_OK,
    response_model=BaseResponse[List[LetterStatistic]],
)
async def get_word_statistic(
    session: AsyncSession = Depends(get_async_session),
):
    statistic = await Words(session).get_letter_statistic()
    return BaseResponse[List[LetterStatistic]](data=statistic)


@router.get(
    '/',
    status_code=status.HTTP_200_OK,
    response_model=BaseResponsePage[List[WordPublic]],
)
async def list_words(
    params: ParamsWordQuery = Depends(),
    session: AsyncSession = Depends(get_async_session),
):
    words = await Words(session).get_list(params)
    total = await Words(session).count(params)
    return BaseResponsePage[WordPublic](data=words, total_items=total)


@router.get(
    '/{word_id}',
    status_code=status.HTTP_200_OK,
    responses={'404': {'model': ErrorResponse}},
    response_model=BaseResponse[WordDetails],
)
async def get_word(
    word_id: int, session: AsyncSession = Depends(get_async_session)
):
    word = await Words(session).get_by_id(word_id)
    return BaseResponse[WordDetails](data=word)


@router.post(
    '/',
    status_code=status.HTTP_201_CREATED,
    dependencies=[
        Depends(security),
        Authorization([PermissionType.USER, PermissionType.ADMIN]),
    ],
    responses={
        '403': {'model': ErrorResponse},
        '409': {'model': ErrorResponse},
    },
    response_model=BaseResponse[CreatedResponse],
)
async def create_word(
    word: WordCreate,
    current_user: UserAuth = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
):
    result = await Words(session).create(word, current_user)

    return BaseResponse[CreatedResponse](data=CreatedResponse(id=result.id))


@router.put(
    '/{word_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[
        Depends(security),
        Authorization([PermissionType.USER, PermissionType.ADMIN]),
    ],
    responses={
        '403': {'model': ErrorResponse},
        '404': {'model': ErrorResponse},
        '409': {'model': ErrorResponse},
    },
)
async def update_word(
    word_id: int,
    word: WordUpdate,
    current_user: UserAuth = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
):
    await Words(session).update_by_id(word_id, word, current_user)

@router.post(
    '/{word_id}/reviews',
    status_code=status.HTTP_201_CREATED,
    dependencies=[
        Depends(security),
        Authorization([PermissionType.ADMIN]),
    ],
    responses={
        '403': {'model': ErrorResponse},
        '404': {'model': ErrorResponse},
    },
    response_model=BaseResponse[WordReviewPublic],
)
async def review_word(
    word_id: int,
    review: WordReviewCreate,
    current_user: UserAuth = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
):
    """
    Cria uma revisão de moderação para uma palavra.

    Apenas ADMINs têm acesso. A decisão do revisor (APPROVED, REJECTED,
    CHANGES_REQUESTED) é registrada no histórico e sincronizada imediatamente
    no status da palavra.
    """
    result = await Words(session).add_review(word_id, review, current_user)
    return BaseResponse[WordReviewPublic](data=result)


@router.delete(
    '/{word_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[
        Depends(security),
        Authorization([PermissionType.USER, PermissionType.ADMIN]),
    ],
    responses={
        '403': {'model': ErrorResponse},
        '404': {'model': ErrorResponse},
        '409': {'model': ErrorResponse},
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
)
async def get_export():
    async def generate_json():
        yield "["
        first = True
        async for word in Words.stream_all():
            if not first:
                yield ","
            first = False
            yield WordExport.model_validate(word).model_dump_json() + "\n"
        yield "]"  

    return StreamingResponse(generate_json(), media_type="application/json")
