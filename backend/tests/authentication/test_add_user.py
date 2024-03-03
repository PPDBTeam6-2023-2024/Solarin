import json
from typing import AsyncGenerator
import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from tests.services import create_test_services

from src.app.database.models.models import Base

from src.app.routers.authentication.router import router
from src.app.routers.authentication.schemas import UserCreate
from src.app.routers.authentication.router import pwd_context
from src.app.models import User as UserTable

client, TestingSessionLocal, engine = create_test_services(router)


@pytest_asyncio.fixture
async def session() -> AsyncGenerator[AsyncSession, None]:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with TestingSessionLocal() as session:
        schema = UserCreate(**json.loads(open("./data/inside_db.json").read()))
        user = UserTable(
            email=schema.email,
            username=schema.username,
            hashed_password=pwd_context.hash(schema.password)
        )
        session.add(user)
        await session.commit()

        yield session

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


pytestmark = pytest.mark.asyncio


#################################################################################
#################################################################################
#################################################################################

async def test_add_user_db_happy(session: AsyncSession):
    schema = UserCreate(**json.loads(open("./data/insert.json").read()))
    user = UserTable(
        email=schema.email,
        username=schema.username,
        hashed_password=pwd_context.hash(schema.password)
    )
    session.add(user)
    assert user.email == "insert@example.com"
    await session.commit()
    await session.refresh(user)
    assert user.email == "insert@example.com"


async def test_add_user_db_already_inside(session: AsyncSession):
    schema = UserCreate(**json.loads(open("./data/inside_db.json").read()))
    user = UserTable(
        email=schema.email,
        username=schema.username,
        hashed_password=pwd_context.hash(schema.password)
    )
    session.add(user)
    try:
        await session.commit()
    except Exception as e:
        pass
    else:
        assert False


async def test_add_user_api_happy(session: AsyncSession):
    data = json.loads(open("./data/insert.json").read())
    response = client.post("/auth/add_user", json=data)
    body = response.json()

    assert response.status_code == 200
    assert body["email"] == "insert@example.com"
    assert body["username"] == "insert"


async def test_add_user_api_already_inside(session: AsyncSession):
    data = json.loads(open("./data/inside_db.json").read())
    response = client.post("/auth/add_user", json=data)

    assert response.status_code == 404


async def test_add_user_api_invalid_email(session: AsyncSession):
    data = json.loads(open("./data/invalid_email.json").read())
    response = client.post("/auth/add_user", json=data)

    assert response.status_code == 422


async def test_add_user_api_invalid_schema(session: AsyncSession):
    data = json.loads(open("./data/invalid_schema.json").read())
    response = client.post("/auth/add_user", json=data)

    assert response.status_code == 422

