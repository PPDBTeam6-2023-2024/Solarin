import pytest

from src.app.database.database import sessionmanager
from src.app.database.database_access.data_access import DataAccess
from src.app.database.models import *
from sqlalchemy import inspect
from ...src.logic.combat.ArriveCheck import *

@pytest.fixture(scope="function", autouse=True)
async def insert_test_data(connection_test):
    async with sessionmanager.connect() as connection:
        # we use our own test types not the tuples
        await sessionmanager.drop_all(connection)
        await sessionmanager.create_all(connection)

    async with sessionmanager.session() as session:
        """
        setup database data that can be queried
        """
        da = DataAccess(session)

        """
        add default resources
        """
        await da.DeveloperAccess.create_resource_type("Vibranium")
        await da.DeveloperAccess.create_resource_type("Energon")
        await da.DeveloperAccess.create_resource_type("SOL")
        await da.DeveloperAccess.create_resource_type("TF")
        await da.DeveloperAccess.create_resource_type("RA")

        await da.DeveloperAccess.create_stat("attack")
        await da.DeveloperAccess.create_stat("defense")
        await da.DeveloperAccess.create_stat("city_attack")
        await da.DeveloperAccess.create_stat("city_defense")
        await da.DeveloperAccess.create_stat("recovery")
        await da.DeveloperAccess.create_stat("speed")

        await da.DeveloperAccess.create_political_stance("anarchism")
        await da.DeveloperAccess.create_political_stance("authoritarian")
        await da.DeveloperAccess.create_political_stance("democratic")
        await da.DeveloperAccess.create_political_stance("corporate_state")
        await da.DeveloperAccess.create_political_stance("theocracy")
        await da.DeveloperAccess.create_political_stance("technocracy")

        """
        Creates 50 users
        """

        for t_index in range(50):
            uuid = await da.UserAccess.create_user(f"username{t_index}", f"t{t_index}@gmail", f"hp{t_index}")
            assert uuid == t_index + 1

        await da.commit()

        """
        Creates friendship so that the first 20 are all friends with each other
        """
        for t_index in range(20):
            for t2_index in range(t_index, 20):
                if t_index == t2_index:
                    continue

                await da.UserAccess.add_friendship(t_index + 1, t2_index + 1)

        """
        Create clan and add the ClanOwner to the clan
        """
        for t_index in range(1, 51, 2):
            await da.AllianceAccess.create_alliance(f"{t_index} his clan")
            await da.AllianceAccess.set_alliance(t_index, f"{t_index} his clan")
            await da.AllianceAccess.set_alliance(t_index + 1, f"{t_index} his clan")

        await da.commit()

        """
        Send messages inside each alliance
        """
        for times in range(21):
            for t_index in range(1, 51, 2):
                mb = await da.MessageAccess.get_alliance_message_board(f"{t_index} his clan")

                m_token = MessageToken(
                    sender_id=t_index,
                    message_board=mb,
                    body="test"
                )

                mid = await da.MessageAccess.create_message(m_token)

                m_token2 = MessageToken(
                    sender_id=t_index + 1,
                    message_board=mb,
                    body="test reply"
                )

                await da.MessageAccess.create_message(m_token2)

        """
        send 5 DM's
        user 1 to user 2
        user 3 to user 4
        ...
        user 9 to user 10
        """
        for t_index in range(1, 11, 2):
            mb = await da.MessageAccess.get_player_messageBoard(t_index, t_index + 1)
            m_token3 = MessageToken(
                sender_id=t_index,
                message_board=mb,
                body="test2"
            )

            await da.MessageAccess.create_message(m_token3)

        """
        create some testing planets
        """
        await da.DeveloperAccess.create_planet_type("Shadow planet", "planet where it is hard to see")
        p_id = await da.PlanetAccess.create_planet("Umbara", "Shadow planet", 1, 1)
        await da.DeveloperAccess.create_planet_region_type("valley of death", "Ooh.. very scary")
        r_id = await da.PlanetAccess.create_planet_region(p_id, "valley of death", 0, 0)
        c_id = await da.CityAccess.create_city(r_id, 20, 0.2, 0.8)
        c_id2 = await da.CityAccess.create_city(r_id, 1, 0.8, 0.2)

        """
        Create some types of buildings and resources
        """
        await da.DeveloperAccess.create_production_building_type("The mines of moria")
        await da.DeveloperAccess.create_barracks_type("Kamino training complex")
        await da.DeveloperAccess.create_tower_type("towerH", 50)
        await da.DeveloperAccess.create_house_type("Solarin mansion", 50)
        await da.DeveloperAccess.create_wall_type("wallW", 50)

        await da.DeveloperAccess.set_produces_resources("The mines of moria", "Vibranium", 100, 2000)

        await da.DeveloperAccess.set_creation_cost("Solarin mansion", [("Vibranium", 2022), ("Energon", 22)])
        await da.DeveloperAccess.set_creation_cost("Kamino training complex", [("Vibranium", 1)])
        await da.DeveloperAccess.set_creation_cost("Kamino training complex", [("Energon", 2)])

        await da.DeveloperAccess.set_creation_cost("The mines of moria", [("TF", 100)])
        await da.DeveloperAccess.set_creation_cost("towerH", [("TF", 100)])
        await da.DeveloperAccess.set_creation_cost("wallW", [("TF", 100)])


        await da.ResourceAccess.add_resource(1, "TF", 10000)
        await da.ResourceAccess.add_resource(20, "TF", 10000)
        await da.ResourceAccess.add_resource(1, "Vibranium", 10000)
        await da.ResourceAccess.add_resource(20, "Vibranium", 10000)
        await da.ResourceAccess.add_resource(1, "Energon", 10000)
        await da.ResourceAccess.add_resource(20, "Energon", 10000)

        """
        Create some actual buildings instances inside cities
        """
        await da.BuildingAccess.create_building(20, c_id, "The mines of moria")
        b_id = await da.BuildingAccess.create_building(20, c_id, "Kamino training complex")
        await da.BuildingAccess.create_building(20, c_id, "Solarin mansion")

        await da.BuildingAccess.create_building(1, c_id2, "The mines of moria")
        b_id2 = await da.BuildingAccess.create_building(1, c_id2, "Kamino training complex")
        await da.BuildingAccess.create_building(1, c_id2, "Solarin mansion")

        await da.BuildingAccess.create_building(20, c_id, "towerH")
        await da.BuildingAccess.create_building(20, c_id, "wallW")

        """
        create some types of troops
        """

        a_id = await da.ArmyAccess.create_army(user_id=1, planet_id=p_id, x=0, y=0)

        a_id2 = await da.ArmyAccess.create_army(user_id=20, planet_id=p_id, x=0, y=0)

        await da.DeveloperAccess.create_troop_type("tank", timedelta(hours=4),
                                                   BattleStats(attack=5, defense=50, city_attack=1, city_defense=120,
                                                            recovery=5, speed=0.4))

        await da.DeveloperAccess.create_troop_type("soldier", timedelta(hours=4, minutes=5),
                                                   BattleStats(attack=30, defense=30, city_attack=30, city_defense=20,
                                                            recovery=5, speed=0.9))

        await da.DeveloperAccess.set_troop_type_cost("tank", [("Vibranium", 20), ("Energon", 2)])
        await da.DeveloperAccess.set_troop_type_cost("soldier", [("Vibranium", 5)])

        """
        add some troops to an army
        """
        await da.ArmyAccess.add_to_army(a_id, "tank", 2, 20)
        await da.ArmyAccess.add_to_army(a_id, "tank", 2, 10)
        await da.ArmyAccess.add_to_army(a_id, "tank", 3, 10)

        await da.ArmyAccess.add_to_army(a_id2, "soldier", 3, 10)

        """
        start training units
        """

        await da.TrainingAccess.train_type(b_id, "tank", 3, 10)
        await da.TrainingAccess.train_type(b_id, "tank", 3, 10)
        await da.TrainingAccess.train_type(b_id2, "tank", 3, 10)
        await da.TrainingAccess.train_type(b_id2, "tank", 3, 10)

        await da.commit()

        yield


async def test_check_messages():
    """
    test case for accessing messages
    """
    async with sessionmanager.session() as session:
        da = DataAccess(session)

        """
        access and verify alliance messages
        """
        for i in range(100):
            m1 = await da.MessageAccess.get_messages_alliance(f"{1} his clan", 0, 20)
            assert len(m1) == 20

        for t_index in range(1, 51, 2):
            m1 = await da.MessageAccess.get_messages_alliance(f"{t_index} his clan", 1, 2)
            m2 = await da.MessageAccess.get_messages_alliance(f"{t_index} his clan", 0, 1)
            assert len(m1) == 2
            assert len(m2) == 1
            assert m1[0].body == "test reply"
            assert m1[1].body == "test"
            assert m2[0].body == "test reply"

        """
        access and verify DM messages
        """
        for t_index in range(1, 11, 2):
            messages = await da.MessageAccess.get_messages_player(t_index, t_index + 1, 0, 1)

            assert len(messages) == 1
            assert messages[0].body == "test2"


async def test_friendship_relations():
    """
    check if the friendship relations are properly working
    """
    async with sessionmanager.session() as session:
        da = DataAccess(session)

        for t_index in range(20):
            friends = await da.UserAccess.get_friends(t_index + 1)
            assert len(friends) == 19
            for f in friends:
                assert 0 < f[0] <= 20
                assert f[0] != t_index+1


async def test_alliance_members():
    """
    check that people are correctly part of the right alliance
    """
    async with sessionmanager.session() as session:
        da = DataAccess(session)
        for t_index in range(1, 51, 2):
            members = await da.AllianceAccess.get_alliance_members(f"{t_index} his clan")
            assert len(members) == 2
            for m in members:
                assert m.email in (f"t{t_index-1}@gmail", f"t{t_index}@gmail")


async def test_planet():
    """
    check that the planet info is correct
    """
    async with sessionmanager.session() as session:
        da = DataAccess(session)

        regions = await da.PlanetAccess.get_regions(1)
        assert len(regions) == 1
        assert regions[0].id == 1

        cities = await da.PlanetAccess.get_planet_cities(1)
        assert len(cities) == 2
        assert cities[0].id == 1
        assert cities[0].controlled_by == 20
        assert cities[0].x == 0.2
        assert cities[0].y == 0.8
        assert cities[1].x == 0.8
        assert cities[1].y == 0.2


async def test_buildings():
    """
    check if the buildings are correctly created and accessed
    """
    async with sessionmanager.session() as session:
        da = DataAccess(session)

        bt = await da.BuildingAccess.get_building_types()
        assert len(bt) == 5
        assert (bt[0].name, bt[0].type) == ('The mines of moria', 'productionBuilding')
        assert (bt[1].name, bt[1].type) == ('Kamino training complex', 'Barracks')
        assert (bt[2].name, bt[2].type) == ('towerH', 'tower')
        assert (bt[3].name, bt[3].type) == ('Solarin mansion', 'house')

        cbt = await da.BuildingAccess.get_city_buildings(1)
        assert len(cbt) == 5
        assert (cbt[0].type.name, cbt[0].type.type) == ('The mines of moria', 'productionBuilding')
        assert (cbt[1].type.name, cbt[1].type.type) == ('Kamino training complex', 'Barracks')
        assert (cbt[2].type.name, cbt[2].type.type) == ('Solarin mansion', 'house')

        assert cbt[0].id == 1
        assert cbt[1].id == 2
        assert cbt[2].id == 3


async def test_DM_overview():
    async with sessionmanager.session() as session:
        da = DataAccess(session)
        r = await da.MessageAccess.get_friend_message_overview(1)
        assert len(r) == 1
        assert r[0][0] == "username1"


async def test_friend_requests():
    async with sessionmanager.session() as session:
        da = DataAccess(session)
        await da.UserAccess.send_friend_request(1, 40)
        await da.UserAccess.send_friend_request(1, 41)
        await da.UserAccess.send_friend_request(40, 41)

        await da.commit()
        with pytest.raises(Exception):
            """
            expected to throw exceptions
            """
            await da.UserAccess.send_friend_request(1, 40)

        await da.rollback()

        with pytest.raises(Exception):
            """
            expected to throw exceptions
            """
            await da.UserAccess.send_friend_request(1, 2)

        await da.rollback()

        await da.UserAccess.accept_friend_request(1, 40)

        friends = await da.UserAccess.get_friends(1)

        """
        verify that 40 is amongs friends
        """
        found_friend = False
        for friend, board in friends:
            if friend == 40:
                found_friend = True
                break

        assert found_friend == True

        r = await da.UserAccess.get_friend_requests(41)
        assert len(r) == 2


async def test_ranking():
    """
    test ranking
    """
    async with sessionmanager.session() as session:
        da = DataAccess(session)
        ranking = await da.RankingAccess.get_top_ranking(10)
        assert len(ranking) == 10
        assert ranking[0][0] == "username1"
        assert ranking[9][0] == "username0"


async def test_training():
    """
    test training
    """
    async with sessionmanager.session() as session:
        da = DataAccess(session)
        await da.TrainingAccess.check_queue(2, 11.5*14400)

        after_queues = await da.TrainingAccess.get_queue(2)
        assert len(after_queues) == 1
        assert after_queues[0][1] == 14400

        """
        assert for remaining time
        """
        assert after_queues[0][0].train_remaining == 122400
        assert after_queues[0][0].training_size == 9

        army_in_city = await da.ArmyAccess.get_army_in_city(1)

        army_troops = await da.ArmyAccess.get_troops(army_in_city)

        assert len(army_troops) == 1

        """
        check troops other rank are the same
        """
        assert army_troops[0].size == 11
        assert army_troops[0].rank == 3


async def test_troop_rank():
    """
    test that troop ank works correctly
    """
    async with sessionmanager.session() as session:
        da = DataAccess(session)

        """
        Tests that retrieving and upgrading unit ranks occurs correctly
        """
        rank = await da.TrainingAccess.get_troop_rank(1, "soldier")
        assert rank == 1

        cost_list = await da.TrainingAccess.get_troop_cost(1, "soldier")
        assert len(cost_list) == 1
        assert cost_list[0][0] == "Vibranium"
        assert cost_list[0][1] == 5

        await da.TrainingAccess.upgrade_troop_rank(1, "soldier")

        rank = await da.TrainingAccess.get_troop_rank(1, "soldier")
        assert rank == 2

        rank = await da.TrainingAccess.get_troop_rank(2, "soldier")
        assert rank == 1

        rank = await da.TrainingAccess.get_troop_rank(1, "medic")
        assert rank == 1

        cost_list = await da.TrainingAccess.get_troop_cost(1, "soldier")
        assert len(cost_list) == 1
        assert cost_list[0][0] == "Vibranium"
        assert cost_list[0][1] == 5


async def test_attack_store():
    async with sessionmanager.session() as session:
        da = DataAccess(session)

        """
        We are not yet attacking anything
        """
        going_to_attack = await da.ArmyAccess.will_on_arrive(1)
        assert going_to_attack is None

        """
        Army 1 will attack army 2
        """
        await da.ArmyAccess.attack_army(1, 2)

        going_to_attack = await da.ArmyAccess.will_on_arrive(1)
        assert going_to_attack.target_id == 2

        going_to_attack = await da.ArmyAccess.will_on_arrive(2)
        assert going_to_attack is None

        """
        Cancel attack and check if properly removed
        """
        await da.ArmyAccess.cancel_attack(1)
        going_to_attack = await da.ArmyAccess.will_on_arrive(1)
        assert going_to_attack is None

        """
        Let an army attack a city
        """
        await da.ArmyAccess.attack_city(1, 1)

        going_to_attack = await da.ArmyAccess.will_on_arrive(1)
        assert going_to_attack.target_id == 1

        """
        Cancel attack and check if properly removed
        """
        await da.ArmyAccess.cancel_attack(1)
        going_to_attack = await da.ArmyAccess.will_on_arrive(1)
        assert going_to_attack is None

        await da.ArmyAccess.get_army_stats(1)


async def test_army_combat():
    """
    Test combat between 2 armies
    """

    async with sessionmanager.session() as session:
        da = DataAccess(session)

        a1 = await da.ArmyAccess.get_army_by_id(1)
        a2 = await da.ArmyAccess.get_army_by_id(2)

        assert a1 is not None
        assert a2 is not None

        await da.ArmyAccess.attack_army(1, 2)

        suc6 = await ArriveCheck.check_arrive(1, da)
        assert suc6

        a1 = await da.ArmyAccess.get_army_by_id(1)
        a2 = await da.ArmyAccess.get_army_by_id(2)

        assert a1 is None or a2 is None


async def test_city_combat():
    """
    Test combat between an army and a city
    """
    async with sessionmanager.session() as session:
        da = DataAccess(session)

        owner = await da.CityAccess.get_city_controller(1)
        assert owner.id == 20

        await da.ArmyAccess.enter_city(1, 2)

        await da.ArmyAccess.attack_city(1, 1)

        suc6 = await ArriveCheck.check_arrive(1, da)
        assert suc6

        owner = await da.CityAccess.get_city_controller(1)
        assert owner.id == 1

        army = await da.ArmyAccess.get_army_by_id(1)
        troops = await da.ArmyAccess.get_troops(1)

        assert army is not None
        assert len(troops) > 0
