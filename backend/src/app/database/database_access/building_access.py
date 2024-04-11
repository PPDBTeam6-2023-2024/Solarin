import datetime

from ..models import *
from ..database import AsyncSession
from sqlalchemy import select, not_, or_, join
from ....logic.utils.compute_properties import *
from .resource_access import ResourceAccess
from .city_access import CityAccess
from ..exceptions.not_found_exception import NotFoundException
from ..exceptions.invalid_action_exception import InvalidActionException
from ..exceptions.permission_exception import PermissionException


class BuildingAccess:
    """
    This class will manage the sql access for data related to information of planets
    """
    def __init__(self, session: AsyncSession):
        self.__session = session

    async def __get_building_cost(self, building_type: str, to_rank: int) -> list:
        """
        get the creation
        to_rank is the rank we want our building to upgrade to, to rank == 1 means creating the building
        """
        cost_query = select(CreationCost.cost_type, CreationCost.cost_amount).where(
            CreationCost.building_name == building_type)
        cost_query_results = await self.__session.execute(cost_query)
        cost_query_rows = cost_query_results.all()

        cost_query_rows = [(c[0], PropertyUtility.getGUC(c[1], to_rank)) for c in cost_query_rows]

        if len(cost_query_rows) == 0:
            raise NotFoundException(building_type, "creation Cost")

        return list(cost_query_rows)

    async def create_building(self, user_id: int, city_id: int, building_type: str):
        """
        Create a new instance of building corresponding to a city
        :param: user_id: the id of the user who controls the city
        :param: city_id: the id of the city we want to add a building to
        :param: building_type: the type of building we want to add
        :return: the id of the building we just created
        """

        ra = ResourceAccess(self.__session)
        ca = CityAccess(self.__session)

        """
        Check if the user is also the owner of the provided city
        """
        city_owner = await ca.getCityController(city_id)
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

        if not has_enough_resources:
            raise InvalidActionException("The user does not have enough resources to build this building")

        """
        Remove the resources from the user his/hers account
        """
        for cost_type, cost_amount in creation_cost:
            await ra.remove_resource(user_id, cost_type, cost_amount)

        """
        Create the building instance
        """
        building_instance = BuildingInstance(city_id=city_id, building_type=building_type)
        self.__session.add(building_instance)

        await self.__session.flush()

        building_id = building_instance.id

        await self.__session.commit()

        return building_id

    async def get_city_buildings(self, city_id: int):
        """
        This method will give all the buildings (from a city) its id, category, type
        -id: unique identifier of the building
        -type: what kind of building it is (House, Production building, Barrack, ...)
        -name: the more specific type of building (mine, ...)

        :param: city_id: id of the city whose buildings we want
        :return:
        """
        get_buildings = Select(BuildingInstance, BuildingType).\
            join(BuildingInstance, BuildingInstance.building_type == BuildingType.name).\
            where(BuildingInstance.city_id == city_id).order_by(asc(BuildingInstance.id))

        building_types = await self.__session.execute(get_buildings)

        return building_types.all()

    async def get_building_types(self):
        """
        get all the types of buildings that are in the game

        :param: city_id: id of the city whose buildings we want
        :return: (type, name) representing each building type
        """

        """
        generate query to access all building tables to access its types
        """
        building_types = await self.__session.execute(Select(BuildingType))

        return building_types.scalars().all()

    async def get_delta_time(self, building_id: int) -> timedelta:
        """
        get the between now and when the building was last checked
        :param: building_id: id of the building
        :return: datetime of when the building was last checked
        """
        last_checked = Select(BuildingInstance.last_checked).where(BuildingInstance.id == building_id)
        results = await self.__session.execute(last_checked)
        last = results.scalar_one_or_none()
        if last is None:
            raise NotFoundException(building_id, "Building Instance")

        return datetime.utcnow() - last

    async def checked(self, building_id: int):
        """
        Indicates that the building is checked, and so set the last checked to current time
        """
        u = update(BuildingInstance).values({"last_checked": datetime.utcnow()}).\
            where(BuildingInstance.id == building_id)
        await self.__session.execute(u)

        await self.__session.flush()

    async def get_available_building_types(self, user_id: int, city_id: int, city_rank: int):
        """
        Get all building types that are being able to be build, based on the upgrade cost and the
        required rank

        and check if the user has enough resources.

        :param city_id: ID of the city
        :param city_rank: Rank of the city
        :param user_id: ID of the user
        :return: List of available building types for the city along with a boolean indicating if the user can build it
        """

        ra = ResourceAccess(self.__session)
        ca = CityAccess(self.__session)

        """
        Check if the user is also the owner of the provided city
        """
        city_owner = await ca.getCityController(city_id)
        if city_owner.id != user_id:
            raise PermissionException(user_id, "add buildings to the city of other players")

        building_types = await self.get_building_types()

        buildings_data = []

        """
        For each building Type request the resource costs needed
        """
        for building_type in building_types:
            if building_type.required_rank is not None and building_type.required_rank > city_rank:

                continue

            creation_cost = await self.__get_building_cost(building_type.name, 1)

            building_data = {attr: getattr(building_type, attr) for attr in BuildingType.__table__.columns.keys()}
            building_data.update({"costs": [{"cost_type": c[0], 'cost_amount': c[1]} for c in creation_cost]})
            building_data['can_build'] = await ra.has_resources(user_id, creation_cost)
            buildings_data.append(building_data)

        return buildings_data

    async def increase_resource_stocks(self, city_id: int) -> bool:

        building_instances_query = select(BuildingInstance).where(
            BuildingInstance.city_id == city_id)
        building_instances_results = await self.__session.execute(building_instances_query)

        for building_instance_row in building_instances_results:
            building_instance: BuildingInstance = building_instance_row[0]
            building_id = building_instance.id
            building_name = building_instance.building_type
            building_type = building_instance.type
            building_rank = building_instance.rank

            if isinstance(building_type, ProductionBuildingType):
                # Fetch all production details for the building
                prod_details_query = select(ProducesResources).where(
                    ProducesResources.building_name == building_name)
                prod_details_result = await self.__session.execute(prod_details_query)
                prod_details = prod_details_result.scalars().all()

                for prod_detail in prod_details:
                    resource_name = prod_detail.resource_name
                    base_production = prod_detail.base_production
                    max_capacity = prod_detail.max_capacity

                    # Calculate the amount to increase based on the time delta and base production
                    time_delta = await self.get_delta_time(building_id)
                    time_delta_as_minutes = int(time_delta.total_seconds() / 60)
                    amount_to_increase = time_delta_as_minutes * PropertyUtility.getGPR(1.0,base_production,building_rank)

                    # Fetch the current amount of the resource for the building
                    current_amount_query = select(StoresResources.amount).where(
                        and_(StoresResources.building_id == building_id,
                             StoresResources.resource_type == resource_name))
                    current_amount_result = await self.__session.execute(current_amount_query)
                    current_amount_row = current_amount_result.fetchone()

                    if current_amount_row is None:
                        # No entry found, assume current amount is 0 and create a new entry
                        current_amount = 0
                        new_resource_entry = StoresResources(building_id=building_id,
                                                             resource_type=resource_name, amount=current_amount)
                        self.__session.add(new_resource_entry)
                        await self.__session.flush()
                    else:
                        # Entry found, use the current amount from the result
                        current_amount = current_amount_row[0]

                    new_amount = min(current_amount + amount_to_increase, max_capacity)

                    # Update or create StoresResources entry with the new amount or the max capacity if exceeded
                    if current_amount_row:
                        update_query = (
                            update(StoresResources)
                            .where(and_(StoresResources.building_id == building_id,
                                        StoresResources.resource_type == resource_name))
                            .values(amount=new_amount)
                        )
                        await self.__session.execute(update_query)
                    else:
                        # Since we've already added the new entry, we just need to update its amount
                        new_resource_entry.amount = new_amount

                update_last_checked = update(BuildingInstance).where(BuildingInstance.id == building_id).values(last_checked = datetime.utcnow() )
                await self.__session.execute(update_last_checked)

        await self.__session.commit()
        return True

    async def collect_resources(self, building_id: int, user_id: int):
        # Retrieve all resource amounts from StoresResources for the building
        current_amounts_query = select(StoresResources).where(StoresResources.building_id == building_id)
        results = await self.__session.execute(current_amounts_query)
        resources = results.scalars().all()

        # Iterate over each resource and update HasResources
        for resource in resources:


            # Update HasResources with the current amount for each resource type
            if resource.amount is not None:
                update_has_resources = (
                    update(HasResources)
                    .where(HasResources.owner_id == user_id, HasResources.resource_type == resource.resource_type)
                    .values(quantity=HasResources.quantity + resource.amount)
                )
                await self.__session.execute(update_has_resources)

        # Then, set the StoresResources amount to zero for all entries of the building
        reset_stores_resources = (
            update(StoresResources)
            .where(StoresResources.building_id == building_id)
            .values(amount=0)
        )
        await self.__session.execute(reset_stores_resources)

        await self.__session.commit()

        return True

    async def upgrade_building(self, user_id: int, building_id: int):
        """
        Upgrade a building
        :param user_id: id of the user who wants to upgrade the building
        :param building_id: id of building we want to upgrade
        """

        if not await self.is_owner(building_id, user_id):
            raise PermissionException(user_id, "upgrading someone else their building is not allowed")

        """
        get building instance
        """
        building_instance_query = select(BuildingInstance).where(
            BuildingInstance.id == building_id)
        building_instances_results = await self.__session.execute(building_instance_query)

        building_instance = building_instances_results.scalar_one()

        """
        get current rank
        """
        current_rank = building_instance.rank
        current_type = building_instance.building_type

        await self.__session.flush()

        """
        get upgrade cost
        """
        upgrade_cost = await self.__get_building_cost(current_type, current_rank+1)

        ra = ResourceAccess(self.__session)
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

        await self.__session.commit()

        return True

    async def get_upgrade_cost(self, user_id: int, building_id: int) -> tuple[int, list[tuple[str, int]], bool]:
        """
        retrieve the building type its upgrade cost

        :param user_id: id of the user who asks for the upgrade cost
        :param building_id: id of building whose upgrade cost we want
        :return: Tuple: building id int, upgrade cost (list), can_build boolean
        """

        if not self.is_owner(building_id, user_id):
            raise PermissionException(user_id, "retrieve the upgrade cost of someone their building")

        """
        retrieve building type
        """
        building_instance_query = select(BuildingInstance).where(BuildingInstance.id == building_id)
        building_instances_results = await self.__session.execute(building_instance_query)
        building_instance = building_instances_results.scalar_one()

        current_rank = building_instance.rank
        current_type = building_instance.building_type

        """
        Get upgrade cost
        """
        upgrade_cost = await self.__get_building_cost(current_type, current_rank+1)

        ra = ResourceAccess(self.__session)
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

        gc = Select(City).join(BuildingInstance, BuildingInstance.city_id ==City.id).where(building_id == BuildingInstance.id)
        results = await self.__session.execute(gc)
        result = results.scalar_one()
        return result

    async def is_owner(self, building_id: int, user_id: int):
        """
        Checks if the user is owner of this building
        """

        get_building = Select(City.controlled_by).join(BuildingInstance, City.id == BuildingInstance.city_id).where(BuildingInstance.id == building_id)
        results = await self.__session.execute(get_building)
        results = results.first()

        if results is None:
            return False
        if results[0] != user_id:
            return False
        return True

