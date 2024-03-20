from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models import Version

# https://stackoverflow.com/questions/68360687/sqlalchemy-asyncio-orm-how-to-query-the-database


class Versions:
    def __init__(self, session: AsyncSession) -> None:
        self.session: AsyncSession = session

    async def first(self) -> Version:
        statement = select(Version)
        result = await self.session.execute(statement)
        version = result.scalar_one()
        return version
