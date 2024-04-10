import pytest

from src.app.database.database import sessionmanager
from src.app.database.database_access.data_access import DataAccess
from src.app.database.models.models import *
from sqlalchemy import inspect
from ...src.logic.combat.ArmyCombat import *
from ...src.logic.combat.AttackCheck import *
@pytest.fixture(scope="function", autouse=True)
async def insert_test_data(connection_test):
    async with sessionmanager.session() as session:
        """
        setup database data that can be queried
        """
        da = DataAccess(session)

        """
        add default resources
        """
        await da.DeveloperAccess.createResourceType("Vibranium")
        await da.DeveloperAccess.createResourceType("Energon")
        await da.DeveloperAccess.createResourceType("SOL")
        """
        Creates 50 users
        """
        for t_index in range(50):
            uuid = await da.UserAccess.createUser(f"username{t_index}", f"t{t_index}@gmail", f"hp{t_index}")
            assert uuid == t_index + 1

        await da.commit()

        """
        Creates friendship so that the first 20 are all friends with each other
        """
        for t_index in range(20):
            for t2_index in range(t_index, 20):
                if t_index == t2_index:
                    continue

                await da.UserAccess.addFriendship(t_index + 1, t2_index + 1)

        """
        Create clan and add the ClanOwner to the clan
        """
        for t_index in range(1, 51, 2):
            await da.AllianceAccess.createAlliance(f"{t_index} his clan")
            await da.AllianceAccess.setAlliance(t_index, f"{t_index} his clan")
            await da.AllianceAccess.setAlliance(t_index + 1, f"{t_index} his clan")

        await da.commit()

        """
        Send messages inside each alliance
        """
        for times in range(21):
            for t_index in range(1, 51, 2):
                mb = await da.MessageAccess.getAllianceMessageBoard(f"{t_index} his clan")

                m_token = MessageToken(
                    sender_id=t_index,
                    message_board=mb,
                    body="test"
                )

                mid = await da.MessageAccess.createMessage(m_token)

                m_token2 = MessageToken(
                    sender_id=t_index + 1,
                    message_board=mb,
                    body="test reply"
                )

                await da.MessageAccess.createMessage(m_token2)

        """
        send 5 DM's
        user 1 to user 2
        user 3 to user 4
        ...
        user 9 to user 10
        """
        for t_index in range(1, 11, 2):
            mb = await da.MessageAccess.getPlayerMessageBoard(t_index, t_index + 1)
            m_token3 = MessageToken(
                sender_id=t_index,
                message_board=mb,
                body="test2"
            )

            await da.MessageAccess.createMessage(m_token3)

        """
        create some testing planets
        """
        sr_id = await da.PlanetAccess.createSpaceRegion("the expansion region")
        await da.DeveloperAccess.createPlanetType("Shadow planet", "planet where it is hard to see")
        p_id = await da.PlanetAccess.createPlanet("Umbara", "Shadow planet", sr_id)
        await da.DeveloperAccess.createPlanetRegionType("valley of death", "Ooh.. very scary")
        r_id = await da.PlanetAccess.createPlanetRegion(p_id, "valley of death", 0, 0)
        c_id = await da.CityAccess.createCity(r_id, 2, 0.2, 0.8)
        c_id2 = await da.CityAccess.createCity(r_id, 1, 0.8, 0.2)

        """
        Create some types of buildings and resources
        """
        await da.DeveloperAccess.createProductionBuildingType("The mines of moria")
        await da.DeveloperAccess.createBarracksType("Kamino training complex")
        await da.DeveloperAccess.createTowerType("towerH", 50)
        await da.DeveloperAccess.createHouseType("Solarin mansion", 50)
        await da.DeveloperAccess.createWallType("wallW", 50)

        await da.DeveloperAccess.setProducesResources("The mines of moria", "Vibranium", 100, 2000)

        await da.DeveloperAccess.setCreationCost("Solarin mansion", [("Vibranium", 2022), ("Energon", 22)])
        await da.DeveloperAccess.setCreationCost("Kamino training complex", [("Vibranium", 1)])
        await da.DeveloperAccess.setCreationCost("Kamino training complex", [("Energon", 2)])
        await da.DeveloperAccess.setCreationCost("The mines of moria", [("Energon", 2)])

        await da.DeveloperAccess.setCreationCost("towerH", [("Energon", 2)])
        await da.DeveloperAccess.setCreationCost("wallW", [("Energon", 2)])

        """
        Create some actual buildings instances inside cities
        """
        await da.BuildingAccess.createBuilding(c_id, "The mines of moria", 1)
        b_id = await da.BuildingAccess.createBuilding(c_id, "Kamino training complex", 1)
        await da.BuildingAccess.createBuilding(c_id, "Solarin mansion",1)

        await da.BuildingAccess.createBuilding(c_id2, "The mines of moria",2)
        b_id2 = await da.BuildingAccess.createBuilding(c_id2, "Kamino training complex",2)
        await da.BuildingAccess.createBuilding(c_id2, "Solarin mansion",2)

        await da.BuildingAccess.createBuilding(c_id, "towerH",1)
        await da.BuildingAccess.createBuilding(c_id, "wallW", 1)

        """
        create some types of troops
        """

        a_id = await da.ArmyAccess.createArmy(user_id=1, planet_id=p_id, x=0, y=0)

        a_id2 = await da.ArmyAccess.createArmy(user_id=3, planet_id=p_id, x=0, y=0)

        await da.DeveloperAccess.createToopType("tank", timedelta(hours=4),
                                                BattleStats(attack=5, defense=50, city_attack=1, city_defense=120,
                                                            recovery=5, speed=0.4))

        await da.DeveloperAccess.createToopType("soldier", timedelta(hours=4, minutes=5),
                                                BattleStats(attack=30, defense=30, city_attack=30, city_defense=20,
                                                            recovery=5, speed=0.9))

        await da.DeveloperAccess.setTroopTypeCost("tank", [("Vibranium", 20), ("Energon", 2)])
        await da.DeveloperAccess.setTroopTypeCost("soldier", [("Vibranium", 5)])

        """
        add some troops to an army
        """
        await da.ArmyAccess.addToArmy(a_id, "tank", 2, 20)
        await da.ArmyAccess.addToArmy(a_id, "tank", 2, 10)
        await da.ArmyAccess.addToArmy(a_id, "tank", 3, 10)

        await da.ArmyAccess.addToArmy(a_id2, "soldier", 3, 10)

        """
        start training units
        """
        await da.TrainingAccess.trainType(a_id, b_id, "tank", 3, 10)
        await da.TrainingAccess.trainType(a_id, b_id, "tank", 3, 10)
        await da.TrainingAccess.trainType(a_id, b_id2, "tank", 3, 10)
        await da.TrainingAccess.trainType(a_id, b_id2, "tank", 3, 10)

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
            m1 = await da.MessageAccess.getMessagesAlliance(f"{1} his clan", 0, 20)
            assert len(m1) == 20

        for t_index in range(1, 51, 2):
            m1 = await da.MessageAccess.getMessagesAlliance(f"{t_index} his clan", 1, 2)
            m2 = await da.MessageAccess.getMessagesAlliance(f"{t_index} his clan", 0, 1)
            assert len(m1) == 2
            assert len(m2) == 1
            assert m1[0][0].body == "test reply"
            assert m1[1][0].body == "test"
            assert m2[0][0].body == "test reply"

        """
        access and verify DM messages
        """
        for t_index in range(1, 11, 2):
            messages = await da.MessageAccess.getMessagesPlayer(t_index, t_index + 1, 0, 1)

            assert len(messages) == 1
            assert messages[0][0].body == "test2"


async def test_friendship_relations():
    """
    check if the friendship relations are properly working
    """
    async with sessionmanager.session() as session:
        da = DataAccess(session)

        for t_index in range(20):
            friends = await da.UserAccess.getFriends(t_index+1)
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
            members = await da.AllianceAccess.getAllianceMembers(f"{t_index} his clan")
            assert len(members) == 2
            for m in members:
                assert m.email in (f"t{t_index-1}@gmail", f"t{t_index}@gmail")


async def test_planet():
    """
    check that the planet info is correct
    """
    async with sessionmanager.session() as session:
        da = DataAccess(session)

        regions = await da.PlanetAccess.getRegions(1)
        assert len(regions) == 1
        assert regions[0].id == 1

        cities = await da.PlanetAccess.getPlanetCities(1)
        assert len(cities) == 2
        assert cities[0][0].id == 1
        assert cities[0][0].controlled_by == 2
        assert cities[0][0].x == 0.2
        assert cities[0][0].y == 0.8
        assert cities[1][0].x == 0.8
        assert cities[1][0].y == 0.2



async def test_buildings():
    """
    check if the buildings are correctly created and accessed
    """
    async with sessionmanager.session() as session:
        da = DataAccess(session)

        bt = await da.BuildingAccess.getBuildingTypes()
        assert len(bt) == 5
        assert (bt[0][0].name, bt[0][0].type) == ('The mines of moria', 'productionBuilding')
        assert (bt[1][0].name, bt[1][0].type) == ('Kamino training complex', 'Barracks')
        assert (bt[2][0].name, bt[2][0].type) == ('towerH', 'tower')
        assert (bt[3][0].name, bt[3][0].type) == ('Solarin mansion', 'house')

        cbt = await da.BuildingAccess.getCityBuildings(1)
        assert len(cbt) == 5
        assert (cbt[0][1].name, cbt[0][1].type) == ('The mines of moria', 'productionBuilding')
        assert (cbt[1][1].name, cbt[1][1].type) == ('Kamino training complex', 'Barracks')
        assert (cbt[2][1].name, cbt[2][1].type) == ('Solarin mansion', 'house')

        assert cbt[0][0].id == 1
        assert cbt[1][0].id == 2
        assert cbt[2][0].id == 3


async def test_DM_overview():
    async with sessionmanager.session() as session:
        da = DataAccess(session)
        r = await da.MessageAccess.getFriendMessageOverview(1)
        assert len(r) == 1
        assert r[0][0] == "username1"


async def test_friend_requests():
    async with sessionmanager.session() as session:
        da = DataAccess(session)
        await da.UserAccess.sendFriendRequest(1, 40)
        await da.UserAccess.sendFriendRequest(1, 41)
        await da.UserAccess.sendFriendRequest(40, 41)

        await da.commit()
        with pytest.raises(Exception):
            """
            expected to throw exceptions
            """
            await da.UserAccess.sendFriendRequest(1, 40)

        await da.rollback()

        with pytest.raises(Exception):
            """
            expected to throw exceptions
            """
            await da.UserAccess.sendFriendRequest(1, 2)

        await da.rollback()

        await da.UserAccess.acceptFriendRequest(1, 40)

        friends = await da.UserAccess.getFriends(1)

        """
        verify that 40 is amongs friends
        """
        found_friend = False
        for friend, board in friends:
            if friend == 40:
                found_friend = True
                break

        assert found_friend == True

        r = await da.UserAccess.getFriendRequests(41)
        assert len(r) == 2


async def test_ranking():
    """
    test ranking
    """
    async with sessionmanager.session() as session:
        da = DataAccess(session)
        ranking = await da.RankingAccess.getTopRanking(10)
        assert len(ranking) == 10
        assert ranking[0][0] == "username0"
        assert ranking[9][0] == "username9"


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

        army_troops = await da.ArmyAccess.getTroops(1)
        assert len(army_troops) == 2

        """
        check troops other rank are the same
        """
        assert army_troops[0][0].size == 30
        assert army_troops[0][0].rank == 2

        """
        check 11 troops are added
        """
        assert army_troops[1][0].size == 10+11
        assert army_troops[1][0].rank == 3


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
        going_to_attack = await da.ArmyAccess.will_attack(1)
        assert going_to_attack is None

        """
        Army 1 will attack army 2
        """
        await da.ArmyAccess.attack_army(1, 2)

        going_to_attack = await da.ArmyAccess.will_attack(1)
        assert going_to_attack.target_id == 2

        going_to_attack = await da.ArmyAccess.will_attack(2)
        assert going_to_attack is None

        """
        Cancel attack and check if properly removed
        """
        await da.ArmyAccess.cancel_attack(1)
        going_to_attack = await da.ArmyAccess.will_attack(1)
        assert going_to_attack is None

        """
        Let an army attack a city
        """
        await da.ArmyAccess.attack_city(1, 1)

        going_to_attack = await da.ArmyAccess.will_attack(1)
        assert going_to_attack.target_id == 1

        """
        Cancel attack and check if properly removed
        """
        await da.ArmyAccess.cancel_attack(1)
        going_to_attack = await da.ArmyAccess.will_attack(1)
        assert going_to_attack is None

        await da.ArmyAccess.get_army_stats(1)


async def test_army_combat():
    """
    Test combat between 2 armies
    """

    async with sessionmanager.session() as session:
        da = DataAccess(session)

        a1 = await da.ArmyAccess.getArmyById(1)
        a2 = await da.ArmyAccess.getArmyById(2)

        assert a1 is not None
        assert a2 is not None

        await da.ArmyAccess.attack_army(1, 2)

        suc6 = await AttackCheck.check_attack(1, da)
        assert suc6

        a1 = await da.ArmyAccess.getArmyById(1)
        a2 = await da.ArmyAccess.getArmyById(2)

        assert a1 is None or a2 is None


async def test_city_combat():
    """
    Test combat between an army and a city
    """
    async with sessionmanager.session() as session:
        da = DataAccess(session)

        owner = await da.CityAccess.getCityController(1)
        assert owner.id == 2

        await da.ArmyAccess.enter_city(1, 2)

        await da.ArmyAccess.attack_city(1, 1)

        suc6 = await AttackCheck.check_attack(1, da)
        assert suc6

        owner = await da.CityAccess.getCityController(1)
        assert owner.id == 1

        army = await da.ArmyAccess.getArmyById(1)
        troops = await da.ArmyAccess.getTroops(1)

        assert army is not None
        assert len(troops) > 0
