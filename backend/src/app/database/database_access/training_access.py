import datetime
import math
from ..models import *
from ..database import AsyncSession
from .building_access import BuildingAccess
from .army_access import ArmyAccess
from ....logic.formula.compute_properties import *
from .database_acess import DatabaseAccess
from src.app import config
from .user_access import UserAccess
from .city_access import CityAccess


class TrainingAccess(DatabaseAccess):
    """
    This class will manage the sql access for data related to information of training units
    """
    def __init__(self, session: AsyncSession):
        super().__init__(session)
        
    async def train_type(self, building_id: int, troop_type: str, rank: int, amount: int):
        """
        Make a training queue for each training request, an entry in the training queue is 1 Entry in the
        queue for a barrack, each queue entry needs to be identified, and linked to barrack building.
        To make sure that the identifier of the queue doesn't grow very large we make TrainingQueue a weak entity of
        a building (which needs to be some kind of barrack). The reason why we care about keeping the id of the queue
        low is because after training is completed the queue entry will be removed. After training a lot of units we
        will end up with high ID numbers while only having a couple entries. So the keep it low, we will make sure the
        next id is 1 higher than the highest id corresponding to the building.
        Concrete NextQueue Is = highest queue Id (correspond to the building id) + 1

        :param: building_id: id of the building which will be some kind of barrack
        :param: troop_type: type of troop we are training
        :param: rank: the rank of the troop we want to train
        :param: amount: amount of this type of troop we want to train, this will increase the training time accordingly,
        but is useful so users directly train multiple
        :return: nothing
        """
        get_highest_id = Select(func.max(TrainingQueue.id)).group_by(TrainingQueue.building_id).\
            where(TrainingQueue.building_id == building_id)
        highest_nr = await self.session.execute(get_highest_id)
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
        when the highest_nr == 0, it means the queue is empty, to make sure the remaining time is not 
        affected (in case user leaves training menu open)
        And so reduces its waiting time in advance, we will set the last_checked to current time 
        if the queue was empty before
        """
        if highest_nr == 0:
            u = update(BuildingInstance).values({"last_checked": datetime.utcnow()}).\
                where(BuildingInstance.id == building_id)
            await self.session.execute(u)

        """
        create queue
        """
        if config.idle_time is not None:
            training_time = config.idle_time * amount
        else:
            training_time: int = await self.__getTrainingTime(troop_type) * amount

        """
        Let the training time depend on the political stance
        """
        city_id = (await BuildingAccess(self.session).get_city(building_id)).id
        user_id = await CityAccess(self.session).get_city_controller(city_id)
        stance = await UserAccess(self.session).get_politics(user_id.id)
        modifier2 = PoliticalModifiers.training_speed_modifier(stance)

        training_time *= modifier2

        tq = TrainingQueue(id=highest_nr, building_id=building_id, troop_type=troop_type, rank=rank,
                           training_size=amount, train_remaining=training_time)

        self.session.add(tq)
        await self.session.flush()

    async def __getTrainingTime(self, troop_type: str):
        """
        Private function to get the training time of a TroopType
        """
        get_time = Select(TroopType.training_time).where(TroopType.type == troop_type)
        results = await self.session.execute(get_time)

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
        :return: time until the next update of the queue
        """

        results = await self.get_queue(building_id)
        """
        developers should be allowed to change the time, that is why seconds can be provided
        """
        if seconds is None:
            delta_time = await BuildingAccess(self.session).get_delta_time(building_id)
            seconds = delta_time.total_seconds()
        time_until_update = None
        for r in results:
            if seconds <= 0:
                break

            """
            this loop will go through the training queues
            It will take the first entry and do remaining_time -= seconds passed
            if remaining_time < 0: remove queue entry and add the troops to the army,
            If multiple troops trained add only part to army when not fully done
            """

            if config.idle_time is not None:
                unit_training_time = config.idle_time
            else:
                unit_training_time = r[1]
            queue_entry: TrainingQueue = r[0]

            """
            make sure we don't train more units than are in a queue => use min
            """
            trained = queue_entry.training_size-math.ceil((queue_entry.train_remaining - seconds)/unit_training_time)

            troops_trained = min(trained, queue_entry.training_size)
            diff = queue_entry.train_remaining - seconds
            if diff < 0:
                seconds = seconds - queue_entry.train_remaining
            else:
                queue_entry.train_remaining = diff
                seconds = 0

            time_until_update = queue_entry.train_remaining % unit_training_time

            """
            handle the trained unit changes
            """
            army_access = ArmyAccess(self.session)

            aa = ArmyAccess(self.session)
            ba = BuildingAccess(self.session)

            building_city = await ba.get_city(building_id)

            army_id = await aa.get_army_in_city(building_city.id)

            await army_access.add_to_army(army_id, queue_entry.troop_type, queue_entry.rank, troops_trained)
            queue_entry.training_size -= troops_trained
            """
            when entry done, remove training queue entry
            """
            if diff < 0:
                await self.session.delete(queue_entry)
                time_until_update = None

        """
        make a commit of the training changes and potentially removed training queue entries
        """
        await self.session.flush()
        return time_until_update

    async def get_queue(self, building_id) -> list[TrainingQueue]:
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
        results = await self.session.execute(get_queue_entries)
        results = results.all()
        return results

    async def get_troop_cost(self, troop_type: str, rank: int):
        """
        Calculate the cost of 1 unit, based on the rank the user has leveled the unit to

        :param: user_id: id of the user who wants to know the unit cost
        :param: troop_type: type of unit it wants to train
        :return: list of following format (resource_type, amount)
        """

        get_cost = Select(TroopTypeCost.resource_type, TroopTypeCost.amount).where(TroopTypeCost.troop_type == troop_type)

        resources = await self.session.execute(get_cost)
        resources = resources.all()
        ranked_cost = []

        """
        Make sure the cost depend on the rank
        """
        for r, c in resources:
            real_cost = PropertyUtility.getUnitTrainCost(c, rank)
            ranked_cost.append((r, real_cost))

        return ranked_cost


