from typing import Sequence, Union

from fastapi import status
from sqlalchemy import func, or_, and_, select, cast, Numeric
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from backend.configs import async_session_maker
from backend.models import Meaning, Word, WordCategory, WordReview, WordStatus
from backend.utils import translate_char
from backend.schemas import (
    CustomHTTPException,
    ParamsPageQuery,
    PermissionType,
    UserAuth,
    WordCreate,
    WordReviewCreate,
    WordStatus,
    WordUpdate,
    LetterStatistic
)
from warnings import deprecated
from .base import Repository
from .categories import Categories

# https://stackoverflow.com/questions/68360687/sqlalchemy-asyncio-orm-how-to-query-the-database


class Words(Repository):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__()
        self.session: AsyncSession = session

    async def get_list(
        self, params: ParamsPageQuery, user: Union[None, UserAuth] = None, only_mine: bool = False
    ) -> Sequence[Word]:
        statement = (
            select(Word)
            .options(joinedload(Word.categories))
            .options(joinedload(Word.meanings))
            .group_by(Word.id)
            .order_by(Word.word)
        )

        # Filtro de visibilidade baseado em aprovação:
        # - se only_mine: vê apenas as suas próprias palavras.
        # - ADMIN: vê todas as palavras independente do status (se não for only_mine).
        # - USER autenticado: vê as APPROVED + as suas próprias (qualquer status).
        # - Público (sem autenticação): vê apenas APPROVED.
        if only_mine and user:
            statement = statement.where(Word.user_id == user.id)
        elif user and user.permission == PermissionType.ADMIN:
            pass  # ADMIN vê tudo, nenhum filtro adicional.
        elif user:
            statement = statement.where(
                or_(
                    Word.status == WordStatus.APPROVED,
                    Word.user_id == user.id,
                )
            )
        else:
            statement = statement.where(Word.status == WordStatus.APPROVED)

        if params.q or params.starts_with:
            search_filter = f'%{params.q.lower()}%' if params.q else f'{params.starts_with.lower()}%'
            if params.starts_with:
                condition = or_(
                    func.lower(translate_char(Word.word)).ilike(search_filter)
                )
            if params.q:
                condition = or_(
                    func.lower(Word.word).ilike(search_filter),
                    func.lower(Meaning.meaning_pt).ilike(search_filter),
                    func.lower(Meaning.meaning_ww).ilike(search_filter),
                    func.lower(Meaning.comment_pt).ilike(search_filter),
                    func.lower(Meaning.comment_ww).ilike(search_filter),
                )

            statement = statement.where(
                condition
            )
        statement = statement.outerjoin(Word.meanings,)
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

        # Regra de negócio: ADMINs publicam direto. USERs submetem para moderação.
        initial_status = (
            WordStatus.APPROVED
            if user.permission == PermissionType.ADMIN
            else WordStatus.PENDING
        )

        word_db = Word(
            word=entity.word,
            phonemic=entity.phonemic,
            user_id=user.id,
            categories=categories_db_list,
            status=initial_status,
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
            .options(joinedload(Word.reviews))
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
        word_db.phonemic = entity.phonemic
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

    async def add_review(
        self, word_id: int, review_data: WordReviewCreate, reviewer: UserAuth
    ) -> WordReview:
        """
        Persiste uma revisão de um ADMIN sobre uma palavra.

        Atualiza `word.status` de forma atômica com a criação da `WordReview`,
        garantindo que o estado da palavra e o histórico de revisão estejam
        sempre em sincronia dentro de uma única transação.
        """
        word_db = await self.get_by_id(word_id)

        review = WordReview(
            word_id=word_id,
            reviewer_id=reviewer.id,
            status=review_data.status,
            comment=review_data.comment,
        )
        # Sincroniza o status raiz da palavra para refletir a última decisão.
        word_db.status = review_data.status

        self.session.add(review)
        self.session.add(word_db)
        await self.session.commit()
        await self.session.refresh(review)
        return review


    @deprecated("This function is deprecated; use stream_all() instead.")
    async def all(self) -> Sequence[Word]:
        statement = select(Word)
        stream = await self.session.stream(statement)
        async for row in stream.scalars():
            yield row

    @staticmethod
    async def stream_all():
        async with async_session_maker() as session:
            statement = select(Word).execution_options(yield_per=100)
            stream = await session.stream_scalars(statement)
            async for row in stream:
                yield row

    async def all_wc(self) -> Sequence[WordCategory]:
        statement = select(WordCategory)
        result = await self.session.execute(statement)
        word_categories = result.all()
        return word_categories

    async def get_letter_statistic(self) -> Sequence[LetterStatistic]:
        subq = select(func.count("*")).select_from(Word).scalar_subquery()
        
        first_letter = func.left(translate_char(Word.word), 1).label("first_letter")
        statement = (
            select(
                first_letter,
                func.count().label("count"),
                func.round(
                    cast((func.count() * 100.0 / subq), Numeric),
                    4
                ).label("percentage")
            )
            .group_by(first_letter)
            .order_by(first_letter)
        )
        result = await self.session.execute(statement)
        rows = result.mappings().all()
        return rows

    async def count(self, params: ParamsPageQuery, user: Union[None, UserAuth] = None, only_mine: bool = False) -> int:
        has_q = bool(params.q)
        has_starts = bool(params.starts_with)

        if not has_q and not has_starts:
            statement = select(func.count()).select_from(Word)

        else:
            statement = (
                select(func.count(func.distinct(Word.id)))
                .select_from(Word)
                .outerjoin(Word.meanings)
            )

            if has_q:
                search_value = params.q.lower()
                condition = or_(
                    func.lower(Word.word).ilike(f'%{search_value}%'),
                    func.lower(Meaning.meaning_pt).ilike(f'%{search_value}%'),
                    func.lower(Meaning.meaning_ww).ilike(f'%{search_value}%'),
                    func.lower(Meaning.comment_pt).ilike(f'%{search_value}%'),
                    func.lower(Meaning.comment_ww).ilike(f'%{search_value}%'),
                )

            else:
                search_value = params.starts_with.lower()
                condition = func.lower(translate_char(Word.word)).ilike(f'{search_value}%')

            statement = statement.where(condition)

        if only_mine and user:
            statement = statement.where(Word.user_id == user.id)
        elif user and user.permission is not PermissionType.ADMIN:
            statement = statement.where(Word.user_id == user.id)

        result = await self.session.execute(statement)
        return result.scalar_one()
