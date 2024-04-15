from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
import pytest

from tests.conftest import sessionmanager
from .conftest import session, data_access

from src.app.database.database_access.alliance_access import AllianceAccess, Alliance, AllianceRequest
from src.app.database.database_access.user_access import UserAccess, User


@pytest.fixture(scope="function", autouse=True)
async def insert_users(data_access):
    user_access = data_access.UserAccess
    for i in range(1, 6):
        await user_access.create_user(f"Test{i}", f"test{i}@test.test", f"test{i}")
    await data_access.commit()

@pytest.fixture(scope="function", autouse=True)
async def alliance_access(data_access):
    yield data_access.AllianceAccess

async def test_create_alliance_1(session: AsyncSession, alliance_access: AllianceAccess):
    await alliance_access.create_alliance("Test Alliance")
    await alliance_access.commit()

    stmt = (
        select(Alliance)
        .where(Alliance.name == "Test Alliance")
    )
    result = await session.execute(stmt)
    assert result.scalar_one_or_none() is not None


async def test_create_alliance_2(session: AsyncSession, alliance_access: AllianceAccess):
    for i in range(4):
        await alliance_access.create_alliance(f"Test{i}")
    await alliance_access.commit()

    stmt = (
        select(Alliance)
    )
    result = await session.execute(stmt)
    assert len(result.scalars().all()) == 4


async def test_set_alliance_1(session: AsyncSession, alliance_access: AllianceAccess):
    await alliance_access.create_alliance("Test Alliance")
    await alliance_access.set_alliance(1, "Test Alliance")
    await alliance_access.commit()

    stmt = (
        select(User)
        .where(User.id == 1)
    )
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()
    assert user is not None
    assert user.alliance == "Test Alliance"


async def test_get_alliance_members_1(alliance_access: AllianceAccess):
    await alliance_access.create_alliance("Test Alliance")
    for i in range(1, 6):
        await alliance_access.set_alliance(i, "Test Alliance")
    await alliance_access.commit()

    users = await alliance_access.get_alliance_members("Test Alliance")
    assert len(users) == 5
    for user in users:
        assert user.alliance == "Test Alliance"

async def test_send_alliance_request_1(session: AsyncSession, alliance_access: AllianceAccess):
    await alliance_access.create_alliance("Test Alliance")
    await alliance_access.send_alliance_request(1, "Test Alliance")
    await alliance_access.commit()

    stmt = (
        select(AllianceRequest)
        .where(AllianceRequest.user_id == 1)
    )
    result = await session.execute(stmt)
    alliance_request = result.scalar_one_or_none()
    assert alliance_request is not None
    assert alliance_request.alliance_name == "Test Alliance"

async def test_send_alliance_request_2(session: AsyncSession, alliance_access: AllianceAccess):
    await alliance_access.create_alliance("Test Alliance 1")
    await alliance_access.create_alliance("Test Alliance 2")
    await alliance_access.send_alliance_request(1, "Test Alliance 1")
    await alliance_access.send_alliance_request(1, "Test Alliance 2")
    await alliance_access.commit()

    stmt = (
        select(AllianceRequest)
        .where(AllianceRequest.user_id == 1)
    )
    result = await session.execute(stmt)
    alliance_request = result.scalar_one_or_none()
    assert alliance_request is not None
    assert alliance_request.alliance_name == "Test Alliance 2"

async def test_accept_alliance_request_1(session: AsyncSession, alliance_access: AllianceAccess):
    await alliance_access.create_alliance("Test Alliance")
    await alliance_access.send_alliance_request(1, "Test Alliance")
    await alliance_access.accept_alliance_request(1, "Test Alliance")
    await alliance_access.commit()

    stmt = (
        select(User)
        .where(User.id == 1)
    )
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()
    assert user is not None
    assert user.alliance == "Test Alliance"

    stmt = (
        select(AllianceRequest)
        .where(AllianceRequest.user_id == 1)
    )
    result = await session.execute(stmt)
    alliance_request = result.scalar_one_or_none()
    assert alliance_request is None

async def test_reject_alliance_request_1(session: AsyncSession, alliance_access: AllianceAccess):
    await alliance_access.create_alliance("Test Alliance")
    await alliance_access.send_alliance_request(1, "Test Alliance")
    await alliance_access.reject_alliance_request(1)
    await alliance_access.commit()

    stmt = (
        select(User)
        .where(User.id == 1)
    )
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()
    assert user is not None
    assert user.alliance is None

    stmt = (
        select(AllianceRequest)
        .where(AllianceRequest.user_id == 1)
    )
    result = await session.execute(stmt)
    alliance_request = result.scalar_one_or_none()
    assert alliance_request is None

async def test_alliance_exists_1(alliance_access: AllianceAccess):
    await alliance_access.create_alliance("Test Alliance")
    await alliance_access.commit()

    assert await alliance_access.alliance_exists("Test Alliance")

async def test_alliance_exists_2(alliance_access: AllianceAccess):
    await alliance_access.create_alliance("Test Alliance")
    await alliance_access.commit()

    assert not await alliance_access.alliance_exists("Test Alliance 2")

async def test_alliance_exists_3(alliance_access: AllianceAccess):
    await alliance_access.create_alliance("Test Alliance")
    await alliance_access.commit()

    assert not await alliance_access.alliance_exists("Test Alliance 2")
    assert await alliance_access.alliance_exists("Test Alliance")

async def test_get_alliance_requests(alliance_access: AllianceAccess):
    await alliance_access.create_alliance("Test Alliance")
    await alliance_access.set_alliance(1, "Test Alliance")
    await alliance_access.send_alliance_request(2, "Test Alliance")
    await alliance_access.send_alliance_request(3, "Test Alliance")
    await alliance_access.send_alliance_request(4, "Test Alliance")
    await alliance_access.send_alliance_request(5, "Test Alliance")
    await alliance_access.commit()

    requests = await alliance_access.get_alliance_requests(1)
    assert len(requests) == 4

async def test_get_alliance(alliance_access: AllianceAccess):
    await alliance_access.create_alliance("Test Alliance")
    await alliance_access.set_alliance(1, "Test Alliance")
    await alliance_access.commit()

    alliance_name = await alliance_access.get_alliance(1)
    assert alliance_name == "Test Alliance"

async def test_get_alliance_2(alliance_access: AllianceAccess):
    alliance = await alliance_access.get_alliance(1)
    assert alliance is None
