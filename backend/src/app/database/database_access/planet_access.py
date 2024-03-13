from sqlalchemy.orm import joinedload

from ..models.models import *
from ..database import AsyncSession

class PlanetAccess:
    """
    This class will manage the sql access for data related to information of planets
    """
    def __init__(self, session: AsyncSession):
        self.__session = session

    async def createSpaceRegion(self, region_name: str):
        """
        Creates space region and returns the id generated

        :param: region_name: name of the space region we want to create
        :return: region_id of the space region we just created
        """
        sp = SpaceRegion(name=region_name)
        self.__session.add(sp)
        await self.__session.flush()
        region_id = sp.id
        return region_id

    async def createPlanet(self, planet_name: str, planet_type: str, space_region_id: int):
        """
        Creates a new planet

        :param: planet_name: name of the planet we want to create
        :param: planet_type: type of the planet
        :param: space_region_id: space region this planet belongs too
        :return: planet_id of the planet we just created
        """
        planet = Planet(name=planet_name, planet_type=planet_type, space_region_id=space_region_id)
        self.__session.add(planet)
        await self.__session.flush()
        planet_id = planet.id
        return planet_id

    async def createPlanetRegion(self, planet_id: int, region_type: str, coordinate: tuple[int, int]):
        """
        create a region on a planet

        :param: planet_id: id of the planet the region will be on
        :param: region_type: type of the planet region
        :param: coordinate: coordinates of the planet region
        :return: region_id of the region that is just created
        """
        region = PlanetRegion(planet_id=planet_id, region_type=region_type, x=coordinate[0], y=coordinate[1])
        self.__session.add(region)
        await self.__session.flush()
        region_id = region.id
        return region_id

    async def getRegions(self, planet_id: int):
        """
        Get all the regions belonging to the given planet

        :param: planet_id: id of the planet we want to check
        :return: a list of all regions that are on this planet
        """
        select_regions = Select(PlanetRegion).where(PlanetRegion.planet_id == planet_id)
        results = await self.__session.execute(select_regions)
        return results.all()

    async def getPlanetCities(self, planet_id: int):
        """
        Get all the cities that are on the given planet

        :param planet_id: id of the planet we want to check
        :return: a list of all cities that are on this planet
        """
        select_cities = select(City).options(joinedload(City.region)).join(
            PlanetRegion, City.region_id == PlanetRegion.id
        ).where(PlanetRegion.planet_id == planet_id)

        results = await self.__session.execute(select_cities)
        return results.all()

    async def getRegionCities(self, region_id: int):
        """
        Get all the cities that are on the given region

        :param: region_id: id of the region we want to check
        :return: a list of all cities that are on this planet
        """

        select_cities = Select(City).where(City.region_id == region_id)
        results = await self.__session.execute(select_cities)
        return results.all()

    async def getAllPlanets(self):
        """
        get all the planets in a map

        :return: a list of tuples (planet id, planet name)
        """
        get_planets = Select(Planet.id, Planet.name)
        results = await self.__session.execute(get_planets)
        results = results.all()
        return results