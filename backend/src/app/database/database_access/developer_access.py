from ..models import *
from ..database import AsyncSession
from typing import List, Tuple
from .database_acess import DatabaseAccess


class DeveloperAccess(DatabaseAccess):
    """
    This class will manage the sql access for developers to easily expand the game
    These data accesses will mainly create Lookup tables and do other action ordinary players are not allowed to do
    This will also be used to do the database related actions for speeding up time, ... for developers.

    None of these function calls are supposed to be called because of a non-dev user action
    """
    def __init__(self, session: AsyncSession):
        super().__init__(session)
        
    async def create_planet_type(self, type_name: str, description: str = None):
        """
        creates a new type of planet

        :param: type_name: name of the planet type
        :param: description: description of the planet type (if provided)
        :return: nothing
        """
        self.session.add(PlanetType(type=type_name, description=description))
        await self.session.flush()

    async def create_planet_region_type(self, type_name: str, description: str = None):
        """
        creates a new type of planet region

        :param: type_name: name of the planet region type
        :param: description: description of the planet region type (if provided)
        :return: nothing
        """
        self.session.add(PlanetRegionType(region_type=type_name, description=description))
        await self.session.flush()

    async def create_production_building_type(self, name: str):
        """
        Creates a new type of building that can produce certain resources
        These types of buildings will generate certain resources over time

        :param: name: name of the building type
        :param: base_production: the value indicating the base production per hour
        :param: max_capacity: the max amount of the resource that can be buffered inside the building,
                as long as the player doesn't collect its resources from here
        :return: nothing
        """
        pb = ProductionBuildingType(name=name)
        self.session.add(pb)

    async def create_barracks_type(self, name: str):
        """
        Creates a new type of barrack that can train new kinds of troops

        :param: name: name of the building type
        :return: nothing
        """
        brt = BarracksType(name=name)
        self.session.add(brt)

    async def create_tower_type(self, name: str, attack: int):
        """
        Creates a new type of tower

        :param: name: name of the tower type
        :return: nothing
        """
        tower = TowerType(name=name, attack=attack)
        self.session.add(tower)

    async def create_wall_type(self, name: str, defense: int):
        """
       Creates a new type of wall

       :param: name: name of the wall type
       :return: nothing
       """
        wall = WallType(name=name, defense=defense)
        self.session.add(wall)

    async def create_house_type(self, name: str, residents: int):
        """
        Create a new type of house having its citizens

        :param: name: name of the building type
        :param: residents: amount of residents living in such a house
        :return: nothing
        """
        ht = HouseType(name=name, residents=residents)
        self.session.add(ht)

    async def create_resource_type(self, type_name: str):
        """
        Add a new type of resource

        :param: type_name: name of resource
        :return: nothing
        """
        r = ResourceType(name=type_name)
        self.session.add(r)

    async def set_produces_resources(self, building_name: str, resource_name: str, base_production: int,
                                     max_capacity: int):
        """
        Creates the link between a productionBuildingType and the Resource type it produces

        :param: building_name: name of the production building
        :param: resource_name: name of resource that will be produced
        :return: nothing
        """
        pr = ProducesResources(building_name=building_name, resource_name=resource_name,
                               base_production=base_production, max_capacity=max_capacity)
        self.session.add(pr)

    async def create_troop_type(self, type_name: str, training_time: timedelta, battle_stats: BattleStats,
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
        self.session.add(troop_type)

    async def set_troop_type_cost(self, troop_name: str, resource_costs: List[Tuple[str, int]]):
        """
        make costs associated with training troops

        :param: troop_name: the name of the troop with want to give a trainings cost
        :param: resource_costs: a list of tuples with format List[Tuple[str, int]].
                The tuples will contain (resource_name, amount) and it is a list to easily support adding
                costs of multiple resources for 1 troop type.
        :return: nothing
        """

        """
        Delete the costs that were set before
        """
        await self.session.flush()
        old_cost = delete(TroopTypeCost).where(TroopTypeCost.troop_type == troop_name)
        await self.session.execute(old_cost)

        """
        Set the new costs
        """
        for resource in resource_costs:
            troop_type_cost = TroopTypeCost(troop_type=troop_name, resource_type=resource[0], amount=resource[1])
            self.session.add(troop_type_cost)

    async def set_creation_cost(self, building_name: str, resource_costs: List[Tuple[str, int]]):
        """
        add a create cost for a certain building,
        This stores the base values for a creation

        :param: building_name: the name of the building type we want to create
        :param: resource_costs: a list of tuples with format List[Tuple[str, int]].
                The tuples will contain (resource_name, amount) and it is a list to easily support adding
                costs of multiple resources for 1 troop type.
        :return: nothing
        """

        """
        Delete the costs that were set before
        """
        old_up_cost = delete(CreationCost).where(CreationCost.building_name == building_name)
        await self.session.execute(old_up_cost)

        """
        Set the new costs
        """
        for resource in resource_costs:
            upgrade = CreationCost(building_name=building_name, cost_type=resource[0], cost_amount=resource[1])
            self.session.add(upgrade)

        await self.session.flush()

    async def create_associated_with(self, planet_type: str, region_type: str):
        """
        Store which region types are associated with which planet

        :param: planet_type: type of the planet of the association
        :param: region_type: type of the region of the association
        """

        self.session.add(AssociatedWith(planet_type=planet_type, region_type=region_type))
        await self.session.flush()

    async def set_production_modifier(self, resource_type: str, region_type: str, modifier: float):
        """
            Some resources are more equal than others... Or more prevalent based on the region type.

        Set production modifier, i.e. a production boost or reduction based on
        - the type of resource being produced
        - the type of region it is produced in

        :param: resource_type: type of the resource
        :param: region_type: type of the planet region
        :param: modifier: multiplier to apply to production rate
        """

        self.session.add(ProductionRegionModifier(resource_type=resource_type, region_type=region_type, modifier=modifier))
        await self.session.flush()