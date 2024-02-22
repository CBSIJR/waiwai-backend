from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.auth import Authorization, security
from backend.configs import get_async_session
from backend.repositories import Categories
from backend.schemas import (
    CategoryCreate,
    CategoryPublic,
    CategoryUpdate,
    Message,
    ParamsCategory,
    PermissionType,
)

router = APIRouter(
    prefix='/categories',
    tags=['Categorias'],
)


@router.get(
    '/', status_code=status.HTTP_200_OK, response_model=list[CategoryPublic]
)
async def list_categories(
    params: ParamsCategory = Depends(),
    session: AsyncSession = Depends(get_async_session),
):
    categories = await Categories(session).get_list(params)
    return categories


@router.get(
    '/{category_id}',
    status_code=status.HTTP_200_OK,
    responses={'404': {'model': Message}},
    response_model=CategoryPublic,
)
async def get_category(
    category_id: int, session: AsyncSession = Depends(get_async_session)
):
    category = await Categories(session).get_by_id(category_id)
    return category


@router.post(
    '/',
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[
        Depends(security),
        Authorization([PermissionType.ADMIN]),
    ],
    responses={'403': {'model': Message}, '409': {'model': Message}},
)
async def create_category(
    category: CategoryCreate,
    session: AsyncSession = Depends(get_async_session),
) -> None:
    await Categories(session).create(category)


@router.put(
    '/{category_id}',
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
async def update_category(
    category_id: int,
    category: CategoryUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    await Categories(session).update_by_id(category_id, category)


@router.delete(
    '/{category_id}',
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
async def delete_category(
    category_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    await Categories(session).delete_by_id(category_id)
