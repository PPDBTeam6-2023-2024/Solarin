from datetime import datetime
from typing import Optional
from math import dist

from ..models.models import *
from ..database import AsyncSession


class ArmyAccess:
    """
    This class will manage the sql access for data related to information of armies
    """
    def __init__(self, session: AsyncSession):
        self.__session = session

    async def createArmy(self, user_id: int, planet_id: int, x: float, y: float):
        """
        Create a new army corresponding to a user_id

        :param: user_id: the id of the user who created the army
        :return: army_id: id of the army that was just generated
        """
        army = Army(
            user_id=user_id,
            planet_id=planet_id,
            x=x,
            y=y,
            to_x=x,
            to_y=y
        )
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

    async def getArmies(self, userid: int, planetid: int):
        getentry = Select(Army).where(Army.user_id==userid)
        armies = await self.__session.execute(getentry)
        await self.__session.flush()
        return armies

    async def getTroops(self, armyid: int):
        getentry = Select(ArmyConsistsOf).where(ArmyConsistsOf.army_id==armyid)
        troops = await self.__session.execute(getentry)
        await self.__session.flush()
        return troops.all()

    async def getArmyById(self, army_id: int):
        getentry = Select(Army).where(Army.id==army_id)
        result = await self.__session.execute(getentry)
        await self.__session.flush()
        army = result.first()
        return army

    async def updateArmyCoordinates(self, army_id: int, x, y):
        getentry = Select(Army).where(Army.id==army_id)
        result = await self.__session.execute(getentry)
        army = result.scalars().first()

        if army is None:
            return False

        army.x = x
        army.y = y

        await self.__session.commit()
        return True

    async def getUserArmies(self, userid: int):
        getentry = Select(Army).where(Army.user_id==userid)
        armies = await self.__session.execute(getentry)
        await self.__session.flush()
        armies = armies.all()
        return armies

    async def get_armies_on_planet(self, planet_id: int) -> list[Army]:
        stmt = (
            select(Army)
            .where(Army.planet_id == planet_id)
        )
        result = await self.__session.execute(stmt)
        return result.scalars().all()

    async def get_army_time_delta(self, army_id: int, distance: float) -> timedelta:
        # TODO: make speed army specific
        return timedelta(seconds=10*distance)

    async def change_army_direction(self, user_id: int, army_id: int, to_x: float, to_y: float) -> tuple[bool, Optional[Army]]:
        stmt = (
            select(Army)
            .where(Army.user_id == user_id)
            .where(Army.id == army_id)
        )
        result = await self.__session.execute(stmt)
        army: Optional[Army] = result.scalar_one_or_none()

        if not army:
            return False, None

        current_time = datetime.utcnow()

        total_time_diff = (army.arrival_time - army.departure_time).total_seconds()
        current_time_diff = (min(current_time, army.arrival_time) - army.departure_time).total_seconds()

        x_diff = army.to_x - army.x
        y_diff = army.to_y - army.y

        current_x = x_diff * (current_time_diff / total_time_diff)
        current_y = y_diff * (current_time_diff / total_time_diff)

        army.x = current_x
        army.y = current_y
        army.to_x = to_x
        army.to_y = to_y

        distance = dist((current_x, current_y), (to_x, to_y))
        delta = await self.get_army_time_delta(army_id, distance=distance)

        army.departure_time = current_time
        army.arrival_time = current_time + delta

        await self.__session.commit()
        await self.__session.refresh(army)
        return True, army
