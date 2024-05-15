import json

from src.app.database.database_access.data_access import DataAccess
from src.app.database.database import sessionmanager


async def test_general_actions(client, data_access: DataAccess):
    data = {
        "email": "insert@example.com",
        "username": "test",
        "password": "test"
    }
    response = client.post("/auth/add_user", json=data)
    assert response.status_code == 200

    headers = {
        "content-type": "application/x-www-form-urlencoded",
        "accept": "application/json",
    }
    response = client.post("/auth/token", data=data, headers=headers)
    assert response.status_code == 200

    body = response.json()
    assert body["token_type"] == "bearer"
    token = body["access_token"]

    headers = {"Authorization": f"Bearer {token}", "content-type": "application/x-www-form-urlencoded",
        "accept": "application/json"}

    user_id = await data_access.UserAccess.get_user_id_email(
        email="insert@example.com"
    )

    planet_id = await data_access.PlanetAccess.create_planet("test", "arctic", 1, 1)
    await data_access.PlanetAccess.create_planet_region(planet_id, "arctic", 0, 0)

    army_id = await data_access.ArmyAccess.create_army(user_id, planet_id, 0, 0)
    await data_access.commit()

    response = client.get("/general/available_generals", headers=headers)
    assert len(response.json()) == 8

    data = {"army_id": army_id, "general_name": "brave"}
    data = json.dumps(data)

    response = client.post("/general/add_general", data=data, headers=headers)

    response = client.get("/general/available_generals", headers=headers)
    assert len(response.json()) == 7

    data = {"army_id": army_id}
    data = json.dumps(data)

    response = client.post("/general/remove_general", data=data, headers=headers)

    response = client.get("/general/available_generals", headers=headers)
    assert len(response.json()) == 8





