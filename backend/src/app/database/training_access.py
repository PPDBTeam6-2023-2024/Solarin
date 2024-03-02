import datetime

from .models import *
from .database import AsyncSession


class TrainingAccess:
    """
    This class will manage the sql access for data related to information of training units
    """
    def __init__(self, session: AsyncSession):
        self.__session = session

    async def trainType(self, army_id: int, building_id: int, troop_type: str, rank: int, amount: int):
        """
        Make a training queue for each training request
        """
        get_highest_id = Select(func.max(TrainingQueue.id)).group_by(TrainingQueue.building_id).where(TrainingQueue.building_id == building_id)
        highest_nr = await self.__session.execute(get_highest_id)
        highest_nr = highest_nr.first()

        if highest_nr is None:
            highest_nr = 0
        else:
            highest_nr = highest_nr[0]+1

        training_time: datetime.timedelta = await self.__getTrainingTime(troop_type)

        tq = TrainingQueue(id=highest_nr, building_id=building_id, troop_type=troop_type, rank=rank,
                           training_size=amount, army_id=army_id, train_remaining=training_time*amount)

        self.__session.add(tq)
        await self.__session.flush()

    async def __getTrainingTime(self, troop_type: str):
        """
        Private function to get the trainingtime of a TroopType
        """
        get_time = Select(TroopType.training_time).where(TroopType.type == troop_type)
        results = await self.__session.execute(get_time)

        if results is None:
            print("throw error")

        results = results.first()[0]

        return results
