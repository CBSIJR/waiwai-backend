from typing import Sequence

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from backend.models import Word
from backend.repositories import Categories, Repository
from backend.schemas import (
    Params,
    PermissionType,
    UserAuth,
    WordCreate,
    WordUpdate,
)

# https://stackoverflow.com/questions/68360687/sqlalchemy-asyncio-orm-how-to-query-the-database


class Words(Repository):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__()
        self.session: AsyncSession = session

    async def get_list(self, params: Params) -> Sequence[Word]:
        statement = (
            select(Word)
            .options(joinedload(Word.categories))
            .options(joinedload(Word.meanings))
            .offset((params.page - 1) * params.page_size)
            .limit(params.page_size)
            .order_by(Word.word)
        )
        result = await self.session.execute(statement)
        words = result.unique().scalars().all()
        return words

    async def create(self, entity: WordCreate, user: UserAuth) -> None:
        word_db = await self.get_by_word(entity.word)
        if word_db:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail='Palavra já registrada.',
            )

        categories = Categories(self.session)
        categories_db_list = []
        for category in entity.categories:
            result_category = await categories.get_by_id(category)
            categories_db_list.append(result_category)

        word_db = Word(
            word=entity.word,
            phonemic=entity.phonemic,
            user_id=user.id,
            categories=categories_db_list
        )

        self.session.add(word_db)
        await self.session.commit()

    async def get_by_id(self, entity_id: int) -> Word:
        statement = (
            select(Word)
            .filter(Word.id == entity_id)
            .options(joinedload(Word.categories))
            .options(joinedload(Word.meanings))
        )
        result = await self.session.execute(statement)
        word = result.unique().scalar_one_or_none()
        if not word:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'Palavra: ID {entity_id} não encontrado.',
            )
        return word

    async def get_by_word(self, entity_word: str) -> Word | None:
        statement = select(Word).where(Word.word == entity_word)
        result = await self.session.execute(statement)
        word = result.scalar_one_or_none()
        return word

    async def update_by_id(
        self, entity_id: int, entity: WordUpdate, user: UserAuth
    ) -> None:
        word_db = await self.get_by_id(entity_id)

        if (
            word_db.user_id != user.id
            and user.permission != PermissionType.ADMIN
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail='Usuário sem permissão.',
            )

        word_exists = await self.get_by_word(entity.word)

        if word_exists and word_exists.id != entity_id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail='Palavra já registrada.',
            )

        categories = Categories(self.session)
        categories_db_list = []
        for category in entity.categories:
            result_category = await categories.get_by_id(category)
            categories_db_list.append(result_category)

        word_db.word = entity.word
        word_db.phonemic = entity.phonemic,
        word_db.categories = categories_db_list

        self.session.add(word_db)
        await self.session.commit()

    async def delete_by_id(self, entity_id: int, user: UserAuth) -> None:
        word_db = await self.get_by_id(entity_id)

        if (
            word_db.user_id != user.id
            and user.permission != PermissionType.ADMIN
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail='Usuário sem permissão.',
            )

        await self.session.delete(word_db)
        await self.session.commit()
