import datetime
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import *
from sqlalchemy import select, not_, or_, join
from ....logic.formula.compute_properties import *
from .resource_access import ResourceAccess
from .city_access import CityAccess
from ..exceptions.not_found_exception import NotFoundException
from ..exceptions.invalid_action_exception import InvalidActionException
from ..exceptions.permission_exception import PermissionException
from .database_acess import DatabaseAccess


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
        get_buildings = Select(BuildingInstance, BuildingType).\
            join(BuildingInstance, BuildingInstance.building_type == BuildingType.name).\
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

    async def collect_resources(self, user_id: int, building_id: int):
        """
        Collect resources from a production building

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
            join(BuildingInstance, BuildingInstance.building_type == ProducesResources.building_name).\
            where(BuildingInstance.id == building_id)

        production = await self.session.execute(get_production)
        production = production.all()

        """
        Add resources earned over time to user
        """
        delta = await self.get_delta_time(building_id)

        hours = delta.total_seconds()/3600

        """
        Add the resources to user taking into account the max capacity
        """
        ra = ResourceAccess(self.session)
        for p in production:
            """
            Apply the bonus for higher levels of buildings
            """
            production_rate = PropertyUtility.getGPR(1.0, p[0].base_production, p[1])
            max_capacity = PropertyUtility.getGPR(1.0, p[0].max_capacity, p[1])
            await ra.add_resource(user_id, p[0].resource_name, min(int(production_rate*hours), max_capacity))

        """
        Check the building, indicating that the last checked timer needs to be set to now
        """
        await self.checked(building_id)

        await self.session.commit()

        return True

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
        Increase the building rank
        """
        building_instance.rank += 1

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


