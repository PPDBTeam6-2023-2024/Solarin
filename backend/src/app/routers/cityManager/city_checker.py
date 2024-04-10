from ...database.database_access.data_access import DataAccess
from ...database.models import BuildingInstance, BarracksType


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
        this function will do all checks
        """
        buildings = await self.da.BuildingAccess.get_city_buildings(self.city_id)

        await self.check_training(buildings)

        for b in buildings:
            await self.da.BuildingAccess.checked(b[0].id)

    async def check_training(self, buildings):
        """
        this function will check the training of units and its assignment to an army when they are trained
        """

        """
        checks the queues of barrack type buildings
        """
        for b in buildings:
            if not isinstance(b[1], BarracksType):
                continue

            await self.da.TrainingAccess.check_queue(b[0].id)
