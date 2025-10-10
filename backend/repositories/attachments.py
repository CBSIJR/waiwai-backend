from os import remove
from typing import Sequence, Union

from fastapi import status
from sqlalchemy import Row, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models import Attachment
from backend.schemas import (
    AttachmentCreate,
    AttachmentUpdate,
    CustomHTTPException,
    ParamsPageQuery,
    ParamsAttachments,
    PermissionType,
    UserAuth,
)

from .base import Repository
from .words import Words

# https://stackoverflow.com/questions/68360687/sqlalchemy-asyncio-orm-how-to-query-the-database


class Attachments(Repository):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__()
        self.session: AsyncSession = session
        self.words: Words = Words(session=self.session)

    async def get_list(self, params: ParamsPageQuery, user: Union[None, UserAuth] = None) -> Sequence[Attachment]:
        raise NotImplementedError

    async def create(self, entity: AttachmentCreate) -> Attachment:
        if await self.count_by_word_id(entity.word_id) >= 10:
            remove(entity.filedir)
            raise CustomHTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f'Palavra ID {entity.word_id}: O anexo excede o limite de 10 anexos por palavra.',
            )

        attachment_db = Attachment(
            uuid=entity.uuid,
            filename=entity.filename,
            filedir=entity.filedir,
            url=entity.url,
            content_type=entity.content_type,
            user_id=entity.user_id,
            word_id=entity.word_id,
        )

        self.session.add(attachment_db)
        await self.session.commit()
        await self.session.refresh(attachment_db)
        attachment_db.url = '/uploads/' + str(attachment_db.id)
        await self.session.commit()
        return attachment_db

    async def get_by_id(self, entity_id: int) -> Attachment:
        statement = select(Attachment).filter(Attachment.id == entity_id)
        result = await self.session.execute(statement)
        attachment = result.scalar_one_or_none()
        if not attachment:
            raise CustomHTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'Anexo: ID {entity_id} não encontrado.',
            )
        return attachment

    async def update_by_id(
        self, entity_id: int, entity: AttachmentUpdate
    ) -> None:
        raise NotImplementedError

    async def delete_by_id(self, entity_id: int, user: UserAuth) -> None:
        attachment_db = await self.get_by_id(entity_id)

        if (
            attachment_db.user_id != user.id
            and user.permission != PermissionType.ADMIN
        ):
            raise CustomHTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail='Usuário sem permissão.',
            )

        await self.session.delete(attachment_db)
        await self.session.commit()
        remove(attachment_db.filedir)

    async def count_by_word_id(self, word_id: int) -> int:
        statement = select(func.count(Attachment.id)).where(
            Attachment.word_id == word_id
        )
        result = await self.session.execute(statement)
        count_attachments = result.scalar()
        return count_attachments

    async def get_list_by_word_id(
        self, word_id: int, params: ParamsAttachments
    ) -> Sequence[Attachment]:
        await self.words.get_by_id(word_id)

        statement = (
            select(Attachment)
            .filter(Attachment.word_id == word_id)
            .offset((params.page - 1) * params.page_size)
            .limit(params.page_size)
        )

        result = await self.session.execute(statement)
        attachments = result.scalars().all()
        return attachments

    async def all(self) -> Sequence[Row[tuple[Attachment]]]:
        statement = select(Attachment)
        result = await self.session.execute(statement)
        attachments = result.fetchall()
        return [attachment[0] for attachment in attachments]

    async def count(self) -> int:
        statement = select(func.count()).select_from(Attachment)
        result = await self.session.execute(statement)
        return result.scalar_one()
