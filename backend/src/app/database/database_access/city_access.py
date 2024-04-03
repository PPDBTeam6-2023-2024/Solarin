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

    async def get_cities_stats(self, city_id: int):
        """
        Get the attack and defense stats of a city
        :param: city_id: id of the city
        :return: dict of the city stats
        """

        city_stats = {}

        """
        Check the towers to calculate the attack stat
        """

        get_towers_attack = Select(TowerType.attack, BuildingInstance.rank).join(BuildingInstance, BuildingInstance.building_type==TowerType.name).where(BuildingInstance.city_id == city_id)
        towers_attack = await self.__session.execute(get_towers_attack)
        towers_attack = towers_attack.all()

        city_stats["attack"] = 0
        for tower in towers_attack:
            city_stats["attack"] += PropertyUtility.getUnitStatsRanked(tower[0], tower[1])

        """
        Check the towers to calculate the attack stat
        """

        get_walls_defense = Select(WallType.defense, BuildingInstance.rank).join(BuildingInstance,
                                                                                 BuildingInstance.building_type == WallType.name).where(
            BuildingInstance.city_id == city_id)
        walls_defense = await self.__session.execute(get_walls_defense)
        walls_defense = walls_defense.all()

        city_stats["defense"] = 0
        for wall in walls_defense:
            city_stats["defense"] += PropertyUtility.getUnitStatsRanked(wall[0], wall[1])

        return city_stats

    async def set_new_controller(self, city_id: int, user_id: int):
        """
        Give the city a new controller
        param: city_id: the city whose owner we want to change
        param: user_id: the user who will become the new owner
        """

        u = Update(City).values({"controlled_by": user_id}).where(City.id == city_id)
        await self.__session.execute(u)