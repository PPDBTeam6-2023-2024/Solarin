from src.app.database.database_access.data_access import DataAccess
from src.app.database.database import sessionmanager


async def test_attack_army(client):
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

    async with sessionmanager.session() as session:
        data_access = DataAccess(session)

        user_id = await data_access.UserAccess.get_user_id_email(
            email="insert@example.com"
        )

        sregion_id = await data_access.PlanetAccess.create_space_region("test")
        await data_access.DeveloperAccess.create_planet_type("arctic")
        planet_id = await data_access.PlanetAccess.create_planet("test", "arctic", sregion_id)
        await data_access.DeveloperAccess.create_planet_region_type("test")
        await data_access.PlanetAccess.create_planet_region(planet_id, "test", 0, 0)

        army_id = await data_access.ArmyAccess.create_army(user_id, planet_id, 0, 0)

        """
        Create city and set army inside city
        """
        c_id = await data_access.CityAccess.create_city(planet_id, user_id, 0, 0)
        await data_access.ArmyAccess.enter_city(c_id, army_id)

        await session.commit()

        headers = {'Authorization': f"Bearer {token}",
                   "content-type": "application/x-www-form-urlencoded",
                   "accept": "application/json"
                   }

        response2 = client.post(f"/army/leave_city/{army_id}", headers=headers)
        r = response2.json()
        assert r["success"]




