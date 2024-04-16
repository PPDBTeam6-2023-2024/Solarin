import asyncio
import pytest
from pytest_postgresql import factories
from pytest_postgresql.janitor import DatabaseJanitor

from src.app.fill_db.create_tuples import CreateTuples
from src.app.database.database import sessionmanager
from src.app.database.database_access.data_access import DataAccess

test_db = factories.postgresql_proc(port=None, dbname="test_db_db")

@pytest.fixture(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session", autouse=True)
async def connection_test(test_db, event_loop):
    pg_host = test_db.host
    pg_port = test_db.port
    pg_user = test_db.user
    pg_db = test_db.dbname
    pg_password = test_db.password

    with DatabaseJanitor(
        pg_user, pg_host, pg_port, pg_db, test_db.version, pg_password
    ):
        connection_str = f"postgresql+psycopg://{pg_user}:@{pg_host}:{pg_port}/{pg_db}"
        sessionmanager.init(connection_str)
        yield
        await sessionmanager.close()

@pytest.fixture(scope="function", autouse=True)
async def create_tables(connection_test):
    async with sessionmanager.connect() as connection:
        await sessionmanager.drop_all(connection)
        await sessionmanager.create_all(connection)
    async with sessionmanager.session() as session:
        await CreateTuples().create_all_tuples(session)


@pytest.fixture(scope="function", autouse=True)
async def data_access(connection_test):
    async with sessionmanager.session() as session:
        yield DataAccess(session)

@pytest.fixture(scope="function", autouse=True)
async def session(connection_test):
    async with sessionmanager.session() as session:
        yield session

