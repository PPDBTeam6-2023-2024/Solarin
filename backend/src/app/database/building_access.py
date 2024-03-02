from .models import *
from .database import AsyncSession


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
