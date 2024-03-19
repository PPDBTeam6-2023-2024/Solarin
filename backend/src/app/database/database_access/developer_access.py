from ..models.models import *
from ..database import AsyncSession
from typing import List, Tuple
from sqlalchemy import select

class DeveloperAccess:
    """
    This class will manage the sql access for developers to easily expand the game
    These data accesses will mainly create Lookup tables and do other action ordinary players are not allowed to do
    This will also be used to do the database related actions for speeding up time, ... for developers.

    None of these function calls are supposed to be called because of a non-dev user action
    """
    def __init__(self, session: AsyncSession):
        self.__session = session

    async def createPlanetType(self, type_name: str, description: str = None):
        """
        creates a new type of planet

        :param: type_name: name of the planet type
        :param: description: description of the planet type (if provided)
        :return: nothing
        """
        self.__session.add(PlanetType(type=type_name, description=description))
        await self.__session.flush()


    async def createPlanetRegionType(self, type_name: str, description: str = None):
        """
        creates a new type of planet region

        :param: type_name: name of the planet region type
        :param: description: description of the planet region type (if provided)
        :return: nothing
        """

        self.__session.add(PlanetRegionType(region_type=type_name, description=description))
        await self.__session.flush()


    async def createProductionBuildingType(self, name: str, base_production: int, max_capacity: int):
        """
        Creates a new type of building that can produce certain resources
        These types of buildings will generate certain resources over time

        :param: name: name of the building type
        :param: base_production: the value indicating the base production per hour
        :param: max_capacity: the max amount of the resource that can be buffered inside the building,
                as long as the player doesn't collect its resources from here
        :return: nothing
        """
        pb = ProductionBuildingType(name=name, base_production=base_production, max_capacity=max_capacity)
        self.__session.add(pb)


    async def createBarracksType(self, name: str):
        """
        Creates a new type of barrack that can train new kinds of troops

        :param: name: name of the building type
        :return: nothing
        """
        brt = BarracksType(name=name)
        self.__session.add(brt)


    async def createHouseType(self, name: str, residents: int):
        """
        Create a new type of house having its citizens

        :param: name: name of the building type
        :param: residents: amount of residents living in such a house
        :return: nothing
        """
        ht = HouseType(name=name, residents=residents)
        self.__session.add(ht)


    async def createResourceType(self, type_name: str):
        """
        Add a new type of resource

        :param: type_name: name of resource
        :return: nothing
        """
        r = ResourceType(name=type_name)
        self.__session.add(r)
        await self.__session.flush()


    async def setProducesResources(self, building_name: str, resource_name: str):
        """
        Creates the link between a productionBuildingType and the Resource type it produces

        :param: building_name: name of the production building
        :param: resource_name: name of resource that will be produced
        :return: nothing
        """
        pr = ProducesResources(building_name=building_name, resource_name=resource_name)
        self.__session.add(pr)


    async def createToopType(self, type_name: str, training_time: timedelta, battle_stats: BattleStats,
                             required_rank: int = None):
        """
        Create a new type of troop that can be added to an army

        :param: type_name: name of the troop type
        :param: training_time: the time that will be needed to train such a troop
        :param: battle_stats: a schema containing all the stats of a unit
        :param: required_rank: the rank a building is required to have to unlock the option to train this troop
        :return: nothing
        """
        troop_type = TroopType.withBattleStats(type_name, training_time, battle_stats, required_rank)
        self.__session.add(troop_type)
        await self.__session.flush()


    async def setTroopTypeCost(self, troop_name: str, resource_costs: List[Tuple[str, int]]):
        """
        make costs associated with training troops

        :param: troop_name: the name of the troop with want to give a trainings cost
        :param: resource_costs: a list of tuples with format List[Tuple[str, int]].
                The tuples will contain (resource_name, amount) and it is a list to easily support adding
                costs of multiple resources for 1 troop type.
        :return: nothing
        """

        await self.__session.flush()
        old_cost = delete(TroopTypeCost).where(TroopTypeCost.troop_type == troop_name)
        await self.__session.execute(old_cost)

        for resource in resource_costs:
            troop_type_cost = TroopTypeCost(troop_type=troop_name, resource_type=resource[0], amount=resource[1])
            self.__session.add(troop_type_cost)

    async def setUpgradeCost(self, building_name: str, resource_costs: List[Tuple[str, int]]):
        """
        add an upgrade cost for a certain building,
        This stores the base values for an upgrade

        :param: building_name: the name of the building type we want to upgrade
        :param: resource_costs: a list of tuples with format List[Tuple[str, int]].
                The tuples will contain (resource_name, amount) and it is a list to easily support adding
                costs of multiple resources for 1 troop type.
        :return: nothing
        """

        await self.__session.flush()
        old_up_cost = delete(UpgradeCost).where(UpgradeCost.building_name == building_name)
        await self.__session.execute(old_up_cost)

        for resource in resource_costs:
            upgrade = UpgradeCost(building_name=building_name, cost_type=resource[0], cost_amount=resource[1])
            self.__session.add(upgrade)

