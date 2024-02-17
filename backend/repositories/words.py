from typing import Sequence

from fastapi import HTTPException, status

from sqlalchemy import select, Row
from sqlalchemy.ext.asyncio import AsyncSession

from backend.repositories import Repository
from backend.models import Word
from backend.schemas import Params, UserAuth, WordCreate

# https://stackoverflow.com/questions/68360687/sqlalchemy-asyncio-orm-how-to-query-the-database


class Words(Repository):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__()
        self.session: AsyncSession = session

    async def get_list(self, params: Params) -> Sequence[Row[tuple[Word]]]:
        statement = select(Word).offset((params.page - 1) * params.page_size).limit(params.page_size)
        result = await self.session.execute(statement)
        words = result.all()
        return words

    async def create(self, entity: WordCreate, user: UserAuth) -> None:
        word_db = await self.get_by_word(entity.word)

        if word_db:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail='Palavra já registrada.'
            )

        word_db = Word(
            word=entity.word,
            user_id=user.id
        )

        self.session.add(word_db)
        await self.session.commit()
        await self.session.refresh(word_db)

    async def get_by_id(self, entity_id: int) -> Row[tuple[Word]]:
        statement = select(Word).filter(Word.id == entity_id)
        result = await self.session.execute(statement)
        word = result.one_or_none()
        if not word:
            raise HTTPException(
                status_code=400, detail='Not found'
            )

        return word

    async def get_by_word(self, entity_word: str) -> Row[tuple[Word]] | None:
        statement = select(Word).where(Word.word == entity_word)
        result = await self.session.execute(statement)
        word = result.one_or_none()
        return word

    async def update_by_id(self, entity_id: int, entity: Word, user: UserAuth) -> None:
        await self.get_by_id(entity_id)

        db_word = await self.get_by_word(entity.word)
        if db_word:
            raise HTTPException(
                status_code=400, detail='Word already registered'
            )

        db_word = Word(
            word=entity.word
        )

        self.session.add(db_word)
        await self.session.commit()
        await self.session.refresh(db_word)

    async def delete_by_id(self, entity_id, user: UserAuth) -> None:
        pass
