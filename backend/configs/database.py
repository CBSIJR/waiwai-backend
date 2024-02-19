from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import sessionmaker

from backend.configs import Settings

engine = create_async_engine(str(Settings().db_url), echo=True, future=True)
async_session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


# https://github.com/tiangolo/fastapi/issues/2662
# https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#using-asyncsession-with-concurrent-tasks
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
