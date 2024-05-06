import asyncio
import pytest
from pytest_postgresql import factories
from pytest_postgresql.janitor import DatabaseJanitor
from contextlib import ExitStack
import pytest
from fastapi.testclient import TestClient

from src.app.app import init_app
from src.app.config import APIConfig
from src.app.database.database import get_db, sessionmanager
from src.app.database.database_access.data_access import DataAccess
from src.app.fill_db.create_tuples import CreateTuples
from src.app.database.database import sessionmanager

test_db = factories.postgresql_proc(port=None, dbname="test_db_api")

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

@pytest.fixture(autouse=True)
def app():
    with ExitStack():
        yield init_app(APIConfig())

@pytest.fixture
def client(app):
    with TestClient(app) as c:
        yield c

@pytest.fixture(scope="function", autouse=True)
async def session_override(app, connection_test):
    async def get_db_override():
        async with sessionmanager.session() as session:
            yield session

    app.dependency_overrides[get_db] = get_db_override

@pytest.fixture(scope="function", autouse=True)
async def data_access(connection_test):
    async with sessionmanager.session() as session:
        yield DataAccess(session)

@pytest.fixture(scope="function", autouse=True)
async def session(connection_test):
    async with sessionmanager.session() as session:
        yield session

@pytest.fixture(scope="function")
async def auth(client, data_access: DataAccess):
    data = {
        "email": "insert@example.com",
        "username": "test",
        "password": "test"
    }
    response = client.post("/auth/add_user", json=data)
    assert response.status_code == 200

    response = client.post("/auth/token", data=data)
    assert response.status_code == 200
    body = response.json()
    assert body["token_type"] == "bearer"
    token = body["access_token"]

    user_id = await data_access.UserAccess.get_user_id_email("insert@example.com")

    yield user_id, {"Authorization": f"Bearer {token}"}
