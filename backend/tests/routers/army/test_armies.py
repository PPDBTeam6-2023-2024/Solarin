from datetime import timedelta

from src.app.database.database import sessionmanager
from src.app.database.database_access.data_access import DataAccess

from src.app.routers.authentication.schemas import BattleStats


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

        await data_access.DeveloperAccess.create_planet_type("test_planet_type")
        await data_access.DeveloperAccess.create_planet_region_type("test_region_type")
        await data_access.DeveloperAccess.create_associated_with("test_planet_type", "test_region_type")
        await session.commit()

        planet_id = await data_access.PlanetAccess.create_planet("test_planet", "test_planet_type", 1, 1)

        user_id = await data_access.UserAccess.get_user_id_email(
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

        await data_access.DeveloperAccess.create_planet_type("test_planet_type")
        await data_access.DeveloperAccess.create_planet_region_type("test_region_type")
        await data_access.DeveloperAccess.create_associated_with("test_planet_type", "test_region_type")
        await session.commit()

        planet_id = await data_access.PlanetAccess.create_planet("test_planet", "test_planet_type", 1, 1)



        user_id = await data_access.UserAccess.get_user_id_email(
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

        await data_access.DeveloperAccess.create_troop_type(
            type_name="Soldier",
            training_time=timedelta(hours=2),
            battle_stats=battle_stats_soldier,
            required_rank=2
        )

        await data_access.DeveloperAccess.create_troop_type(
            type_name="Brute",
            training_time=timedelta(hours=8),
            battle_stats=battle_stats_brute,
            required_rank=3
        )

        await data_access.ArmyAccess.add_to_army(army_id, "Soldier", 1, 20)
        await data_access.ArmyAccess.add_to_army(army_id, "Brute", 2, 40)

        await session.commit()

    response = client.get(f"/army/troops/{army_id}")
    assert response.status_code == 401


async def test_split_army(client):
    async with sessionmanager.session() as session:
        data_access = DataAccess(session)

        # Setup test data
        data = {
            "email": "test@example.com",
            "username": "test",
            "password": "test"
        }
        response = client.post("/auth/add_user", json=data)
        assert response.status_code == 200

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
        token = body["access_token"]

        headers = {'Authorization': f"Bearer {token}"}
        response = client.get("/auth/validate", headers=headers)


        await data_access.DeveloperAccess.create_planet_type("test_planet_type")
        await data_access.DeveloperAccess.create_planet_region_type("test_region_type")
        await data_access.DeveloperAccess.create_associated_with("test_planet_type", "test_region_type")
        await session.commit()

        user_id = await data_access.UserAccess.get_user_id_email(
            email="test@example.com"
        )
        planet_id = await data_access.PlanetAccess.create_planet("test_planet", "test_planet_type", 1, 1)

        army_id = await data_access.ArmyAccess.create_army(user_id, planet_id, 0.25, 0.55)

        battle_stats_infantry = BattleStats(
            attack=15,
            defense=5,
            city_attack=10,
            city_defense=4,
            recovery=3,
            speed=10.0
        )

        battle_stats_cavalry = BattleStats(
            attack=25,
            defense=20,
            city_attack=20,
            city_defense=15,
            recovery=5,
            speed=5.0
        )
        await data_access.DeveloperAccess.create_troop_type(
            type_name="Infantry",
            training_time=timedelta(hours=2),
            battle_stats=battle_stats_infantry,
            required_rank=1
        )

        await data_access.DeveloperAccess.create_troop_type(
            type_name="Cavalry",
            training_time=timedelta(hours=8),
            battle_stats=battle_stats_cavalry,
            required_rank=1
        )
        # Adding troops to the army
        await data_access.ArmyAccess.add_to_army(army_id, "Infantry",1, 50)
        await data_access.ArmyAccess.add_to_army(army_id, "Cavalry",1, 50)
        await session.commit()

        # Prepare split data
        split_data = {
            "to_split": [
                {"troop_type": "Infantry", "rank":1, "size": 50, "army_id": army_id}
            ]
        }
        await session.flush()
        await session.commit()

        # Call the split_army endpoint
        response = client.post(f"/army/split_army/{army_id}", headers=headers, json=split_data)

        # Assert the response
        assert response.status_code == 200
        new_army_id = response.json()
        assert isinstance(new_army_id, int)

