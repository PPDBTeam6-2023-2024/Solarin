
async def test_1(client, data_access):
    data = {
        "email": "insert@example.com",
        "username": "insert",
        "password": "unused"
    }
    response = client.post("/auth/add_user", json=data)
    assert response.status_code == 200

    userId = await data_access.UserAccess.get_user_id_email("insert@example.com")
    region_id = await data_access.PlanetAccess.create_space_region("test_region")
    await data_access.DeveloperAccess.create_planet_type("test_planet_type")
    planet_id = await data_access.PlanetAccess.create_planet("test_planet", "test_planet_type", region_id)
    await data_access.DeveloperAccess.create_planet_region_type("test_planet_region")
    region_id = await data_access.PlanetAccess.create_planet_region(planet_id, "test_planet_region", 0, 0)
    city_id = await data_access.CityAccess.create_city(planet_id, userId, 0, 0)
    planets = await data_access.PlanetAccess.get_planets_of_user(userId)

    assert len(planets) == 1
    assert planets[0].id == planet_id

async def test_2(client, data_access):
    data = {
        "email": "insert@example.com",
        "username": "insert",
        "password": "unused"
    }
    response = client.post("/auth/add_user", json=data)
    assert response.status_code == 200

    userId = await data_access.UserAccess.get_user_id_email("insert@example.com")
    region_id = await data_access.PlanetAccess.create_space_region("test_region")
    await data_access.DeveloperAccess.create_planet_type("test_planet_type")
    planet_id_1 = await data_access.PlanetAccess.create_planet("test_planet_1", "test_planet_type", region_id)
    planet_id_2 = await data_access.PlanetAccess.create_planet("test_planet_2", "test_planet_type", region_id)
    planet_id_3 = await data_access.PlanetAccess.create_planet("test_planet_3", "test_planet_type", region_id)
    await data_access.DeveloperAccess.create_planet_region_type("test_planet_region")
    region_id_1 = await data_access.PlanetAccess.create_planet_region(planet_id_1, "test_planet_region", 0, 0)
    region_id_2 = await data_access.PlanetAccess.create_planet_region(planet_id_2, "test_planet_region", 0, 0)
    region_id_3 = await data_access.PlanetAccess.create_planet_region(planet_id_3, "test_planet_region", 0, 0)
    city_id_1 = await data_access.CityAccess.create_city(planet_id_1, userId, 0, 0)
    city_id_2 = await data_access.CityAccess.create_city(planet_id_2, userId, 0, 0)
    city_id_3 = await data_access.CityAccess.create_city(planet_id_3, userId, 0, 0)
    planets = await data_access.PlanetAccess.get_planets_of_user(userId)
    assert len(planets) == 3
    assert planets[0].id == planet_id_1
    assert planets[1].id == planet_id_2
    assert planets[2].id == planet_id_3
