from typing import Sequence

from fastapi import status
from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from backend.models import Meaning, Word, WordCategory
from backend.schemas import (
    CustomHTTPException,
    ParamsPageQuery,
    PermissionType,
    UserAuth,
    WordCreate,
    WordUpdate,
)

from .base import Repository
from .categories import Categories

# https://stackoverflow.com/questions/68360687/sqlalchemy-asyncio-orm-how-to-query-the-database


class Words(Repository):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__()
        self.session: AsyncSession = session

    async def get_list(
        self, params: ParamsPageQuery, user_id: int | None = None
    ) -> Sequence[Word]:
        statement = (
            select(Word)
            .options(joinedload(Word.categories))
            .options(joinedload(Word.meanings, innerjoin=False))
            .group_by(Word.id)
            .order_by(Word.word)
        )
        if user_id:
            statement = statement.where(Word.user_id == user_id)
        if params.q:
            search_filter = f'%{params.q.lower()}%'
            statement = statement.where(
                or_(
                    func.lower(Word.word).ilike(search_filter),
                    func.lower(Meaning.meaning_pt).ilike(search_filter),
                    func.lower(Meaning.meaning_ww).ilike(search_filter),
                    func.lower(Meaning.comment_pt).ilike(search_filter),
                    func.lower(Meaning.comment_ww).ilike(search_filter),
                )
            )
        statement = statement.join(Word.meanings)
        statement = statement.offset(
            (params.page - 1) * params.page_size
        ).limit(params.page_size)

        result = await self.session.execute(statement)
        words = result.unique().scalars().all()
        return words

    async def create(self, entity: WordCreate, user: UserAuth) -> Word:
        word_db = await self.get_by_word(entity.word)
        if word_db:
            raise CustomHTTPException(
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
            categories=categories_db_list,
        )

        self.session.add(word_db)
        await self.session.commit()
        await self.session.refresh(word_db)
        return word_db

    async def get_by_id(self, entity_id: int) -> Word:
        statement = (
            select(Word)
            .filter(Word.id == entity_id)
            .options(joinedload(Word.categories))
            .options(joinedload(Word.meanings).joinedload(Meaning.reference))
            .options(joinedload(Word.attachments))
        )
        result = await self.session.execute(statement)
        word = result.unique().scalar_one_or_none()
        if not word:
            raise CustomHTTPException(
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
            raise CustomHTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail='Usuário sem permissão.',
            )

        word_exists = await self.get_by_word(entity.word)

        if word_exists and word_exists.id != entity_id:
            raise CustomHTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail='Palavra já registrada.',
            )

        categories = Categories(self.session)
        categories_db_list = []
        for category in entity.categories:
            result_category = await categories.get_by_id(category)
            categories_db_list.append(result_category)

        word_db.word = entity.word
        word_db.phonemic = (entity.phonemic,)
        word_db.categories = categories_db_list

        self.session.add(word_db)
        await self.session.commit()

    async def delete_by_id(self, entity_id: int, user: UserAuth) -> None:
        word_db = await self.get_by_id(entity_id)

        if (
            word_db.user_id != user.id
            and user.permission != PermissionType.ADMIN
        ):
            raise CustomHTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail='Usuário sem permissão.',
            )

        await self.session.delete(word_db)
        await self.session.commit()

    async def all(self) -> Sequence[Word]:
        statement = select(Word)
        result = await self.session.execute(statement)
        words = result.scalars().all()
        return words

    async def all_wc(self) -> Sequence[WordCategory]:
        statement = select(WordCategory)
        result = await self.session.execute(statement)
        word_categories = result.all()
        return word_categories

    async def count(self, params: ParamsPageQuery) -> int:
        if not params.q:
            statement = select(func.count()).select_from(Word)
        else:
            statement = (
                select(func.count(func.distinct(Word.id)))
                .select_from(Word)
                .join(Word.meanings)
                .where(
                    or_(
                        func.lower(Word.word).ilike(f'%{params.q.lower()}%'),
                        func.lower(Meaning.meaning_pt).ilike(
                            f'%{params.q.lower()}%'
                        ),
                        func.lower(Meaning.meaning_ww).ilike(
                            f'%{params.q.lower()}%'
                        ),
                        func.lower(Meaning.comment_pt).ilike(
                            f'%{params.q.lower()}%'
                        ),
                        func.lower(Meaning.comment_ww).ilike(
                            f'%{params.q.lower()}%'
                        ),
                    )
                )
            )

        result = await self.session.execute(statement)
        return result.scalar_one()
