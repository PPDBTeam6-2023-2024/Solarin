import datetime
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import *
from sqlalchemy import select, not_, or_, join

from ..models.SettlementModels import BuildingType
from ....logic.formula.compute_properties import *
from .resource_access import ResourceAccess
from .city_access import CityAccess
from ..exceptions.not_found_exception import NotFoundException
from ..exceptions.invalid_action_exception import InvalidActionException
from ..exceptions.permission_exception import PermissionException
from .database_acess import DatabaseAccess
from .user_access import UserAccess
from ....logic.formula.compute_properties import PoliticalModifiers
from src.app import config


class BuildingAccess(DatabaseAccess):
    """
    This class will manage the sql access for data related to information of buildings
    """
    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def __get_building_cost(self, building_type: str, to_rank: int) -> list:
        """
        get the creation/Upgrade cost (to_rank 1 => creation cost)

        :param: building_type: the type of building whose cost we want
        :param: to_rank: the rank we want our building to upgrade to, to rank == 1 means creating the building
        """

        """
        Retrieve the base costs
        """
        cost_query = select(CreationCost.cost_type, CreationCost.cost_amount).where(
            CreationCost.building_name == building_type)
        cost_query_results = await self.session.execute(cost_query)
        cost_query_rows = cost_query_results.all()

        """
        Apply the cost changes based on the rank we want to upgrade to
        """
        cost_query_rows = [(c[0], PropertyUtility.getGUC(c[1], to_rank)) for c in cost_query_rows]

        """
        Error in case we do not have an upgrade cost
        """
        if len(cost_query_rows) == 0:
            raise NotFoundException(building_type, "creation Cost")

        return list(cost_query_rows)

    async def create_building(self, user_id: int, city_id: int, building_type: str, force: bool = False):
        """
        Create a new instance of building corresponding to a city
        :param: user_id: the id of the user who controls the city
        :param: city_id: the id of the city we want to add a building to
        :param: building_type: the type of building we want to add
        :param: force: if you enforce to build it even if the user does not have enough resources
        :return: the id of the building we just created
        """

        ra = ResourceAccess(self.session)
        ca = CityAccess(self.session)

        """
        Check if the user is also the owner of the provided city
        """
        city_owner = await ca.get_city_controller(city_id)
        if city_owner.id != user_id:
            raise PermissionException(user_id, "add buildings to the city of other players")

        """
        Retrieve the creation cost
        """
        creation_cost = await self.__get_building_cost(building_type, 1)

        """
        Check if the user has enough resources to building this building
        """
        has_enough_resources: bool = await ra.has_resources(user_id, creation_cost)

        if not has_enough_resources and not force:
            raise InvalidActionException("The user does not have enough resources to build this building")

        """
        Remove the resources from the user his/hers account
        """
        if not force:
            for cost_type, cost_amount in creation_cost:
                await ra.remove_resource(user_id, cost_type, cost_amount)

        """
        Create the building instance
        """
        building_instance = BuildingInstance(city_id=city_id, building_type=building_type)
        self.session.add(building_instance)

        await self.session.flush()
        building_id = building_instance.id

        return building_id

    async def get_city_buildings(self, city_id: int):
        """
        This method will give all the buildings (from a city) its id, category, type
        -id: unique identifier of the building
        -type: what kind of building it is (House, Production building, Barrack, ...)
        -name: the more specific type of building (mine, ...)

        :param: city_id: id of the city whose buildings we want
        :return: list of tuples: BuildingInstance object, Building Type Object
        """
        get_buildings = Select(BuildingInstance).\
            where(BuildingInstance.city_id == city_id).order_by(asc(BuildingInstance.id))

        building_types = await self.session.execute(get_buildings)

        return building_types.scalars().all()

    async def get_building_types(self):
        """
        get all the types of buildings that are in the game

        :param: city_id: id of the city whose buildings we want
        :return: (type, name) representing each building type
        """

        """
        generate query to access all building tables to access its types
        """
        building_types = await self.session.execute(Select(BuildingType))

        return building_types.scalars().all()

    async def get_delta_time(self, building_id: int, raw_time: bool=False) -> timedelta:
        """
        get the between now and when the building was last checked
        :param: building_id: id of the building
        :param: raw_time: return the last_checked time instead of delta time
        :return: datetime of when the building was last checked
        """
        last_checked = Select(BuildingInstance.last_checked).where(BuildingInstance.id == building_id)
        results = await self.session.execute(last_checked)
        last = results.scalar_one_or_none()
        if last is None:
            raise NotFoundException(building_id, "Building Instance")

        if raw_time:
            return last
        return datetime.utcnow() - last

    async def checked(self, building_id: int):
        """
        Indicates that the building is checked, and so set the last checked to current time
        """
        u = update(BuildingInstance).values({"last_checked": datetime.utcnow()}).\
            where(BuildingInstance.id == building_id)
        await self.session.execute(u)

        await self.session.flush()

    async def get_available_building_types(self, user_id: int, city_id: int):
        """
        Get all building types that are being able to be build, based on the upgrade cost and the
        required rank. Make sure only buildings not yet inside the city are available

        and check if the user has enough resources.

        :param city_id: ID of the city
        :param user_id: ID of the user
        :return: List of available building types for the city along with a boolean indicating if the user can build it
        """

        ra = ResourceAccess(self.session)
        ca = CityAccess(self.session)

        """
        Check if the user is also the owner of the provided city
        """
        city_owner = await ca.get_city_controller(city_id)
        if city_owner.id != user_id:
            raise PermissionException(user_id, "add buildings to the city of other players")

        building_types = await self.get_building_types()

        """
        get the building types of the buildings that are inside the city
        """
        get_city_building_type = Select(BuildingType.name).\
            join(BuildingInstance, BuildingType.name == BuildingInstance.building_type).\
            where(BuildingInstance.city_id == city_id)

        city_buildings = await self.session.execute(get_city_building_type)
        city_buildings = city_buildings.scalars().all()

        """
        Calculate all the building types not yet inside the city
        """
        new_building_types = []
        for b in building_types:
            if b.name not in city_buildings:
                new_building_types.append(b)

        building_types = new_building_types

        """
        Obtain the costs of the building types the user is able to create
        """
        buildings_data = []

        """
        For each building Type request the resource costs needed
        """
        city_rank = await ca.get_city_rank(city_id)

        for building_type in building_types:
            if building_type.required_rank is not None and building_type.required_rank > city_rank:
                continue

            creation_cost = await self.__get_building_cost(building_type.name, 1)

            building_data = {attr: getattr(building_type, attr) for attr in BuildingType.__table__.columns.keys()}
            building_data.update({"costs": [{"cost_type": c[0], 'cost_amount': c[1]} for c in creation_cost]})
            building_data['can_build'] = await ra.has_resources(user_id, creation_cost)
            buildings_data.append(building_data)

        return buildings_data

    async def get_building_rank(self, building_id: int):
        """
        Get the rank of a building

        :param: building_id: id of the building whose rank we want
        return: int indicating the rank of the building
        """
        get_rank = Select(BuildingInstance.rank).where(BuildingInstance.id == building_id)
        rank = await self.session.execute(get_rank)
        rank = rank.scalar_one()
        return rank

    async def get_region_controlled_by(self, region_id: int) -> int | None:
        """
        Get the controller of a region

        :param: region_id: id of the region we want to check
        :return: user_id of controller of the region, returns None if there is no controller of the region,
        meaning at least two different users have cities in the region
        """

        get_cities = Select(City).where(City.region_id == region_id)
        cities = await self.session.execute(get_cities)
        cities = set(cities.scalars().all())
        users = set()
        for city in cities:
            city: City
            users.add(city.controlled_by)
        if len(users) != 1:
            return None
        else:
            return users.pop()

    async def get_resource_stocks(self, user_id: int, city_id: int):
        """
        Get the dict with resources for each building in a city

        :param: user_id: the id of the user who is collecting the resources
        :param: city_id: id of the target city
        """

        ba = BuildingAccess(self.session)
        building_list = await BuildingAccess.get_city_buildings(ba,city_id)

        get_production_building_list = select(ProductionBuildingType)
        production_building_list = await self.session.execute(get_production_building_list)
        production_building_list = production_building_list.all()


        production_building_set = set()
        for building in production_building_list:
            production_building_set.add(building[0])

        overview_dict = dict()

        for building_instance in building_list:
            building_instance: BuildingInstance
            if building_instance.type in production_building_set:
                temp = await self.collect_resources(user_id, building_instance.id, False)
                overview_dict[building_instance.id] = temp

        return overview_dict

    async def get_production_building_stats(self, user_id: int, building_id: int):
        """
        Get the production rate stats for a particular building

        :param: building_id: id of the building whose stats we want
        """
        """
             Check if the user is also the owner of the provided city
             """
        is_owner = await self.is_owner(user_id, building_id)
        if not is_owner:
            raise PermissionException(user_id, "cannot get building stats from another user")

        """
        retrieve the resource production
        """
        get_production = Select(ProducesResources, BuildingInstance.rank). \
            join(BuildingInstance, BuildingInstance.building_type == ProducesResources.building_name). \
            where(BuildingInstance.id == building_id)

        production = await self.session.execute(get_production)
        production = production.all()

        """
        Get planet_region building is located in
        """
        get_building = select(BuildingInstance).where(BuildingInstance.id == building_id)
        building = await self.session.execute(get_building)
        building: BuildingInstance = building.first()[0]

        get_planet_region_id = select(City.region_id).where(building.city_id == City.id)
        planet_region_id = await self.session.execute(get_planet_region_id)
        planet_region_id = planet_region_id.scalar_one_or_none()

        region_controller = await self.get_region_controlled_by(planet_region_id)

        region_control = False
        if region_controller == user_id:
            region_control = True

        """
        Get production bonuses based on region type and store as dict
        """
        get_production_modifier = select(ProductionRegionModifier.resource_type, ProductionRegionModifier.modifier) \
            .join(City, City.id == building.city_id) \
            .join(PlanetRegion, City.region_id == PlanetRegion.id).where(
            ProductionRegionModifier.region_type == PlanetRegion.region_type)

        production_modifier = await self.session.execute(get_production_modifier)
        production_modifier = production_modifier.fetchall()

        """
        calculate and apply the political modifier
        default value = 1
        """

        stance = await UserAccess(self.session).get_politics(user_id)
        general_production_modifier = PoliticalModifiers.production_modifier(stance)

        modifier_dict = dict()
        for row_list in production_modifier:
            resource_type = row_list[0]
            modifier_dict[resource_type] = row_list[1]
            modifier_dict[resource_type] += general_production_modifier

        rates = dict()
        for p in production:
            """
            if regional modifier exists, apply
            else set regional modifier to 1.0
            """
            modifier_ = modifier_dict.get(p[0].resource_name)
            if modifier_ is None:
                modifier_ = 1.0

            """
            Calculate production rate using following modifiers:
            - bonus for higher levels of buildings
            - regional modifiers (for higher yields in certain regions)
            - control modifier (higher production rate if in control of region)
            """
            production_rate = PropertyUtility.getGPR(modifier_, p[0].base_production, p[1], region_control)
            rates[p[0].resource_name] = production_rate
        return rates

    async def collect_resources(self, user_id: int, building_id: int, collect_resources: bool):
        """
        Get the resources stocks for a building and
        collect resources from a production building ( by setting collect_resources=True )

        :param: user_id: the id of the user who is collecting the resources
        :param: building_id: id of the building whose resources we will collect
        """

        """
        Check if the user is also the owner of the provided city
        """
        is_owner = await self.is_owner(user_id, building_id)
        if not is_owner:
            raise PermissionException(user_id, "cannot collect resources from a building from another user")

        """
        retrieve the resource production
        """
        get_production = Select(ProducesResources, BuildingInstance.rank).\
            join(BuildingInstance, ProducesResources.building_name == BuildingInstance.building_type).\
            where(BuildingInstance.id == building_id)

        production = await self.session.execute(get_production)
        production = production.all()

        """
        Add resources earned over time to user
        """
        delta = await self.get_delta_time(building_id)

        hours = delta.total_seconds()/3600

        """
        Get planet_region building is located in
        """
        get_building = select(BuildingInstance).where(BuildingInstance.id==building_id)
        building = await self.session.execute(get_building)
        building: BuildingInstance = building.first()[0]

        get_planet_region_id = select(City.region_id).where(building.city_id == City.id)
        planet_region_id = await self.session.execute(get_planet_region_id)
        planet_region_id = planet_region_id.scalar_one_or_none()

        region_controller = await self.get_region_controlled_by(planet_region_id)

        region_control = False
        if region_controller == user_id:
            region_control = True

        """
        Get production bonuses based on region type and store as dict
        """
        get_production_modifier = select(ProductionRegionModifier.resource_type, ProductionRegionModifier.modifier) \
            .join(City, City.id == building.city_id) \
            .join(PlanetRegion, City.region_id == PlanetRegion.id).where(ProductionRegionModifier.region_type == PlanetRegion.region_type)


        production_modifier = await self.session.execute(get_production_modifier)
        production_modifier = production_modifier.fetchall()

        """
        calculate and apply the political modifier
        default value = 1
        """

        stance = await UserAccess(self.session).get_politics(user_id)

        general_production_modifier = PoliticalModifiers.production_modifier(stance)

        modifier_dict = dict()
        for row_list in production_modifier:
            resource_type = row_list[0]
            modifier_dict[resource_type] = row_list[1]
            modifier_dict[resource_type] += general_production_modifier

        """
        Store new amount to list
        """
        updated_resource_stocks = []

        """
        Add the resources to user taking into account the max capacity
        """
        ra = ResourceAccess(self.session)

        for p in production:
            """
            if regional modifier exists, apply
            else set regional modifier to 1.0
            """
            modifier_ = modifier_dict.get(p[0].resource_name)
            if modifier_ is None:
                modifier_ = 1.0

            """
            Calculate production rate using following modifiers:
            - bonus for higher levels of buildings
            - regional modifiers (for higher yields in certain regions)
            - control modifier (higher production rate if in control of region)
            """
            production_rate = PropertyUtility.getGPR(modifier_, p[0].base_production, p[1], region_control)

            max_capacity = PropertyUtility.getGPR(modifier_, p[0].max_capacity, p[1], False)

            # add increased resource to list
            updated_resource_stocks.append((p[0].resource_name, min(int(production_rate*hours),max_capacity), max_capacity ))

            # if flag "increase_resources" is on, increase resources
            if collect_resources:
                await ra.add_resource(user_id, p[0].resource_name, min(int(production_rate*hours), max_capacity))

        """
        If flag "increase_resources" is on,
        check the building, indicating that the last checked timer needs to be set to now
        """
        if collect_resources:
            await self.checked(building_id)

            await self.session.commit()

        return updated_resource_stocks


    async def upgrade_building(self, user_id: int, building_id: int):
        """
        Upgrade a building
        :param user_id: id of the user who wants to upgrade the building
        :param building_id: id of building we want to upgrade
        """
        if not await self.is_owner(user_id, building_id):
            raise PermissionException(user_id, "upgrading someone else their building is not allowed")

        """
        get building instance
        """
        building_instance_query = select(BuildingInstance).where(
            BuildingInstance.id == building_id)
        building_instances_results = await self.session.execute(building_instance_query)

        building_instance = building_instances_results.scalar_one()

        """
        get current rank
        """
        current_rank = building_instance.rank
        current_type = building_instance.building_type

        await self.session.flush()

        """
        get upgrade cost
        """
        upgrade_cost = await self.__get_building_cost(current_type, current_rank+1)

        ra = ResourceAccess(self.session)
        can_upgrade = await ra.has_resources(user_id, upgrade_cost)

        if not can_upgrade:
            raise InvalidActionException("insufficient resources to upgrade this building")

        """
        Get TF cost from cost list
        """
        TF_cost = None
        for cost_type, cost_amount in upgrade_cost:
            if cost_type == "TF":
                TF_cost = cost_amount
                break


        """
        Add building to the upgrade queue
        """
        if config.idle_time is not None:
            duration = config.idle_time
        else:
            duration = PropertyUtility.get_GUT(TF_cost, building_instance.rank)
        building_upgrade = BuildingUpgradeQueue(id=building_id, city_id=building_instance.city_id, start_time=datetime.utcnow(), duration=duration, current_rank=building_instance.rank)

        self.session.add(building_upgrade)


        """
        Remove the resources form the user their account
        """
        for u_type, u_amount in upgrade_cost:
            await ra.remove_resource(user_id, u_type, u_amount)

        await self.session.commit()

        return True

    async def get_upgrade_cost(self, user_id: int, building_id: int) -> tuple[int, list[tuple[str, int]], bool]:
        """
        retrieve the building type its upgrade cost

        :param user_id: id of the user who asks for the upgrade cost
        :param building_id: id of building whose upgrade cost we want
        :return: Tuple: building id int, upgrade cost (list), can_build boolean
        """

        if not await self.is_owner(user_id, building_id):
            raise PermissionException(user_id, "retrieve the upgrade cost of someone their building")

        """
        retrieve building type
        """
        building_instance_query = select(BuildingInstance).where(BuildingInstance.id == building_id)
        building_instances_results = await self.session.execute(building_instance_query)
        building_instance = building_instances_results.scalar_one()

        current_rank = building_instance.rank
        current_type = building_instance.building_type

        """
        Get upgrade cost
        """
        upgrade_cost = await self.__get_building_cost(current_type, current_rank+1)

        ra = ResourceAccess(self.session)
        can_upgrade = await ra.has_resources(user_id, upgrade_cost)

        """
        Return building id, upgrade cost and whether the user can afford it
        """
        return building_id, upgrade_cost, can_upgrade

    async def get_city(self, building_id: int):
        """
        get the city corresponding to this building

        :param building_id: id of building whose corresponding city we want
        """

        gc = Select(City).\
            join(BuildingInstance, BuildingInstance.city_id ==City.id).where(building_id == BuildingInstance.id)
        results = await self.session.execute(gc)
        result = results.scalar_one()
        return result

    async def is_owner(self, user_id: int, building_id: int):
        """
        Checks if the user is owner of this building

        :param: user_id: id of the user we want to check whether he is the owner or not
        :param: building_id: id of the building we want to check
        return: bool indicating if the user is the owener or not
        """

        get_building = Select(City.controlled_by).\
            join(BuildingInstance, City.id == BuildingInstance.city_id).where(BuildingInstance.id == building_id)
        results = await self.session.execute(get_building)
        results = results.scalar_one_or_none()

        if results is None:
            return False

        return results == user_id

    async def update_building_upgrade_queue(self, city_id: int):
        """
        Update the building upgrade queue and remove buildings that are done
        """

        get_upgrade_list = select(BuildingUpgradeQueue).where(BuildingUpgradeQueue.city_id == city_id)
        upgrade_list = await self.session.execute(get_upgrade_list)

        upgrade_list = upgrade_list.all()

        remaining_update_dict = dict()

        for upgrade in upgrade_list:
            upgrade_queue_entry = upgrade[0]
            """
            Calculate the remaining time
            """
            remaining_time = (upgrade_queue_entry.start_time + timedelta(
                seconds=upgrade_queue_entry.duration)) - datetime.utcnow()

            get_building_instance = select(BuildingInstance).where(upgrade_queue_entry.id==BuildingInstance.id)
            get_building_instance = await self.session.execute(get_building_instance)

            """
            Increase the building rank
            """
            building_instance: BuildingInstance = get_building_instance.first()[0]


            if remaining_time.total_seconds() <= 0:

                building_instance.rank += 1

                """
                If the remaining time is zero or negative, remove the update queue entry
                """
                await self.session.delete(upgrade_queue_entry)

            else:
                """
                Add the remaining time in seconds to the upgrade time dict
                """
                remaining_update_dict[building_instance.id] = floor(remaining_time.total_seconds())

        await self.session.flush()
        await self.session.commit()

        return remaining_update_dict

    async def get_base_stats(self):
        """
        get the base stats of all types of towers and walls
        :return: a dictionary with wall/tower names as keys and their defense/attack values as values
        """
        # Query WallType
        wall_query = select(WallType.name, WallType.defense)
        result = await self.session.execute(wall_query)
        wall_types = result.all()

        # Query TowerType
        tower_query = select(TowerType.name, TowerType.attack)
        result = await self.session.execute(tower_query)
        tower_types = result.all()

        # Combine results into a single dictionary
        base_stats = {name: value for name, value in wall_types}
        base_stats.update({name: value for name, value in tower_types})

        return base_stats

    async def get_prod_stats(self):
        """
        get the types of production buildings and what they produce
        :return: a dictionary with building name as key and what it produces as value
        """
        query = Select(ProducesResources.building_name, ProducesResources.resource_name, ProducesResources.base_production)
        result = await self.session.execute(query)
        result = result.all()
        return result


    async def get_barrack_ids_in_city(self, city_id: int) -> list[int]:
        """
        Get all the barrack ids in a city
        :param city_id: id of the city
        :return: list of barrack ids
        """
        get_barracks = select(BuildingInstance.id).where(and_(BuildingInstance.city_id == city_id, BuildingInstance.building_type == "barracks"))
        barracks = await self.session.execute(get_barracks)
        barracks = barracks.all()
        return [b[0] for b in barracks]