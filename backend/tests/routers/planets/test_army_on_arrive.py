from src.app.database.database_access.data_access import DataAccess
from src.app.database.database import sessionmanager


async def test_attack_army(client, data_access: DataAccess):
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
    await data_access.PlanetAccess.create_planet_region(planet_id, "arctic", 0, 0)

    army_id = await data_access.ArmyAccess.create_army(user_id, planet_id, 0, 0)

    """
    Create second user
    """
    user_2 = await data_access.UserAccess.create_user("a", "a", "a")
    army2_id = await data_access.ArmyAccess.create_army(user_2, planet_id, 0, 0)

    army3_id = await data_access.ArmyAccess.create_army(user_id, planet_id, 0, 0)

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
            "to_x": 0,
            "to_y": 0,
            "on_arrive": True,
            "target_type": "attack_army",
            "target_id": army2_id

        })

        data = websocket.receive_json()

        """
        Check the websocket reload request
        """

        data = websocket.receive_json()
        assert data["request_type"] == "reload"

        c_id = await data_access.CityAccess.create_city(planet_id, user_2, 0, 0)
        await data_access.commit()

        websocket.send_json({
            "type": "change_direction",
            "army_id": army3_id,
            "to_x": 0.000001,
            "to_y": 0,
            "on_arrive": True,
            "target_type": "attack_city",
            "target_id": c_id

        })

        """
        Check the websocket reload request
        """
        data = websocket.receive_json()

        data = websocket.receive_json()
        assert data["request_type"] == "reload"


