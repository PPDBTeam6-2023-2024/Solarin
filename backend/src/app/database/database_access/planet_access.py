from sqlalchemy.orm import joinedload
import math
from ..models.PlanetModels import *
from ..models.SettlementModels import City
from ..models.ArmyModels import Army
from ..database import AsyncSession
from typing import Optional
from .database_acess import DatabaseAccess


class PlanetAccess(DatabaseAccess):
    """
    This class will manage the sql access for data related to information of planets
    """
    def __init__(self, session: AsyncSession):
        super().__init__(session)


    async def create_planet(self, planet_name: str, planet_type: str, x: float, y: float):
        """
        Creates a new planet

        :param: planet_name: name of the planet we want to create
        :param: planet_type: type of the planet
        :return: planet_id of the planet we just created
        """
        planet = Planet(name=planet_name, planet_type=planet_type, x=x, y=y)
        self.session.add(planet)
        await self.session.flush()
        planet_id = planet.id
        return planet_id

    async def create_planet_region(self, planet_id: int, region_type: str, x: float, y: float):
        """
        create a region on a planet

        :param: planet_id: id of the planet the region will be on
        :param: region_type: type of the planet region
        :param: x: the x position between [0-1]
        :param: y: the y position between [0-1]
        :return: region_id of the region that is just created
        """
        region = PlanetRegion(planet_id=planet_id, region_type=region_type, x=x, y=y)
        self.session.add(region)
        await self.session.flush()
        region_id = region.id
        return region_id

    async def get_regions(self, planet_id: int) -> list[PlanetRegion]:
        """
        Get all the regions belonging to the given planet

        :param: planet_id: id of the planet we want to check
        :return: a list of all regions that are on this planet
        """
        select_regions = Select(PlanetRegion).where(PlanetRegion.planet_id == planet_id)
        results = await self.session.execute(select_regions)
        return list(results.scalars().all())

    async def get_planet_cities(self, planet_id: int) -> list[City]:
        """
        Get all the cities that are on the given planet

        :param planet_id: id of the planet we want to check
        :return: a list of all cities that are on this planet
        """
        select_cities = select(City).options(joinedload(City.region)).join(
            PlanetRegion, City.region_id == PlanetRegion.id
        ).where(PlanetRegion.planet_id == planet_id)

        results = await self.session.execute(select_cities)
        return list(results.scalars().all())

    async def get_region_cities(self, region_id: int) -> list[City]:
        """
        Get all the cities that are on the given region

        :param: region_id: id of the region we want to check
        :return: a list of all cities that are on this planet
        """

        select_cities = Select(City).where(City.region_id == region_id)
        results = await self.session.execute(select_cities)
        return list(results.scalars().all())

    async def get_all_planets(self):
        """
        get all the planets in a map

        :return: a list of tuples (planet id, planet name)
        """
        get_planets = Select(Planet.id, Planet.name)
        results = await self.session.execute(get_planets)
        results = results.all()
        return results

    async def get_planet(self, planet_id) -> Optional[Planet]:
        """
        get planet by id
        :param: planet_id: the id of the planet we want to retrieve
        :return: a planet column if it exists, otherwise None
        """
        stmt = (
            Select(Planet)
            .where(Planet.id == planet_id)
        )
        result = await self.session.execute(stmt)
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
        results = await self.session.execute(stmt)
        return results.scalars().all()

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
        results = await self.session.execute(stmt)
        return results.scalar_one()

    async def get_planets_of_user(self, user_id: int) -> list[Planet]:
        """
        Get all the planets that a user has a city or an army on

        :param: user_id: id of the user we want to check
        :return: a list of all planets this user has a city on
        """
        stmt = (
            Select(Planet)
            .join(PlanetRegion, PlanetRegion.planet_id == Planet.id)
            .join(City, City.region_id == PlanetRegion.id)
            .where(City.controlled_by == user_id)
        )
        stmt = stmt.union(
            Select(Planet)
            .join(Army, Army.planet_id == Planet.id)
            .where(Army.user_id == user_id)
        )
        results = await self.session.execute(stmt)
        return results.all()

    async def get_planets_between_times(self, start_time: datetime, end_time: datetime) -> list[Planet]:
        """
        Get all the planets created between two given times

        :param: start_time: the start time
        :param: end_time: the end time
        :return: a list of planets created between the given times
        """
        stmt = (
            Select(Planet)
            .where(Planet.created_at >= start_time)
            .where(Planet.created_at <= end_time)
            .order_by(Planet.created_at.asc())
        )
        results = await self.session.execute(stmt)
        return list(results.scalars().all())

    async def get_closest_region(self, planet_id: int, x: float, y: float):
        """
        Get the region closest to the provided position

        :param: planet_id: id of the planet whose regions we want to check
        :param: x, y: coordinates
        :return: region that is the closest to the provided position
        """

        regions = await PlanetAccess(self.session).get_regions(planet_id)

        """
        Calculate which region our city belongs too based on the closed distance
        """
        closest_region = regions[0]
        closest_distance = math.dist((closest_region.x, closest_region.y), (x, y))
        for region in regions[1:]:
            distance = math.dist((region.x, region.y), (x, y))
            if distance < closest_distance:
                closest_distance = distance
                closest_region = region
        return closest_region

    async def get_planets_amount(self) -> int:
        """
        Get the amount of planets in a region

        :param: region_id: id of the space region we want to check
        :return: the amount of planets in this space region
        """
        stmt = (
            Select(func.count(Planet.id))
        )
        result = await self.session.execute(stmt)
        return result.scalar_one()
    
    async def get_planets_global(self, user_id) -> list[Planet]:
        """
        Get all the planets who are globally visible and include the user its planets

        :param: user_id: id of the user
        :param: region_id: id of the region
        :return: a list of planets
        """
        stmt_city = (
                Select(Planet)
                .join(PlanetRegion, PlanetRegion.planet_id == Planet.id)
                .join(City, City.region_id == PlanetRegion.id)
                .where(City.controlled_by == user_id)
            )

        stmt_army = (
            Select(Planet)
            .join(Army, Army.planet_id == Planet.id)
            .where(Army.user_id == user_id)
            )

        stmt_visible = (
            Select(Planet)
            .where(Planet.visible == True)
        )

        results = await self.session.execute(stmt_city.union(stmt_army, stmt_visible))
        return results.all()
    
    async def get_planet_from_city_id(self, city_id: int) -> Planet:
        stmt = (
            Select(Planet)
            .join(PlanetRegion, PlanetRegion.planet_id == Planet.id)
            .join(City, City.region_id == PlanetRegion.id)
            .where(City.id == city_id)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one()
