from typing import Sequence


from fastapi import HTTPException, status

from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.repositories import Repository
from backend.models import Word
from backend.schemas import Params, UserAuth, WordCreate


class Words(Repository):
    def __init__(self, session: Session) -> None:
        super().__init__()
        self.session: Session = session

    async def get_list(self, params: Params) -> Sequence[Word]:

        words = self.session.scalars(select(Word)
                                     .offset((params.page - 1) * params.page_size)
                                     .limit(params.page_size)).all()
        return words

    async def create(self, entity: WordCreate, user: UserAuth) -> None:
        db_word = await self.get_by_word(entity.word)

        if db_word:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail='Word already registered'
            )

        db_word = Word(
            word=entity.word,
            user_id=user.id
        )

        self.session.add(db_word)
        self.session.commit()
        self.session.refresh(db_word)

    async def get_by_id(self, entity_id: int) -> Word:
        return self.session.scalar(
            select(Word).where(Word.id == entity_id)
        )

    async def get_by_word(self, entity_word: str) -> Word:
        return self.session.scalar(
            select(Word).where(Word.word == entity_word)
        )

    async def update_by_id(self, entity_id: int, entity: Word, user: UserAuth) -> None:
        db_word = self.get_by_id(entity_id)
        if db_word:
            raise HTTPException(
                status_code=400, detail='Not found'
            )

        db_word = self.get_by_word(entity.word)
        if db_word:
            raise HTTPException(
                status_code=400, detail='Word already registered'
            )

        db_word = Word(
            word=entity.word
        )

        self.session.add(db_word)
        self.session.commit()
        self.session.refresh(db_word)

    async def delete_by_id(self, entity_id, user: UserAuth) -> None:
        pass
