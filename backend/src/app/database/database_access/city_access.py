from ..models.models import *
from ..database import AsyncSession


class CityAccess:
    """
    This class will manage the sql access for data related to information of cities
    """
    def __init__(self, session: AsyncSession):
        self.__session = session

    async def createCity(self, region_id: int, founder_id: int):
        """
        Creates a city like it was just founded
        :param: region_id: the region on a planet we want to create the city in
        :param: founder_id: id of the user who created the city
        :return: the id of the city
        """

        city = City(region_id=region_id, controlled_by=founder_id, x=0, y=0)
        self.__session.add(city)
        await self.__session.flush()
        city_id = city.id
        return city_id

    async def getCityController(self, city_id: int):
        """
        get the user who controls the city
        :param: city_id: id of the city
        :return: the id of the user who is currently in control of the city
        """
        get_user = Select(User).join(City, City.controlled_by == User.id).where(city_id == City.id)

        results = await self.__session.execute(get_user)

        return results.first()[0]
