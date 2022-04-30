import asyncio

from sqlalchemy import Column, select
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()


class User(Base):
    __tablename__ = "user_account"
    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    fullname = Column(String)


    def __repr__(self):
        return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"


async def create_session(base: declarative_base):
    engine = create_async_engine("postgresql+asyncpg://postgres:password@localhost:5439/test", echo=True,
                                 future=True)

    async with engine.begin() as conn:
        await conn.run_sync(base.metadata.drop_all)
        await conn.run_sync(base.metadata.create_all)

    return sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def main():
    async_session = await create_session(Base)
    async with async_session() as session:
        async with session.begin():
            user = User(name="brandon_rollback", fullname="Brandon Rollback")
            session.add(user)
            # await session.commit()

            selected_user = await session.execute(select(User).where(User.name == "brandon_rollback"))
            print(selected_user.scalars().first())
        await session.rollback()


asyncio.run(main())
