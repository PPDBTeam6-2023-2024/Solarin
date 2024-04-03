import datetime

from ..models.models import *
from ..database import AsyncSession
from sqlalchemy import select, not_, or_, join


class BuildingAccess:
    """
    This class will manage the sql access for data related to information of planets
    """
    def __init__(self, session: AsyncSession):
        self.__session = session

    async def createBuilding(self, city_id: int, building_type: str):
        """
        Create a new instance of building corresponding to a city
        :param: city_id: the id of the city we want to add a building to
        :param: building_type: the type of building we want to add
        :return: the id of the building we just created
        """
        cost_query = select(CreationCost.cost_amount, CreationCost.cost_type).where(CreationCost.building_name == building_type)
        cost_query_results = await self.__session.execute(cost_query)
        cost_query_row = cost_query_results.all()
        if cost_query_row is None:
            raise ValueError(f"No user found controlling city with ID {city_id}")
        cost_amount = cost_query_row[0][0]
        cost_type = cost_query_row[0][1]

        # Get user id
        user_id_query = select(City.controlled_by).where(City.id==city_id)
        user_id_results = await self.__session.execute(user_id_query)
        user_id_row = user_id_results.scalar()

        # Check if user_id_row is None to handle cases where no results are returned
        if user_id_row is None:
            raise ValueError(f"No user found controlling city with ID {city_id}")

        user_id = user_id_row

        # reduce resources in has resources table, by cost
        # Update the HasResources table by subtracting the cost amount from the user's resource quantity
        update_query = (
            update(HasResources)
            .where(and_(HasResources.owner_id == user_id, HasResources.resource_type == cost_type))
            .values({HasResources.quantity: HasResources.quantity - cost_amount})
        )
        await self.__session.execute(update_query)

        building_instance = BuildingInstance(city_id=city_id, building_type=building_type)

        self.__session.add(building_instance)
        await self.__session.flush()

        building_id = building_instance.id

        await self.__session.commit()

        return building_id

    async def getCityBuildings(self, city_id: int):
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

    async def getBuildingTypes(self):
        """
        get all the types of buildings that are in the game

        :param: city_id: id of the city whose buildings we want
        :return: (type, name) representing each building type
        """

        """
        generate query to access all building tables to access its types
        """
        building_types = await self.__session.execute(Select(BuildingType))

        return building_types.all()

    async def getDeltaTime(self, building_id: int) -> timedelta:
        """
        get the between now and when the building was last checked
        :param: building_id: id of the building
        :return: datetime of when the building was last checked
        """
        last_checked = Select(BuildingInstance.last_checked).where(BuildingInstance.id == building_id)
        results = await self.__session.execute(last_checked)
        last = results.first()
        if last is None:
            raise Exception("Building does not exist")

        # Check if last[0] is None, which means the building was never checked
        if last[0] is None:
            # Handle the never checked scenario. For example, return None or raise an exception.
            return timedelta(seconds=0)

            # Calculate the delta time since the building was last checked
        return datetime.utcnow() - last[0]

    async def checked(self, building_id: int):
        """
        Indicates that the building is checked, and so set the last checked to current time
        """
        u = update(BuildingInstance).values({"last_checked": datetime.utcnow()}).where(BuildingInstance.id == building_id)
        await self.__session.execute(u)

        await self.__session.flush()

    async def getAvailableBuildingTypes(self, city_id: int, city_rank: int):
        """
        Get all building types that are not yet present in the city and for which
        the required rank is null or less than or equal to the city's rank. Join
        with the CreationCost table to filter based on the available building types
        and check if the user has enough resources.

        :param city_id: ID of the city
        :param city_rank: Rank of the city
        :param user_id: ID of the user
        :return: List of available building types for the city along with a boolean indicating if the user can build it
        """

        # Get user id
        user_id_query = select(City.controlled_by).where(City.id==city_id)
        user_id_results = await self.__session.execute(user_id_query)
        user_id_row = user_id_results.scalar()

        # Check if user_id_row is None to handle cases where no results are returned
        if user_id_row is None:
            raise ValueError(f"No user found controlling city with ID {city_id}")

        user_id = user_id_row

        # Get all building names in the city
        city_buildings_query = select(BuildingInstance.building_type).where(BuildingInstance.city_id == city_id)
        city_buildings_results = await self.__session.execute(city_buildings_query)
        city_building_names = [result[0] for result in city_buildings_results]

        # Get user's available resources
        available_resources_query = select(HasResources).where(HasResources.owner_id == user_id)
        available_resources_results = await self.__session.execute(available_resources_query)
        user_resources = {res.resource_type: res.quantity for res in available_resources_results.scalars().all()}

        # Define a join between BuildingType and CreationCost on the building name
        join_condition = join(BuildingType, CreationCost, BuildingType.name == CreationCost.building_name)
        available_buildings_query = select(
            BuildingType,
            CreationCost
        ).select_from(join_condition).where(
            and_(
                or_(
                    BuildingType.required_rank == None,
                    BuildingType.required_rank <= city_rank
                ),
                not_(BuildingType.name.in_(city_building_names))
            )
        )

        available_buildings_results = await self.__session.execute(available_buildings_query)
        available_buildings = available_buildings_results.all()

        buildings_data = []
        for building, cost in available_buildings:
            can_build = user_resources.get(cost.cost_type, 0) >= cost.cost_amount
            # Construct building_data dictionary manually
            building_data = {attr: getattr(building, attr) for attr in BuildingType.__table__.columns.keys()}
            building_data.update({attr: getattr(cost, attr) for attr in CreationCost.__table__.columns.keys()})
            building_data['can_build'] = can_build
            buildings_data.append(building_data)

        return buildings_data

    async def IncreaseResourceStocks(self, city_id: int) -> bool:

        building_instances_query = select(BuildingInstance).where(
            BuildingInstance.city_id == city_id)
        building_instances_results = await self.__session.execute(building_instances_query)

        for building_instance_row in building_instances_results:
            building_instance: BuildingInstance = building_instance_row[0]
            building_id = building_instance.id
            building_name = building_instance.building_type
            building_type = building_instance.type

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
                    time_delta = await self.getDeltaTime(building_id)
                    time_delta_as_minutes = int(time_delta.total_seconds() / 60)
                    amount_to_increase = time_delta_as_minutes * base_production

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

    async def collectResources(self, building_id: int, city_id: int):

        # Get user id
        user_id_query = select(City.controlled_by).where(City.id == city_id)
        user_id_results = await self.__session.execute(user_id_query)
        user_id_row = user_id_results.scalar()

        # Check if user_id_row is None to handle cases where no results are returned
        if user_id_row is None:
            raise ValueError(f"No user found controlling city with ID {city_id}")

        user_id = user_id_row

        # First, retrieve the current resource amount from StoresResources for the building
        current_amount_query = select(StoresResources.amount).where(StoresResources.building_id == building_id)
        result = await self.__session.execute(current_amount_query)
        current_amount = result.scalar_one_or_none()

        # If there is a current amount, update HasResources with this amount
        if current_amount is not None:
            update_has_resources = (
                update(HasResources)
                .where(StoresResources.building_id == building_id, HasResources.owner_id == user_id)
                .values(quantity=HasResources.quantity + current_amount)
            )
            await self.__session.execute(update_has_resources)

        # Then, set the StoresResources amount to zero for the building
        reset_stores_resources = (
            update(StoresResources)
            .where(StoresResources.building_id == building_id)
            .values(amount=0)
        )
        await self.__session.execute(reset_stores_resources)

        await self.__session.commit()

        return True
