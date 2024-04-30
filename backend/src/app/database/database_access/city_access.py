import math
from sqlalchemy.ext.asyncio import AsyncSession

from .resource_access import ResourceAccess
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

    async def get_city_costs(self):
        """
        get the types of costs associated with cities
        returns a dict, the key is the cost type, the value is a list of costs
        e.f. cost_map["upgrade"] = [(time, 100), (POP, 1000),...]
        """
        get_city_costs = select(CityCosts)
        city_costs = await self.session.execute(get_city_costs)
        city_costs = city_costs.all()
        cost_map = dict()
        for cost in city_costs:
            cost: CityCosts = cost[0]
            if cost.activity not in cost_map:
                cost_map[cost.activity] = [("time", cost.time_cost), (cost.resource_type, cost.cost_amount)]
            else :
                cost_map[cost.activity].append((cost.resource_type, cost.cost_amount))

        return cost_map

    async def get_city_upgrade_cost(self, city_id: int):
        get_city_level = select(City).where(City.id == city_id)
        city = await self.session.execute(get_city_level)
        city : City= city.first()[0]
        city_level = city.rank
        user_id = city.controlled_by

        city_cost_map = await self.get_city_costs()

        base_upgrade_cost: list = city_cost_map["upgrade"]
        base_time = base_upgrade_cost.pop(0)[1]

        ra = ResourceAccess(self.session)
        can_upgrade = await ra.has_resources(user_id, base_upgrade_cost)

        result = PropertyUtility.get_upgrade_city_costs(base_time, base_upgrade_cost, city_level)

        return result[0], result[1], can_upgrade

    async def upgrade_city(self, user_id: int, city_id: int) -> bool:
        """
        upgrade the rank of a city by one
        param: city_id: the city whose rank we want
        """
        upgrade_tuple = await self.get_city_upgrade_cost(city_id)

        get_city = select(City).where(City.id == city_id)
        city = await self.session.execute(get_city)
        city : City= city.first()[0]

        resource_cost = upgrade_tuple[0]
        time_cost = upgrade_tuple[1]
        can_upgrade = upgrade_tuple[2]

        """
        Check if there's an existing upgrade entry for this city
        If an entry exists, return False to indicate no upgrade was performed
        """
        get_existing_update = select(CityUpdateQueue).where(CityUpdateQueue.city_id == city_id)
        existing_update = await self.session.execute(get_existing_update)
        if existing_update.scalars().first():
            return False

        if can_upgrade:

            """
            Decrease the users resources by the required upgrade cost
            """
            ra = ResourceAccess(self.session)
            for u_type, u_amount in resource_cost:
                await ra.remove_resource(user_id, u_type, u_amount)

            city.rank += 1


            """
            Add city to the cityUpdateQueue
            """
            city_update = CityUpdateQueue(city_id=city_id, start_time=datetime.utcnow(), duration=time_cost)

            self.session.add(city_update)

            await self.session.flush()

            await self.session.commit()

            return True

        else:
            return False

    async def get_remain_update_time(self, city_id: int) -> float:
        """
        Checks the remaining time a city has left to be updated,
        returns None if it is done
        """

        """
        Query to find the CityUpdateQueue entry for the specified city_id
        """
        get_update_queue_entry = select(CityUpdateQueue).where(CityUpdateQueue.city_id == city_id)
        update_queue_entry = await self.session.execute(get_update_queue_entry)
        update_queue_entry = update_queue_entry.scalars().first()

        if not update_queue_entry:
            return 0

        """
        Calculate the remaining time
        """
        remaining_time = (update_queue_entry.start_time + timedelta(seconds=update_queue_entry.duration)) - datetime.utcnow()

        if remaining_time.total_seconds() <= 0:
            """
            If the remaining time is zero or negative, remove the update queue entry
            """
            await self.session.delete(update_queue_entry)
            await self.session.commit()
            return 0
        else:
            """
            Return the remaining time in seconds
            """
            return int(remaining_time.total_seconds())