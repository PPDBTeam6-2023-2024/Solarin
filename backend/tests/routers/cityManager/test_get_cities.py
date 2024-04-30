
import pytest

from src.app.database.database import sessionmanager
from src.app.database.database_access.data_access import DataAccess
async def test_get_cities(client, data_access: DataAccess):

    data = {
        "email": "test@example.com",
        "username": "test",
        "password": "test"
    }
    response = client.post("/auth/add_user", json=data)
    assert response.status_code == 200

    user_id = await data_access.UserAccess.get_user_id_email(
        email="test@example.com"
    )

    sregion_id = await data_access.PlanetAccess.create_space_region("test_region")
    planet_id = await data_access.PlanetAccess.create_planet("test_planet", "arctic", sregion_id)
    await data_access.PlanetAccess.create_planet_region(planet_id, "arctic", 0,0)

    c_id = await data_access.CityAccess.create_city(planet_id, user_id, 0, 0)

    await data_access.commit()

    response = client.get(f"/cityManager/cities/{c_id}")

    assert response.status_code == 200


async def test_upgrade_cities(client,  data_access: DataAccess):

    data = {
        "email": "upgrade_test@example.com",
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

    user_id = await data_access.UserAccess.get_user_id_email(
        email="upgrade_test@example.com"
    )

    body = response.json()
    assert body["token_type"] == "bearer"
    token = body["access_token"]

    headers = {
        'Authorization': f"Bearer {token}",
        "content-type": "application/x-www-form-urlencoded",
        "accept": "application/json"
    }

    sregion_id = await data_access.PlanetAccess.create_space_region("upgrade_test_region")
    planet_id = await data_access.PlanetAccess.create_planet("upgrade_test_planet", "arctic", sregion_id)
    await data_access.PlanetAccess.create_planet_region(planet_id, "arctic", 0, 0)

    initial_POP_resource_amount: int = 100000
    initial_SOL_resource_amount: int = 100000
    await data_access.ResourceAccess.add_resource(user_id,"POP",100000)
    await data_access.ResourceAccess.add_resource(user_id,"SOL",100000)

    c_id = await data_access.CityAccess.create_city(planet_id, user_id, 0, 0)

    await data_access.commit()

    response = client.post(f"/cityManager/upgrade_city/{c_id}", headers=headers)

    assert response.status_code == 200

    """
    Check if user resources decreased due to upgrade
    """
    current_POP_resource_amount = await data_access.ResourceAccess.get_resource_amount(user_id, "POP")
    current_SOL_resource_amount = await data_access.ResourceAccess.get_resource_amount(user_id, "SOL")

    assert current_POP_resource_amount < initial_POP_resource_amount
    assert current_SOL_resource_amount < initial_SOL_resource_amount

    """
    check that the upgrade was initiated and an update time greater than 0 was set
    """
    remaining_update_time = await data_access.CityAccess.get_remain_update_time(city_id=c_id)

    assert remaining_update_time > 0

    headers = {'Authorization': f"Bearer {token}",
               "content-type": "application/x-www-form-urlencoded",
               "accept": "application/json"
               }

async def test_get_resource_stocks(client, data_access: DataAccess):

    """
    Register and authenticate a new user
    """
    data = {
        "email": "resource_test@example.com",
        "username": "test",
        "password": "test"
    }
    response = client.post("/auth/add_user", json=data)
    assert response.status_code == 200

    """
    Get token for the test user
    """
    headers = {
        "content-type": "application/x-www-form-urlencoded",
        "accept": "application/json",
    }
    response = client.post("/auth/token", data=data, headers=headers)
    assert response.status_code == 200

    body = response.json()
    assert body["token_type"] == "bearer"
    token = body["access_token"]

    """
    Prepare headers with the token for authorized requests
    """
    headers = {
        'Authorization': f"Bearer {token}",
        "content-type": "application/x-www-form-urlencoded",
        "accept": "application/json"
    }

    """
    Create necessary city and planet for the test
    """
    user_id = await data_access.UserAccess.get_user_id_email(email="resource_test@example.com")
    sregion_id = await data_access.PlanetAccess.create_space_region("resource_test_region")
    planet_id = await data_access.PlanetAccess.create_planet("resource_test_planet", "arctic", sregion_id)
    await data_access.PlanetAccess.create_planet_region(planet_id, "arctic", 0, 0)
    c_id = await data_access.CityAccess.create_city(planet_id, user_id, 0, 0)
    await data_access.commit()

    """
    create productionBuilding in city
    """
    await data_access.BuildingAccess.create_building(user_id, c_id,"nexus",True)
    await data_access.commit()

    """
    Fetch the resource stocks of the city
    """
    response = client.get(f"/cityManager/get_resource_stocks/{c_id}", headers=headers)
    assert response.status_code == 200

    """
    Parse the response to check the contents
    """
    resource_data = response.json()
    assert 'overview' in resource_data
    overview = resource_data['overview']

    """
    Verify if the response contains some resource stocks
    """
    resource_found = False
    for stocks in overview.values():
        for stock in stocks:
            if len(stock) > 0:
                resource_found = True

    assert resource_found, "No resources found in city storage."


