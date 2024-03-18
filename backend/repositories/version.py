from typing import Sequence

from fastapi import HTTPException, status
from sqlalchemy import select, Row
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from backend.models import Version
from backend.repositories import Categories, Repository
from backend.schemas import (
    Params,
    PermissionType,
    UserAuth,
    WordCreate,
    WordUpdate,
)
from backend.utils import get_logger
# https://stackoverflow.com/questions/68360687/sqlalchemy-asyncio-orm-how-to-query-the-database


class Versions:
    def __init__(self, session: AsyncSession) -> None:
        self.session: AsyncSession = session

    async def first(self) -> Version:
        statement = select(Version)
        result = await self.session.execute(statement)
        version = result.scalar_one()
        return version
