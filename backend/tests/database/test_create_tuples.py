import pytest

from src.app.database.database import sessionmanager
from src.app.database.database_access.developer_access import *

@pytest.fixture(scope="function", autouse=True)
async def prepare_developer_access():
    async with sessionmanager.session() as session:
        dev_access = DeveloperAccess(session)
        return dev_access


async def test_create_tuples(prepare_developer_access):
    # TODO
    print(prepare_developer_access)