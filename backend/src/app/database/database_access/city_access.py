import math
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import *
from .planet_access import PlanetAccess
from .database_acess import DatabaseAccess


class CityAccess(DatabaseAccess):
    """
    This class will manage the sql access for data related to information of cities
    """
    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def create_city(self, planet_id: int, founder_id: int, x: float, y: float):
        """
        Creates a city like it was just founded
        :param: planet_id: id of the planet where we want to create a new city
        :param: founder_id: id of the user who created the city
        :param: x, y: coordinates of where the city will be created
        :return: the id of the city
        """

        """
        Determine in which region the city is found in
        """
        closest_region = await PlanetAccess(self.session).get_closest_region(planet_id, x, y)

        """
        Add the city to the database
        """
        city = City(region_id=closest_region.id, controlled_by=founder_id, x=x, y=y)
        self.session.add(city)
        await self.session.flush()
        city_id = city.id
        return city_id

    async def get_city_controller(self, city_id: int) -> User:
        """
        get the user who controls the city
        :param: city_id: id of the city
        :return: the id of the user who is currently in control of the city
        """

        get_user = Select(User).join(City, City.controlled_by == User.id).where(city_id == City.id)

        results = await self.session.execute(get_user)

        owner = results.scalar_one()
        return owner

    async def get_cities_by_controller(self, user_id: int) -> list[City]:
        """
        get all the cities controlled by a certain user
        :param: city_id: id of the city
        :return: the id of the user who is currently in control of the city
        """
        get_cities = Select(City).where(City.controlled_by == user_id).order_by(asc(City.id))

        results = await self.session.execute(get_cities)
        results = results.scalars().all()

        return list(results)

    async def get_cities_stats(self, city_id: int) -> dict[str, int]:
        """
        Get the attack and defense stats of a city
        :param: city_id: id of the city
        :return: dict of the city stats
        """

        city_stats = {"speed": 0,
                      "attack": 0,
                      "defense": 0,
                      "city_attack": 0,
                      "city_defense": 0}

        """
        Check the towers to calculate the attack stat
        """
        get_towers_attack = Select(TowerType.attack, BuildingInstance.rank).\
            join(BuildingInstance, BuildingInstance.building_type == TowerType.name).\
            where(BuildingInstance.city_id == city_id)
        towers_attack = await self.session.execute(get_towers_attack)
        towers_attack = towers_attack.all()

        """
        Change the stats based on the rank of the building
        """
        for tower in towers_attack:
            city_stats["attack"] += PropertyUtility.getUnitStatsRanked(tower[0], tower[1])
            city_stats["city_attack"] += PropertyUtility.getUnitStatsRanked(tower[0], tower[1])

        """
        Check the towers to calculate the attack stat
        """

        get_walls_defense = Select(WallType.defense, BuildingInstance.rank).\
            join(BuildingInstance, BuildingInstance.building_type == WallType.name).\
            where(BuildingInstance.city_id == city_id)
        walls_defense = await self.session.execute(get_walls_defense)
        walls_defense = walls_defense.all()

        """
        Change the stats based on the rank of the building
        """
        for wall in walls_defense:
            city_stats["defense"] += PropertyUtility.getUnitStatsRanked(wall[0], wall[1])
            city_stats["city_defense"] += PropertyUtility.getUnitStatsRanked(wall[0], wall[1])

        return city_stats

    async def set_new_controller(self, city_id: int, user_id: int):
        """
        Give the city a new controller
        param: city_id: the city whose owner we want to change
        param: user_id: the user who will become the new owner
        """

        u = Update(City).values({"controlled_by": user_id}).where(City.id == city_id)
        await self.session.execute(u)

    async def get_city_rank(self, city_id: int) -> int:
        """
        Get the rank of a city
        param: city_id: the city whose rank we want
        return: rank of the city
        """
        get_rank = Select(City.rank).where(City.id == city_id)
        result = await self.session.execute(get_rank)
        result = result.scalar_one()
        return result
    