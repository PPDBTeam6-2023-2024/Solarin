from datetime import timedelta

from tests.conftest import client

from src.app.database.database import sessionmanager
from src.app.database.database_access.data_access import DataAccess

from backend.src.app.routers.authentication.schemas import BattleStats


async def test_get_armies(client):
    async with sessionmanager.session() as session:
        data_access = DataAccess(session)

        data = {
            "email": "test@example.com",
            "username": "test",
            "password": "test"
        }
        response = client.post("/auth/add_user", json=data)
        assert response.status_code == 200

        await data_access.DeveloperAccess.createPlanetType("test_planet_type")
        await data_access.DeveloperAccess.createPlanetRegionType("test_region_type")
        await data_access.DeveloperAccess.createAssociatedWith("test_planet_type", "test_region_type")
        await session.commit()

        space_region_id = await data_access.PlanetAccess.createSpaceRegion("test_space_region")
        region_id = await data_access.PlanetAccess.createSpaceRegion("test_region")
        planet_id = await data_access.PlanetAccess.createPlanet("test_planet", "test_planet_type", space_region_id)

        user_id = await data_access.UserAccess.getUserIdEmail(
            email="test@example.com"
        )

        await data_access.ArmyAccess.create_army(user_id, planet_id, 0.25, 0.25)
        await data_access.ArmyAccess.create_army(user_id, planet_id, 0.75, 0.75)
        await session.commit()
    response = client.get("/army/armies", params={"planet_id": 1})
    assert response.status_code == 200


async def test_get_troops(client):
    async with sessionmanager.session() as session:
        data_access = DataAccess(session)

        data = {
            "email": "test@example.com",
            "username": "test",
            "password": "test"
        }
        response = client.post("/auth/add_user", json=data)
        assert response.status_code == 200

        await data_access.DeveloperAccess.createPlanetType("test_planet_type")
        await data_access.DeveloperAccess.createPlanetRegionType("test_region_type")
        await data_access.DeveloperAccess.createAssociatedWith("test_planet_type", "test_region_type")
        await session.commit()

        space_region_id = await data_access.PlanetAccess.createSpaceRegion("test_space_region")
        region_id = await data_access.PlanetAccess.createSpaceRegion("test_region")
        planet_id = await data_access.PlanetAccess.createPlanet("test_planet", "test_planet_type", space_region_id)



        user_id = await data_access.UserAccess.getUserIdEmail(
            email="test@example.com"
        )

        army_id = await data_access.ArmyAccess.create_army(user_id, planet_id, 0.25, 0.25)

        battle_stats_soldier = BattleStats(
            attack=15,
            defense=5,
            city_attack=10,
            city_defense=4,
            recovery=3,
            speed=10.0
        )

        battle_stats_brute = BattleStats(
            attack=25,
            defense=20,
            city_attack=20,
            city_defense=15,
            recovery=5,
            speed=5.0
        )

        await data_access.DeveloperAccess.createToopType(
            type_name="Soldier",
            training_time=timedelta(hours=2),
            battle_stats=battle_stats_soldier,
            required_rank=2
        )

        await data_access.DeveloperAccess.createToopType(
            type_name="Brute",
            training_time=timedelta(hours=8),
            battle_stats=battle_stats_brute,
            required_rank=3
        )

        await data_access.ArmyAccess.add_to_army(army_id, "Soldier", 1, 20)
        await data_access.ArmyAccess.add_to_army(army_id, "Brute", 2, 40)

        await session.commit()

    response = client.get("/army/troops", params={"armyid": army_id})
    assert response.status_code == 200

