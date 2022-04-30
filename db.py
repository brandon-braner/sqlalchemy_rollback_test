from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker


async def create_session(base: declarative_base):
    engine = create_async_engine("sqlite:///Users/brandonbraner/tutorials/sqlalchemy-sessions/data.sqlite", echo=True, future=True)

    async with engine.begin() as conn:
        await conn.run_sync(base.metadata.drop_all)
        await conn.run_sync(base.metadata.create_all)
    # expire_on_commit=False will prevent attributes from being expired
    # after commit.
    async_session = sessionmaker(
        engine, expire_on_commit=False, class_=AsyncSession
    )
    with async_session as db:
        yield db