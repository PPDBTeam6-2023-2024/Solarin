from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base
from typing import AsyncGenerator

from .config import DBConfig

Base = declarative_base()


class Database:
    def __init__(self) -> None:
        self.__session = None
        self.__engine = None

    async def connect(self, config: DBConfig) -> None:
        self.__engine = create_async_engine(
            f"postgresql+asyncpg://{config.user}:{config.password.get_secret_value()}@{config.host}:{config.port}/{config.database}",
        )

        self.__session = async_sessionmaker(
            bind=self.__engine,
            autocommit=False,
            autoflush=False
        )

    async def disconnect(self) -> None:
        await self.__engine.dispose()

    async def get_db(self) -> AsyncGenerator[AsyncSession, None]:
        session = self.__session()
        try:
            yield session
        finally:
            await session.close()


db = Database()
