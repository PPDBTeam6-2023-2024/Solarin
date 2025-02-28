from ...database.database_access.data_access import DataAccess
from ...database.models import BuildingInstance, BarracksType
import asyncio

check_semaphore = asyncio.Semaphore(1)


class CityChecker:
    """
    This class is a checker so we can trigger the right city checks, and update the city information
    """

    def __init__(self, city_id: int, da: DataAccess):
        """
        Constructor for the checker containing the city id we want to check
        """

        self.city_id = city_id
        self.da = da

    async def check_all(self):
        """
        this function will do all checks for idle mechanics in cities
        retuns: (remaining update time city, remaining update time building)
        """
        async with check_semaphore:
            remaining_update_time_city = await self.da.CityAccess.get_remain_update_time(city_id=self.city_id)
            remaining_update_time_buildings = await self.da.BuildingAccess.update_building_upgrade_queue(city_id=self.city_id)

            buildings = await self.da.BuildingAccess.get_city_buildings(self.city_id)

            await self.check_training(buildings)
            await self.da.flush()

        return remaining_update_time_city, remaining_update_time_buildings

    async def check_upgrade_time(self):
        remaining_update_time = await self.da.CityAccess.get_remain_update_time(city_id=self.city_id)
        return remaining_update_time

    async def check_training(self, buildings):
        """
        this function will check the training of units and its assignment to an army when they are trained
        """

        """
        checks the queues of barrack type buildings
        """
        for b in buildings:
            if not isinstance(b.type, BarracksType):
                continue

            await self.da.TrainingAccess.check_queue(b.id)

            await self.da.BuildingAccess.checked(b.id)

            await self.da.flush()
