from typing import Sequence, Union

from fastapi import status
from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models import Meaning
from backend.schemas import (
    ParamsPageQuery,
    CustomHTTPException,
    MeaningCreate,
    MeaningUpdate,
    ParamsMeaning,
    PermissionType,
    UserAuth,
)

from .references import References
from .base import Repository
from .words import Words

# https://stackoverflow.com/questions/68360687/sqlalchemy-asyncio-orm-how-to-query-the-database


class Meanings(Repository):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__()
        self.session: AsyncSession = session
        self.words: Words = Words(session=self.session)

    async def get_list(self, params: ParamsPageQuery, user: Union[None, UserAuth] = None) -> Sequence[Meaning]:
        if params.q:
            search = '%{}%'.format(params.q)
            statement = (
                select(Meaning)
                .where(
                    or_(
                        func.lower(Meaning.meaning_pt).ilike(
                            search
                        ),
                        func.lower(Meaning.meaning_ww).ilike(
                            search
                        ),
                        func.lower(Meaning.comment_pt).ilike(
                            search
                        ),
                        func.lower(Meaning.comment_ww).ilike(
                            search
                        )
                    )
                )
                .offset((params.page - 1) * params.page_size)
                .limit(params.page_size)
            )
        else:
            statement = (
                select(Meaning)
                .offset((params.page - 1) * params.page_size)
                .limit(params.page_size)
            )

        if user and user.permission is not PermissionType.ADMIN:
            statement = statement.where(Meaning.user_id == user.id)
        result = await self.session.execute(statement)
        meanings = result.scalars().all()

        return meanings

    async def create(
        self, word_id: int, entity: MeaningCreate, user: UserAuth
    ) -> Meaning:

        await Words(session=self.session).get_by_id(entity_id=word_id)
        await References(session=self.session).get_by_id(entity_id=entity.reference_id)

        meaning_db = Meaning(
            meaning_pt=entity.meaning_pt,
            meaning_ww=entity.meaning_ww,
            comment_pt=entity.comment_pt,
            comment_ww=entity.comment_ww,
            user_id=user.id,
            word_id=word_id,
            reference_id=entity.reference_id,
        )

        self.session.add(meaning_db)
        await self.session.commit()
        await self.session.refresh(meaning_db)
        return meaning_db

    async def get_by_id(self, entity_id: int) -> Meaning:
        statement = select(Meaning).filter(Meaning.id == entity_id)
        result = await self.session.execute(statement)
        meaning = result.scalar_one_or_none()
        if not meaning:
            raise CustomHTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'Significado: ID {entity_id} não encontrado.',
            )
        return meaning

    async def update_by_id(
        self, entity_id: int, entity: MeaningUpdate
    ) -> None:
        meaning_db = await self.get_by_id(entity_id)

        meaning_db.meaning_pt = (entity.meaning_pt,)
        meaning_db.meaning_ww = (entity.meaning_ww,)
        meaning_db.comment_pt = (entity.comment_pt,)
        meaning_db.comment_ww = (entity.comment_ww,)

        self.session.add(meaning_db)
        await self.session.commit()
        await self.session.refresh(meaning_db)

    async def delete_by_id(self, entity_id: int, user: UserAuth) -> None:
        meaning_db = await self.get_by_id(entity_id)

        if (
            meaning_db.user_id != user.id
            and user.permission != PermissionType.ADMIN
        ):
            raise CustomHTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail='Usuário sem permissão.',
            )

        await self.session.delete(meaning_db)
        await self.session.commit()

    async def get_list_by_word_id(
        self, word_id: int, params: ParamsMeaning
    ) -> Sequence[Meaning]:
        await self.words.get_by_id(word_id)

        if params.q:
            search = '%{}%'.format(params.q)
            statement = (
                select(Meaning)
                .filter(
                    func.upper(Meaning.meaning).like(func.upper(search)),
                    Meaning.word_id == word_id,
                )
                .offset((params.page - 1) * params.page_size)
                .limit(params.page_size)
            )
        else:
            statement = (
                select(Meaning)
                .filter(Meaning.word_id == word_id)
                .offset((params.page - 1) * params.page_size)
                .limit(params.page_size)
            )
        result = await self.session.execute(statement)
        meanings = result.scalars().all()

        return meanings

    async def all(self) -> Sequence[Meaning]:
        statement = select(Meaning)
        result = await self.session.execute(statement)
        meanings = result.scalars().all()
        return meanings

    async def count(self, params: ParamsPageQuery, user: Union[None, UserAuth]) -> int:
        statement = select(func.count()).select_from(Meaning)
        if params.q:
            statement = statement.where(
                or_(
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
                    )
                ))

        if user and user.permission is not PermissionType.ADMIN:
            statement = statement.where(Meaning.user_id == user.id)

        result = await self.session.execute(statement)
        return result.scalar_one()
