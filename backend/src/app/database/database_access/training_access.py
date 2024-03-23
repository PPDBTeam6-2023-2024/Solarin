import datetime

from ..models.models import *
from ..database import AsyncSession


class TrainingAccess:
    """
    This class will manage the sql access for data related to information of training units
    """
    def __init__(self, session: AsyncSession):
        self.__session = session

    async def trainType(self, army_id: int, building_id: int, troop_type: str, rank: int, amount: int):
        """
        Make a training queue for each training request, an entry in the training queue is 1 Entry in the
        queue for a barrack, each queue entry needs to be identified, and linked to barrack building.
        To make sure that the identifier of the queue doesn't grow very large we make TrainingQueue a weak entity of
        a building (which needs to be some kind of barrack). The reason why we care about keeping the id of the queue
        low is because after training is completed the queue entry will be removed. After training a lot of units we
        will end up with high ID numbers while only having a couple entries. So the keep it low, we will make sure the
        next id is 1 higher than the highest id corresponding to the building.
        Concrete NextQueue Is = highest queue Id (correspond to the building id) + 1

        :param: army_id: army we want to add the units to after they are trained
        :param: building_id: id of the building which will be some kind of barrack
        :param: troop_type: type of troop we are training
        :param: rank: the rank of the troop we want to train
        :param: amount: amount of this type of troop we want to train, this will increase the training time accordingly,
        but is useful so users directly train multiple
        :return: nothing
        """
        get_highest_id = Select(func.max(TrainingQueue.id)).group_by(TrainingQueue.building_id).\
            where(TrainingQueue.building_id == building_id)
        highest_nr = await self.__session.execute(get_highest_id)
        highest_nr = highest_nr.first()

        """
        calculate the new highest id corresponding to the building id,
        This ensures that we can keep the id values low and that key (building_id, id) is unique
        """
        if highest_nr is None:
            highest_nr = 0
        else:
            highest_nr = highest_nr[0]+1

        """
        create queue
        """
        training_time: datetime.timedelta = await self.__getTrainingTime(troop_type)
        tq = TrainingQueue(id=highest_nr, building_id=building_id, troop_type=troop_type, rank=rank,
                           training_size=amount, army_id=army_id, train_remaining=training_time*amount)

        self.__session.add(tq)
        await self.__session.flush()

    async def __getTrainingTime(self, troop_type: str):
        """
        Private function to get the training time of a TroopType
        """
        get_time = Select(TroopType.training_time).where(TroopType.type == troop_type)
        results = await self.__session.execute(get_time)

        if results is None:
            raise Exception("SQL TrainingAccess --> __getTrainingTime: unit does not exist")

        results = results.first()[0]

        return results