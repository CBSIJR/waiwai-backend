from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.configs import get_async_session
from backend.repositories import Words
from backend.schemas import WordCategoryExport

from logging import Logger
from backend.utils import get_logger

router = APIRouter(
    prefix='/wordcategories',
    tags=['Palavras Categorias'],
)


@router.get(
    '/export/all',
    status_code=status.HTTP_200_OK,
    response_model=List[WordCategoryExport],
)
async def get_export(session: AsyncSession = Depends(get_async_session)):
    word_categories = await Words(session).all_wc()
    return word_categories
