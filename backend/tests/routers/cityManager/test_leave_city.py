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

    headers = {
        "content-type": "application/x-www-form-urlencoded",
        "accept": "application/json",
    }
    response = client.post("/auth/token", data=data, headers=headers)
    assert response.status_code == 200

    body = response.json()
    assert body["token_type"] == "bearer"
    token = body["access_token"]


    user_id = await data_access.UserAccess.get_user_id_email(
        email="insert@example.com"
    )

    sregion_id = await data_access.PlanetAccess.create_space_region("test")
    planet_id = await data_access.PlanetAccess.create_planet("test", "arctic", sregion_id, 1, 1)
    await data_access.PlanetAccess.create_planet_region(planet_id, "arctic", 0, 0)

    army_id = await data_access.ArmyAccess.create_army(user_id, planet_id, 0, 0)

    """
    Create city and set army inside city
    """
    c_id = await data_access.CityAccess.create_city(planet_id, user_id, 0, 0)
    await data_access.ArmyAccess.enter_city(c_id, army_id)

    await data_access.commit()

    headers = {'Authorization': f"Bearer {token}",
                "content-type": "application/x-www-form-urlencoded",
                "accept": "application/json"
                }





