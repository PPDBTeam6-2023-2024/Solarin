import math

from ..models.models import *
from ..database import AsyncSession
from .planet_access import PlanetAccess


class CityAccess:
    """
    This class will manage the sql access for data related to information of cities
    """
    def __init__(self, session: AsyncSession):
        self.__session = session

    async def createCity(self, planet_id: int, founder_id: int, x: float, y: float):
        """
        Creates a city like it was just founded
        :param: founder_id: id of the user who created the city
        :return: the id of the city
        """
        regions = await PlanetAccess(self.__session).getRegions(planet_id)

        closest_region = regions[0]
        closest_distance = math.dist((closest_region.x,closest_region.y), (x,y))
        for region in regions[1:]:
            distance = math.dist((region.x,region.y), (x,y))
            if distance < closest_distance:
                closest_distance = distance
                closest_region = region

        city = City(region_id=closest_region.id, controlled_by=founder_id, x=x, y=y)
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

    async def getCitiesByController(self, user_id: int):
        """
        get all the cities controlled by a certain user
        :param: city_id: id of the city
        :return: the id of the user who is currently in control of the city
        """
        get_cities = Select(City).where(City.controlled_by == user_id).order_by(asc(City.id))

        results = await self.__session.execute(get_cities)
        results = results.all()

        return results
