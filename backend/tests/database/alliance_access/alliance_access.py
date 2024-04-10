from sqlalchemy import select
import pytest

from tests.conftest import sessionmanager, connection_test

from src.app.database.database_access.alliance_access import AllianceAccess, Alliance, AllianceRequest
from src.app.database.database_access.user_access import UserAccess, User


@pytest.fixture(scope="function", autouse=True)
async def insert_users(connection_test):
    async with sessionmanager.session() as session:
        user_access = UserAccess(session)
        for i in range(1, 6):
            await user_access.createUser(f"Test{i}", f"test{i}@test.test", f"test{i}")
        await session.commit()


async def test_create_alliance_1(connection_test):
    async with sessionmanager.session() as session:
        alliance_access = AllianceAccess(session)
        await alliance_access.create_alliance("Test Alliance")
        await session.commit()

    async with sessionmanager.session() as session:
        stmt = (
            select(Alliance)
            .where(Alliance.name == "Test Alliance")
        )
        result = await session.execute(stmt)
        assert result.scalar_one_or_none() is not None


async def test_create_alliance_2(connection_test):
    async with sessionmanager.session() as session:
        alliance_access = AllianceAccess(session)

        for i in range(4):
            await alliance_access.create_alliance(f"Test{i}")
        await session.commit()

    async with sessionmanager.session() as session:
        stmt = (
            select(Alliance)
        )
        result = await session.execute(stmt)
        assert len(result.scalars().all()) == 4


async def test_set_alliance_1(connection_test):
    async with sessionmanager.session() as session:
        alliance_access = AllianceAccess(session)
        await alliance_access.create_alliance("Test Alliance")
        await alliance_access.set_alliance(1, "Test Alliance")
        await session.commit()

    async with sessionmanager.session() as session:
        stmt = (
            select(User)
            .where(User.id == 1)
        )
        result = await session.execute(stmt)
        user = result.scalar_one_or_none()
        assert user is not None
        assert user.alliance == "Test Alliance"


async def test_get_alliance_members_1(connection_test):
    async with sessionmanager.session() as session:
        alliance_access = AllianceAccess(session)
        await alliance_access.create_alliance("Test Alliance")
        for i in range(1, 6):
            await alliance_access.set_alliance(i, "Test Alliance")
        await session.commit()

    async with sessionmanager.session() as session:
        alliance_access = AllianceAccess(session)
        users = await alliance_access.get_alliance_members("Test Alliance")
        assert len(users) == 5
        for user in users:
            assert user.alliance == "Test Alliance"

async def test_send_alliance_request_1(connection_test):
    async with sessionmanager.session() as session:
        alliance_access = AllianceAccess(session)
        await alliance_access.create_alliance("Test Alliance")
        await alliance_access.send_alliance_request(1, "Test Alliance")
        await session.commit()

    async with sessionmanager.session() as session:
        stmt = (
            select(AllianceRequest)
            .where(AllianceRequest.user_id == 1)
        )
        result = await session.execute(stmt)
        alliance_request = result.scalar_one_or_none()
        assert alliance_request is not None
        assert alliance_request.alliance_name == "Test Alliance"

async def test_send_alliance_request_2(connection_test):
    async with sessionmanager.session() as session:
        alliance_access = AllianceAccess(session)
        await alliance_access.create_alliance("Test Alliance 1")
        await alliance_access.create_alliance("Test Alliance 2")
        await alliance_access.send_alliance_request(1, "Test Alliance 1")
        await alliance_access.send_alliance_request(1, "Test Alliance 2")
        await session.commit()

    async with sessionmanager.session() as session:
        stmt = (
            select(AllianceRequest)
            .where(AllianceRequest.user_id == 1)
        )
        result = await session.execute(stmt)
        alliance_request = result.scalar_one_or_none()
        assert alliance_request is not None
        assert alliance_request.alliance_name == "Test Alliance 2"

async def test_accept_alliance_request_1(connection_test):
    async with sessionmanager.session() as session:
        alliance_access = AllianceAccess(session)
        await alliance_access.create_alliance("Test Alliance")
        await alliance_access.send_alliance_request(1, "Test Alliance")
        await alliance_access.accept_alliance_request(1, "Test Alliance")
        await session.commit()

    async with sessionmanager.session() as session:
        stmt = (
            select(User)
            .where(User.id == 1)
        )
        result = await session.execute(stmt)
        user = result.scalar_one_or_none()
        assert user is not None
        assert user.alliance == "Test Alliance"

    async with sessionmanager.session() as session:
        stmt = (
            select(AllianceRequest)
            .where(AllianceRequest.user_id == 1)
        )
        result = await session.execute(stmt)
        alliance_request = result.scalar_one_or_none()
        assert alliance_request is None

async def test_reject_alliance_request_1(connection_test):
    async with sessionmanager.session() as session:
        alliance_access = AllianceAccess(session)
        await alliance_access.create_alliance("Test Alliance")
        await alliance_access.send_alliance_request(1, "Test Alliance")
        await alliance_access.reject_alliance_request(1)
        await session.commit()

    async with sessionmanager.session() as session:
        stmt = (
            select(User)
            .where(User.id == 1)
        )
        result = await session.execute(stmt)
        user = result.scalar_one_or_none()
        assert user is not None
        assert user.alliance is None

    async with sessionmanager.session() as session:
        stmt = (
            select(AllianceRequest)
            .where(AllianceRequest.user_id == 1)
        )
        result = await session.execute(stmt)
        alliance_request = result.scalar_one_or_none()
        assert alliance_request is None

async def test_alliance_exists_1(connection_test):
    async with sessionmanager.session() as session:
        alliance_access = AllianceAccess(session)
        await alliance_access.create_alliance("Test Alliance")
        await session.commit()

    async with sessionmanager.session() as session:
        alliance_access = AllianceAccess(session)
        assert await alliance_access.alliance_exists("Test Alliance")

async def test_alliance_exists_2(connection_test):
    async with sessionmanager.session() as session:
        alliance_access = AllianceAccess(session)
        await alliance_access.create_alliance("Test Alliance")
        await session.commit()

    async with sessionmanager.session() as session:
        alliance_access = AllianceAccess(session)
        assert not await alliance_access.alliance_exists("Test Alliance 2")

async def test_alliance_exists_3(connection_test):
    async with sessionmanager.session() as session:
        alliance_access = AllianceAccess(session)
        await alliance_access.create_alliance("Test Alliance")
        await session.commit()

    async with sessionmanager.session() as session:
        alliance_access = AllianceAccess(session)
        assert not await alliance_access.alliance_exists("Test Alliance 2")
        assert await alliance_access.alliance_exists("Test Alliance")

async def test_get_alliance_requests(connection_test):
    async with sessionmanager.session() as session:
        alliance_access = AllianceAccess(session)
        await alliance_access.create_alliance("Test Alliance")
        await alliance_access.set_alliance(1, "Test Alliance")
        await alliance_access.send_alliance_request(2, "Test Alliance")
        await alliance_access.send_alliance_request(3, "Test Alliance")
        await alliance_access.send_alliance_request(4, "Test Alliance")
        await alliance_access.send_alliance_request(5, "Test Alliance")
        await session.commit()

    async with sessionmanager.session() as session:
        alliance_access = AllianceAccess(session)
        requests = await alliance_access.get_alliance_requests(1)
        assert len(requests) == 4

async def test_get_alliance(connection_test):
    async with sessionmanager.session() as session:
        alliance_access = AllianceAccess(session)
        await alliance_access.create_alliance("Test Alliance")
        await alliance_access.set_alliance(1, "Test Alliance")
        await session.commit()

    async with sessionmanager.session() as session:
        alliance_access = AllianceAccess(session)
        alliance_name = await alliance_access.get_alliance(1)
        assert alliance_name == "Test Alliance"

async def test_get_alliance_2(connection_test):
    async with sessionmanager.session() as session:
        alliance_access = AllianceAccess(session)
        alliance = await alliance_access.get_alliance(1)
        assert alliance is None
