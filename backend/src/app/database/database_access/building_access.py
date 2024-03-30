import datetime

from ..models.models import *
from ..database import AsyncSession


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

        return building_instance.id

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

    async def getDeltaTime(self, building_id: int):
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

        return datetime.utcnow()-last[0]

    async def checked(self, building_id: int):
        """
        Indicates that the building is checked, and so set the last checked to current time
        """
        u = update(BuildingInstance).values({"last_checked": datetime.utcnow()}).where(BuildingInstance.id == building_id)
        await self.__session.execute(u)

        await self.__session.flush()