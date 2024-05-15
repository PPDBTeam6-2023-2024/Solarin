from src.app.database.database_access.data_access import DataAccess
from src.app.database.database import sessionmanager


async def test_get_armies(client, data_access: DataAccess):
    data = {
        "email": "insert@example.com",
        "username": "test",
        "password": "test"
    }
    response = client.post("/auth/add_user", json=data)
    assert response.status_code == 200

    user_id = await data_access.UserAccess.get_user_id_email(
        email="insert@example.com"
    )

    planet_id = await data_access.PlanetAccess.create_planet("test", "arctic", 1, 1)

    await data_access.ArmyAccess.create_army(user_id, planet_id, 0, 0)
    await data_access.ArmyAccess.create_army(user_id, planet_id, 0, 0)
    await data_access.commit()

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


async def test_move_army(client, data_access: DataAccess):
    data = {
        "email": "insert@example.com",
        "username": "test",
        "password": "test"
    }
    response = client.post("/auth/add_user", json=data)
    assert response.status_code == 200

    user_id = await data_access.UserAccess.get_user_id_email(
        email="insert@example.com"
    )

    planet_id = await data_access.PlanetAccess.create_planet("test", "arctic", 1, 1)

    army_id = await data_access.ArmyAccess.create_army(user_id, planet_id, 0, 0)
    await data_access.commit()

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
