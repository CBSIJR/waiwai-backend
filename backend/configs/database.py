from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from backend.configs import Settings

engine = create_async_engine(str(Settings().db_url), echo=True, future=True)


# https://github.com/tiangolo/fastapi/issues/2662
# https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#using-asyncsession-with-concurrent-tasks
async def get_async_session() -> AsyncSession:
    async with AsyncSession(engine) as session:
        yield session
