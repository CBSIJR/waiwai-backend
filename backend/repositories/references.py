from typing import Sequence

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models import Reference
from backend.schemas import ParamsReference, ReferenceCreate, ReferenceUpdate

from .base import Repository

# https://stackoverflow.com/questions/68360687/sqlalchemy-asyncio-orm-how-to-query-the-database


class References(Repository):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__()
        self.session: AsyncSession = session

    async def get_list(self, params: ParamsReference) -> Sequence[Reference]:
        if params.q:
            search = '%{}%'.format(params.q)
            statement = (
                select(Reference)
                .filter(Reference.reference.like(search))
                .offset((params.page - 1) * params.page_size)
                .limit(params.page_size)
            )
        else:
            statement = (
                select(Reference)
                .offset((params.page - 1) * params.page_size)
                .limit(params.page_size)
            )
        result = await self.session.execute(statement)
        references = result.scalars().all()

        return references

    async def create(self, entity: ReferenceCreate) -> None:
        reference_db = await self.get_by_reference(entity.reference)

        if reference_db:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail='Referência já registrada.',
            )

        reference_db = Reference(
            reference=entity.reference,
            url=str(entity.url) if entity.url else None,
        )

        self.session.add(reference_db)
        await self.session.commit()
        await self.session.refresh(reference_db)

    async def get_by_id(self, entity_id: int) -> Reference | None:
        statement = select(Reference).filter(Reference.id == entity_id)
        result = await self.session.execute(statement)
        reference = result.scalar_one_or_none()
        if not reference:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'Referência: ID {entity_id} não encontrado.',
            )
        return reference

    async def get_by_reference(
        self, entity_reference: str
    ) -> Reference | None:
        statement = select(Reference).where(
            Reference.reference == entity_reference
        )
        result = await self.session.execute(statement)
        reference = result.scalar_one_or_none()
        return reference

    async def update_by_id(
        self, entity_id: int, entity: ReferenceUpdate
    ) -> None:
        reference_db = await self.get_by_id(entity_id)

        reference_exists = await self.get_by_reference(entity.reference)

        if reference_exists and entity_id != reference_exists.id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail='Referência já registrada.',
            )

        reference_db.reference = entity.reference
        reference_db.url = str(entity.url) if entity.url else None

        self.session.add(reference_db)
        await self.session.commit()
        await self.session.refresh(reference_db)

    async def delete_by_id(self, entity_id: int) -> None:
        reference_db = await self.get_by_id(entity_id)

        await self.session.delete(reference_db)
        await self.session.commit()

    async def all(self) -> Sequence[Reference]:
        statement = select(Reference)
        result = await self.session.execute(statement)
        references = result.scalars().all()
        return references
