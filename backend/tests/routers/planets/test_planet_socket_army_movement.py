from tests.conftest import client

from src.app.database.database_access.data_access import DataAccess
from src.app.database.database import sessionmanager


async def test_get_armies(client):
    data = {
        "email": "insert@example.com",
        "username": "test",
        "password": "test"
    }
    response = client.post("/auth/add_user", json=data)
    assert response.status_code == 200

    async with sessionmanager.session() as session:
        data_access = DataAccess(session)

        user_id = await data_access.UserAccess.getUserIdEmail(
            email="insert@example.com"
        )

        region_id = await data_access.PlanetAccess.createSpaceRegion("test")
        await data_access.DeveloperAccess.createPlanetType("arctic")
        planet_id = await data_access.PlanetAccess.createPlanet("test", "arctic", region_id)

        await data_access.ArmyAccess.create_army(user_id, planet_id, 0, 0)
        await data_access.ArmyAccess.create_army(user_id, planet_id, 0, 0)
        await session.commit()

    data = {
        "username": "test",
        "password": "test"
    }
    headers = {
        "content-type": "application/x-www-form-urlencoded",
        "accept": "application/json",
    }
    response = client.post("/auth/token", data=data, headers=headers)
    assert response.status_code == 200

    body = response.json()
    assert body["token_type"] == "bearer"
    token = body["access_token"]

    with client.websocket_connect(f"/planet/ws/{planet_id}", subprotocols=[token]) as websocket:
        websocket.send_json({"type": "get_armies"})
        data = websocket.receive_json()
        assert data["request_type"] == "get_armies"
        assert len(data["data"]) == 2
        assert "x" in data["data"][0]


async def test_move_army(client):
    data = {
        "email": "insert@example.com",
        "username": "test",
        "password": "test"
    }
    response = client.post("/auth/add_user", json=data)
    assert response.status_code == 200

    async with sessionmanager.session() as session:
        data_access = DataAccess(session)

        user_id = await data_access.UserAccess.getUserIdEmail(
            email="insert@example.com"
        )

        region_id = await data_access.PlanetAccess.createSpaceRegion("test")
        await data_access.DeveloperAccess.createPlanetType("arctic")
        planet_id = await data_access.PlanetAccess.createPlanet("test", "arctic", region_id)

        army_id = await data_access.ArmyAccess.create_army(user_id, planet_id, 0, 0)
        await session.commit()

    data = {
        "username": "test",
        "password": "test"
    }
    headers = {
        "content-type": "application/x-www-form-urlencoded",
        "accept": "application/json",
    }
    response = client.post("/auth/token", data=data, headers=headers)
    assert response.status_code == 200

    body = response.json()
    assert body["token_type"] == "bearer"
    token = body["access_token"]

    with client.websocket_connect(f"/planet/ws/{planet_id}", subprotocols=[token]) as websocket:
        websocket.send_json({
            "type": "change_direction",
            "army_id": army_id,
            "to_x": 1,
            "to_y": 1
        })
        data = websocket.receive_json()
        assert data["request_type"] == "change_direction"
        assert "data" in data
