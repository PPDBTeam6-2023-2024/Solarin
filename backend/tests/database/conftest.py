import pytest

from tests.conftest import sessionmanager, connection_test

from src.app.database.database_access.data_access import DataAccess

@pytest.fixture(scope="function", autouse=True)
async def data_access(connection_test):
    async with sessionmanager.session() as session:
        yield DataAccess(session)

@pytest.fixture(scope="function", autouse=True)
async def session(connection_test):
    async with sessionmanager.session() as session:
        yield session

