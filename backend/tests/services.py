from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession, AsyncEngine
from sqlalchemy import StaticPool
from fastapi import FastAPI, APIRouter
from typing import Tuple


from ..src.app.database.database import db


def create_test_services(router: APIRouter) -> Tuple[TestClient, async_sessionmaker[AsyncSession], AsyncEngine]:
    db_url = "sqlite+aiosqlite://"
    db_url = f"postgresql+asyncpg://postgres:postgres@localhost:5432/postgres"

    engine = create_async_engine(
        db_url,
        poolclass=StaticPool
    )
    TestingSessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)

    app = FastAPI()
    app.include_router(router)

    async def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            await db.close()

    app.dependency_overrides[db.get_db] = override_get_db

    client = TestClient(app)

    return client, TestingSessionLocal, engine
