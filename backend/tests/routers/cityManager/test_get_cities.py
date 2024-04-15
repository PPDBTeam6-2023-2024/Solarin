import pytest
from tests.conftest import client


async def test_get_cities(client):
    response = client.get(f"/cityManager/cities/{1}")
    assert response.status_code == 200
