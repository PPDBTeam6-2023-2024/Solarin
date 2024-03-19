import pytest
from tests.conftest import client


async def test_get_buildings(client):

    response = client.get("/cityManager/buildings", params={"city_id": 1})
    assert response.status_code == 200




