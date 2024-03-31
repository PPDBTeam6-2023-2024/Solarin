import datetime

from ..models.models import *
from ..database import AsyncSession
from sqlalchemy import select, not_, or_


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
        the required rank is null or less than or equal to the city's rank.

        :param city_id: ID of the city
        :param city_rank: Rank of the city
        :return: List of available building types for the city
        """
        # Get all building names in the city
        city_buildings = select(BuildingInstance.building_type).where(BuildingInstance.city_id == city_id)
        city_buildings_results = await self.__session.execute(city_buildings)
        city_building_names = [result[0] for result in city_buildings_results]

        # Select building types not in the city and meeting the rank requirement
        available_buildings = select(BuildingType).where(
            or_(
                BuildingType.required_rank == None,
                BuildingType.required_rank <= city_rank
            ),
            not_(BuildingType.name.in_(city_building_names))
        )

        results = await self.__session.execute(available_buildings)
        return results.all()
