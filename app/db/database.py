from __future__ import annotations

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.config import DatabaseConfig
from app.db.models import Base


class Database:

    def __init__(self, config: DatabaseConfig):
        self.engine = create_async_engine(
            f"mysql+aiomysql://"
            f"{config.USER}:"
            f"{config.PASS}@"
            f"{config.HOST}:"
            f"{config.PORT}/"
            f"{config.NAME}",
            pool_pre_ping=True,
        )
        self.sessionmaker = async_sessionmaker(
            bind=self.engine,
            class_=AsyncSession,
            expire_on_commit=False
        )

    async def init(self) -> Database:
        async with self.engine.begin() as connection:
            await connection.run_sync(Base.metadata.create_all)
        return self

    async def close(self) -> None:
        await self.engine.dispose()
