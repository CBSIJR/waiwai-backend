from typing import Sequence

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models import Category
from backend.repositories import Repository
from backend.schemas import (
    CategoryCreate,
    CategoryUpdate,
    Params,
    PermissionType,
    UserAuth,
)

# https://stackoverflow.com/questions/68360687/sqlalchemy-asyncio-orm-how-to-query-the-database


class Categories(Repository):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__()
        self.session: AsyncSession = session

    async def get_list(self, params: Params) -> Sequence[Category]:
        statement = (
            select(Category)
            .offset((params.page - 1) * params.page_size)
            .limit(params.page_size)
        )
        result = await self.session.execute(statement)
        categories = result.scalars().all()
        return categories

    async def create(self, entity: CategoryCreate, user: UserAuth) -> None:
        category_db = await self.get_by_category(entity.category)

        if category_db:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail='Categoria já registrada.',
            )

        category_db = Category(
            category=entity.category,
            description=entity.description,
            user_id=user.id,
        )

        self.session.add(category_db)
        await self.session.commit()

    async def get_by_id(self, entity_id: int) -> Category | None:
        statement = select(Category).filter(Category.id == entity_id)
        result = await self.session.execute(statement)
        category = result.scalar_one_or_none()
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail='Não encontrado.'
            )
        return category

    async def get_by_category(self, entity_category: str) -> Category | None:
        statement = select(Category).where(
            Category.category == entity_category
        )
        result = await self.session.execute(statement)
        category = result.scalar_one_or_none()
        return category

    async def update_by_id(
        self, entity_id: int, entity: CategoryUpdate, user: UserAuth
    ) -> None:
        category_db = await self.get_by_id(entity_id)

        if category_db.user_id != user.id or (
            category_db.user_id != user.id
            and user.permission != PermissionType.ADMIN
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail='Usuário sem permissão.',
            )

        if await self.get_by_category(entity.category):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail='Categoria já registrada.',
            )

        category_db.category = entity.category

        self.session.add(category_db)
        await self.session.commit()
        await self.session.refresh(category_db)

    async def delete_by_id(self, entity_id: int, user: UserAuth) -> None:
        category_db = await self.get_by_id(entity_id)

        if category_db.user_id != user.id or (
            category_db.user_id != user.id
            and user.permission != PermissionType.ADMIN
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail='Usuário sem permissão.',
            )

        await self.session.delete(category_db)
        await self.session.commit()
