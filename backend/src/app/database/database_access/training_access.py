import datetime
import math
from ..models.models import *
from ..database import AsyncSession
from .building_access import BuildingAccess
from .army_access import ArmyAccess
from ....logic.utils.compute_properties import *

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
        when the highest_nr == 0, it means the queue is empty, to make sure the remaining time is not affected (in case user leaves training menu open)
        And so reduces its waiting time in advance, we will set the last_checked to current time if the queue was empty before
        """
        if highest_nr == 0:
            u = update(BuildingInstance).values({"last_checked": datetime.datetime.now()}).where(BuildingInstance.id == building_id)
            await self.__session.execute(u)

        """
        create queue
        """
        training_time: int = await self.__getTrainingTime(troop_type)
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

        return int(results)

    async def check_queue(self, building_id, seconds=None):
        """
        this function will check the queue of a building type, it check which units are done training and assign
        them to an army

        :param: building_id: id of buildings whose queue we will check
        :param: seconds: time in between provided (ONLY USED BY DEVELOPERS) if None, the real time will be used
        """

        results = await self.get_queue(building_id)

        """
        developers should be allowed to change the time, that is why seconds can be provided
        """
        if seconds is None:
            delta_time = await BuildingAccess(self.__session).getDeltaTime(building_id)
            seconds = delta_time.total_seconds()
            print("s", seconds)
        print("s2", seconds)

        for r in results:
            if seconds <= 0:
                break

            """
            this loop will go through the training queues
            It will take the first entry and do remaining_time -= seconds passed
            if remaining_time < 0: remove queue entry and add the troops to the army,
            If multiple troops trained add only part to army when not fully done
            """

            per_unit_training_time = r[1]
            queue_entry: TrainingQueue = r[0]

            """
            make sure we don't train more units than are in a queue => use min
            """
            troops_trained = min(math.floor(seconds/per_unit_training_time), queue_entry.training_size)

            diff = queue_entry.train_remaining - seconds
            if diff < 0:
                seconds = seconds - queue_entry.train_remaining
            else:
                queue_entry.train_remaining = diff
                seconds = 0

            """
            handle the trained unit changes
            """
            army_access = ArmyAccess(self.__session)
            await army_access.addToArmy(queue_entry.army_id, queue_entry.troop_type, queue_entry.rank, troops_trained)
            queue_entry.training_size -= troops_trained

            """
            when entry done, remove training queue entry
            """
            if diff < 0:
                await self.__session.delete(queue_entry)

        """
        make a commit of the training changes and potentially removed training queue entries
        """
        await self.__session.flush()

    async def get_queue(self, building_id):
        """
        get the training queue of a building id
        :param: building_id: id of buildings whose queue we will check
        :return: list of trainingQueueObjects and the time/unit for that unit type
        """

        """
                query to get the training queue, sorted by asc Training id, so the first entry will be first in the list 
                """
        get_queue_entries = Select(TrainingQueue, TroopType.training_time).join(TroopType,
                                                                                TroopType.type == TrainingQueue.troop_type).where(
            TrainingQueue.building_id == building_id).order_by(asc(TrainingQueue.id))
        results = await self.__session.execute(get_queue_entries)
        results = results.all()
        return results

    async def get_troop_cost(self, user_id: int, troop_type: str):
        """
        Calculate the cost of 1 unit, based on the rank the user has leveled the unit to

        :param: user_id: id of the user who wants to know the unit cost
        :param: troop_type: type of unit it wants to train
        :return: list of following format (resource_type, amount)
        """

        rank = await self.get_troop_rank(user_id, troop_type)

        get_cost = Select(TroopTypeCost.resource_type, TroopTypeCost.amount).where(TroopTypeCost.troop_type == troop_type)

        resources = await self.__session.execute(get_cost)
        resources = resources.all()
        ranked_cost = []

        """
        Make sure the cost depend on the rank
        """
        for r, c in resources:
            real_cost = PropertyUtility.getGUC(c, rank)
            ranked_cost.append((r, real_cost))

        return ranked_cost

    async def get_troop_rank(self, user_id: int, troop_type: str):
        """
        Get the rank of a specific unit for a specific user

        :param: user_id: id of the user who wants to know the unit cost
        :param: troop_type: type of unit whose rank we want to retrieve corresponding to the user id
        """

        rank = Select(TroopRank.rank).where((TroopRank.user_id==user_id) & (TroopRank.troop_type==troop_type))
        results = await self.__session.execute(rank)
        result = results.first()

        if result is None:
            return 1
        return result[0]

    async def upgrade_troop_rank(self, user_id: int, troop_type: str):
        """
        Upgrade the rank of a specific unit, for a specific user

        :param: user_id: id of the user who wants to know the unit cost
        :param: troop_type: type of unit whose rank we want to upgrade corresponding to the user id
        """

        rank = await self.get_troop_rank(user_id, troop_type)

        """
        rank 1 is not yet stored, so if the original rank mis 1, we need to create a row with the new rank
        """
        create_new_row = False
        if rank == 1:
            create_new_row = True

        rank += 1

        if create_new_row:
            """
            create new row entry
            """
            self.__session.add(TroopRank(user_id=user_id, troop_type=troop_type, rank=rank))
        else:
            """
            alter row entry
            """
            u = update(TroopRank).values({"rank": rank}).where((TroopRank.user_id==user_id) & (TroopRank.troop_type==troop_type))
            await self.__session.execute(u)

        await self.__session.flush()

