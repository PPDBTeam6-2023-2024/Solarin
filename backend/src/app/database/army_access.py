from .models import *
from .database import AsyncSession


class ArmyAccess:
    """
    This class will manage the sql access for data related to information of armies
    """
    def __init__(self, session: AsyncSession):
        self.__session = session

    async def createArmy(self, user_id: int):
        """
        Create a new army corresponding to a user_id

        :param: user_id: the id of the user who created the army
        :return: army_id: id of the army that was just generated
        """
        army = Army(user_id=user_id)
        self.__session.add(army)
        await self.__session.flush()
        return army.id

    async def addToArmy(self, army_id: int, troop_type: str, rank: int, amount: int):
        """
        Check if the ArmyConsistsOf does already contain an entry for (amry_id, trooptype, rank)
        If so: increase the amount by the given amount
        If not: add a new entry containing the given information

        :param: army_id: id of the army we want to add our troops to
        :param: troop_type: the type of troop we want to add to our army
        :param: rank: rank of the troop
        :param: amount: the amount of troops we add to this army
        :return: nothing
        """

        """
        run a query to find the table given the relation between troops and armies
        """
        get_entry = Select(ArmyConsistsOf).where(ArmyConsistsOf.army_id==army_id,
                                                 ArmyConsistsOf.troop_type==troop_type,
                                                 ArmyConsistsOf.rank == rank)

        results = await self.__session.execute(get_entry)
        result = results.first()

        """
        verify whether the entry (giving the specific relation) existed
        """
        if result is None:
            """
            In case no entry is yet present:
            We will create a new entry
            """
            army_consists_of = ArmyConsistsOf(army_id=army_id, troop_type=troop_type, rank=rank, size=amount)
            self.__session.add(army_consists_of)

        else:
            """
            In case an entry is present:
            We will increase the amount of the entry with the provided amount
            """

            result[0].size += amount

        """
        Flush is necessary in case multiple adds to an army are done before a commit, because we might need
        to alter the just created entry when the exact same troops are added to the army
        """
        await self.__session.flush()
