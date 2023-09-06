from __future__ import annotations

from sqlalchemy import *
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
    )
    user_id = Column(
        BigInteger,
        unique=True,
        nullable=False,
    )
    name = Column(
        VARCHAR(length=64),
        nullable=False,
    )
    created_at = Column(
        DateTime,
        default=func.now(),
        nullable=False,
    )

    @staticmethod
    async def add(sessionmaker: async_sessionmaker, **kwargs) -> User:
        async with sessionmaker() as session:
            obj = User(**kwargs)
            session.add(obj)
            await session.commit()
            await session.refresh(obj)
            return obj

    @staticmethod
    async def is_exist(sessionmaker: async_sessionmaker, user_id: int) -> bool:
        async with sessionmaker() as session:
            filters = [User.user_id == user_id]
            query = await session.execute(select(User).filter(*filters))
            return bool(query.scalar())
