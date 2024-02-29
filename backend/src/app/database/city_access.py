from .models import *
from .database import db, AsyncSession


class CityAccess:
    """
    This class will manage the sql access for data related to information of planets
    """
    def __init__(self, session):
        self.__session = session

    async def createCity(self, planet_id: int, region_id: int, founder_id: int):
        """
        Creates a city like it was just founded
        """
        city = City(planet_id=planet_id, region_id=region_id, controlled_by=founder_id)
        self.__session.add(city)
        await self.__session.flush()
        city_id = city.id
        return city_id
