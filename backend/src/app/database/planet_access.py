from .models import *
from .database import db, AsyncSession


class PlanetAccess:
    """
    This class will manage the sql access for data related to information of planets
    """
    def __init__(self, session):
        self.__session = session

    async def createSpaceRegion(self, region_name: str):
        """
        Creates space region and returns the id generated
        """
        sp = SpaceRegion(name=region_name)
        self.__session.add(sp)
        await self.__session.flush()
        region_id = sp.space_region_id
        return region_id

    async def createPlanet(self, planet_name: str, planet_type: str, space_region_id: int):
        """
        Creates a new planet
        """
        planet = Planet(name=planet_name, planet_type=planet_type, space_region_id=space_region_id)
        self.__session.add(planet)
        await self.__session.flush()
        planet_id = planet.id
        return planet_id

    async def createPlanetRegion(self, planet_id: int, region_type: str):
        """
        create a region on a planet
        """
        region = PlanetRegion(planet_id=planet_id, region_type=region_type)
        self.__session.add(region)
        await self.__session.flush()
        region_id = region.id
        return region_id
