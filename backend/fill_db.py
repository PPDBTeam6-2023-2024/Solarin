"""
fill database with test data
"""
import asyncio
from src.app.database.database import *
from src.app.database.database_access.data_access import DataAccess
from src.app.routers.authentication.schemas import MessageToken
from src.app.database.models import *
from src.app.routers.spawn.planet_generation import generate_random_planet
from src.app.config import APIConfig
from confz import FileSource

async def fill_db():
    sessionmanager = DatabaseSessionManager()
    config = APIConfig(config_sources=FileSource(file='config.yml'))
    sessionmanager.init(config.db.get_connection_string().get_secret_value())
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

        await da.commit()

        """
        Creates friendship so that the first 20 are all friends with each other
        """
        for t_index in range(20):
            for t2_index in range(t_index, 20):
                if t_index == t2_index:
                    continue

                await da.UserAccess.addFriendship(t_index + 1, t2_index + 1)
        await da.commit()
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
        await da.DeveloperAccess.createPlanetRegionType("valley of death", "Ooh.. very scary")
        await da.DeveloperAccess.createPlanetRegionType("dark valley", "Ooh.. i cant see")
        await da.DeveloperAccess.createAssociatedWith("Shadow planet", "valley of death")
        await da.DeveloperAccess.createAssociatedWith("Shadow planet", "dark valley")

        p_id = await generate_random_planet(session, sr_id)
        c_id = await da.CityAccess.createCity(p_id, 1, 0.2, 0.8)
        c_id2 = await da.CityAccess.createCity(p_id, 1, 0.8, 0.2)

        """
        Create some types of buildings and resources
        """
        await da.DeveloperAccess.createProductionBuildingType("The mines of moria")
        await da.DeveloperAccess.createBarracksType("Kamino training complex")
        await da.DeveloperAccess.createHouseType("Solarin mansion", 50)
        await da.DeveloperAccess.setProducesResources("The mines of moria", "Vibranium", 10, 200)


        await da.DeveloperAccess.setCreationCost("Solarin mansion", [("Vibranium", 2022), ("Energon", 22)])
        await da.DeveloperAccess.setCreationCost("Kamino training complex", [("Vibranium", 1)])
        await da.DeveloperAccess.setCreationCost("Kamino training complex", [("Energon", 2)])

        """
        Create some actual buildings instances inside cities
        """
        await da.BuildingAccess.createBuilding(c_id, "The mines of moria", 1)
        b_id = await da.BuildingAccess.createBuilding(c_id, "Kamino training complex",1)
        await da.BuildingAccess.createBuilding(c_id, "Solarin mansion",1)

        await da.BuildingAccess.createBuilding(c_id2, "The mines of moria",2)
        b_id2 = await da.BuildingAccess.createBuilding(c_id2, "Kamino training complex",2)
        await da.BuildingAccess.createBuilding(c_id2, "Solarin mansion",2)

        """
        create some types of troops
        """

        a_id = await da.ArmyAccess.createArmy(user_id=1,planet_id=1,x=0.25, y=0.75)
        await da.DeveloperAccess.createToopType("tank", timedelta(hours=4),
                                                BattleStats(attack=5, defense=50, city_attack=1, city_defense=120,
                                                            recovery=5, speed=0.4))

        await da.DeveloperAccess.createToopType("soldier", timedelta(hours=4, minutes=5),
                                                BattleStats(attack=30, defense=30, city_attack=30, city_defense=20,
                                                            recovery=5, speed=0.9))

        await da.DeveloperAccess.setTroopTypeCost("tank", [("SOL", 20)])
        await da.DeveloperAccess.setTroopTypeCost("soldier", [("SOL", 5)])

        """
        add some troops to an army
        """
        await da.ArmyAccess.addToArmy(a_id, "tank", 2, 20)
        await da.ArmyAccess.addToArmy(a_id, "tank", 2, 10)
        await da.ArmyAccess.addToArmy(a_id, "tank", 3, 10)

        """
        start training units
        """
        await da.TrainingAccess.trainType(a_id, b_id, "tank", 3, 10)
        await da.TrainingAccess.trainType(a_id, b_id, "tank", 3, 10)
        await da.TrainingAccess.trainType(a_id, b_id2, "tank", 3, 10)
        await da.TrainingAccess.trainType(a_id, b_id2, "tank", 3, 10)

        await da.commit()

asyncio.run(fill_db())
