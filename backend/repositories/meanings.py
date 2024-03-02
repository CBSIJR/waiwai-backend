from typing import Sequence

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models import Meaning
from backend.repositories import Repository
from .words import Words
from backend.schemas import MeaningCreate, MeaningUpdate, ParamsMeaning

# https://stackoverflow.com/questions/68360687/sqlalchemy-asyncio-orm-how-to-query-the-database


class Meanings(Repository):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__()
        self.session: AsyncSession = session
        self.words: Words = Words(session=self.session)

    async def get_list(self, params: ParamsMeaning) -> Sequence[Meaning]:
        if params.q:
            search = '%{}%'.format(params.q)
            statement = (
                select(Meaning)
                .filter(Meaning.meaning.like(search))
                .offset((params.page - 1) * params.page_size)
                .limit(params.page_size)
            )
        else:
            statement = (
                select(Meaning)
                .offset((params.page - 1) * params.page_size)
                .limit(params.page_size)
            )
        result = await self.session.execute(statement)
        meanings = result.scalars().all()

        return meanings

    async def create(self, entity: MeaningCreate) -> None:
        meaning_db = Meaning(
            meaning=entity.meaning,
            comment=entity.comment,
            chapter_id=entity.chapter_id,
            entry_id=entity.entry_id,
            word_id=entity.word_id,
            reference_id=entity.reference_id,
        )
        self.session.add(meaning_db)
        await self.session.commit()
        await self.session.refresh(meaning_db)

    async def get_by_id(self, entity_id: int) -> Meaning:
        statement = select(Meaning).filter(Meaning.id == entity_id)
        result = await self.session.execute(statement)
        meaning = result.scalar_one_or_none()
        if not meaning:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'Significado: ID {entity_id} não encontrado.',
            )
        return meaning

    async def update_by_id(
        self, entity_id: int, entity: MeaningUpdate
    ) -> None:
        meaning_db = await self.get_by_id(entity_id)

        meaning_db.meaning = entity.meaning
        meaning_db.comment = entity.comment
        meaning_db.chapter_id = entity.chapter_id
        meaning_db.entry_id = entity.entry_id
        meaning_db.reference_id = entity.reference_id

        self.session.add(meaning_db)
        await self.session.commit()
        await self.session.refresh(meaning_db)

    async def delete_by_id(self, entity_id: int) -> None:
        meaning_db = await self.get_by_id(entity_id)

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
                    Meaning.meaning.like(search), Meaning.word_id == word_id
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

    async def create_by_word(
        self, word_id: int, entity: MeaningCreate
    ) -> None:
        meaning_db = Meaning(
            meaning=entity.meaning,
            comment=entity.comment,
            chapter_id=entity.chapter_id,
            entry_id=entity.entry_id,
            word_id=word_id,
            reference_id=entity.reference_id,
        )
        self.session.add(meaning_db)
        await self.session.commit()
        await self.session.refresh(meaning_db)
