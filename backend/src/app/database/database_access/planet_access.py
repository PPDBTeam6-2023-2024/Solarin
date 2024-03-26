from sqlalchemy.orm import joinedload

from ..models.models import *
from ..database import AsyncSession
from typing import Optional

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

    async def createPlanetRegion(self, planet_id: int, region_type: str, x: float, y: float):
        """
        create a region on a planet

        :param: planet_id: id of the planet the region will be on
        :param: region_type: type of the planet region
        :param: x: the x position between [0-1]
        :param: y: the y position between [0-1]
        :return: region_id of the region that is just created
        """
        region = PlanetRegion(planet_id=planet_id, region_type=region_type, x=x, y=y)
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

    async def getPlanet(self, planet_id) -> Optional[Planet]:
        """
        get planet by id
        :return: a planet column if it exists, otherwise None
        """
        stmt = (
            Select(Planet)
            .where(Planet.id == planet_id)
        )
        result = await self.__session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_planet_region_types(self, planet_type: str):
        """
        Get all the planet region types associated with a planet type

        :param: planet_type: the planet type
        :return: a list of all planet regions associated with the planet type
        """
        stmt = (
            Select(PlanetRegionType)
            .join(AssociatedWith, PlanetRegionType.region_type == AssociatedWith.region_type)
            .filter(AssociatedWith.planet_type == planet_type)
        )
        results = await self.__session.execute(stmt)
        return results.all()

    async def get_random_planet_type(self):
        """
        Get a random planet type

        :return: a random planet type
        """
        stmt = (
            Select(PlanetType)
            .order_by(func.random())
            .limit(1)
        )
        results = await self.__session.execute(stmt)
        return results.first()
