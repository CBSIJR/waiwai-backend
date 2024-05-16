from typing import Sequence

from fastapi import HTTPException, status
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models import Category
from backend.schemas import CategoryCreate, CategoryUpdate, ParamsCategory

from .base import Repository

# https://stackoverflow.com/questions/68360687/sqlalchemy-asyncio-orm-how-to-query-the-database


class Categories(Repository):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__()
        self.session: AsyncSession = session

    async def get_list(self, params: ParamsCategory) -> Sequence[Category]:
        if params.q:
            search = '%{}%'.format(params.q)
            statement = (
                select(Category)
                .filter(func.upper(Category.category).like(func.upper(search)))
                .offset((params.page - 1) * params.page_size)
                .limit(params.page_size)
            )
        else:
            statement = (
                select(Category)
                .offset((params.page - 1) * params.page_size)
                .limit(params.page_size)
            )
        result = await self.session.execute(statement)
        categories = result.scalars().all()
        return categories

    async def create(self, entity: CategoryCreate) -> None:
        category_db = await self.get_by_category(entity.category)

        if category_db:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail='Categoria já registrada.',
            )

        category_db = Category(
            category=entity.category, description=entity.description
        )

        self.session.add(category_db)
        await self.session.commit()
        await self.session.refresh(category_db)

    async def get_by_id(self, entity_id: int) -> Category | None:
        statement = select(Category).filter(Category.id == entity_id)
        result = await self.session.execute(statement)
        category = result.scalar_one_or_none()
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'Categoria: ID {entity_id} não encontrado.',
            )
        return category

    async def get_by_category(self, entity_category: str) -> Category | None:
        statement = select(Category).where(
            func.upper(Category.category) == func.upper(entity_category)
        )
        result = await self.session.execute(statement)
        category = result.scalar_one_or_none()
        return category

    async def update_by_id(
        self, entity_id: int, entity: CategoryUpdate
    ) -> None:
        category_db = await self.get_by_id(entity_id)

        category_exists = await self.get_by_category(entity.category)

        if category_exists and category_exists.id != entity_id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail='Categoria já registrada.',
            )

        category_db.category = entity.category

        self.session.add(category_db)
        await self.session.commit()
        await self.session.refresh(category_db)

    async def delete_by_id(self, entity_id: int) -> None:
        category_db = await self.get_by_id(entity_id)

        await self.session.delete(category_db)
        await self.session.commit()

    async def all(self) -> Sequence[Category]:
        statement = select(Category)
        result = await self.session.execute(statement)
        categories = result.scalars().all()
        return categories
