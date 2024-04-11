from typing import Optional
from math import dist

from ..models import *
from ..database import AsyncSession
from .city_access import CityAccess
from ..exceptions.permission_exception import PermissionException
from ..exceptions.invalid_action_exception import InvalidActionException


class ArmyAccess:
    """
    This class will manage the sql access for data related to information of armies
    """

    def __init__(self, session: AsyncSession):
        self.__session = session

    async def create_army(self, user_id: int, planet_id: int, x: float, y: float):
        """
        Create a new army corresponding to a user_id
        This army will spawn on the planet corresponding to the planet id
        on position x, y

        :param: user_id: the id of the user who created the army
        :param: planet_id: the id of the planet where the army will be
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

    async def add_to_army(self, army_id: int, troop_type: str, rank: int, amount: int):
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
        run a query to find the table giving the relation between troops and armies
        """
        get_entry = Select(ArmyConsistsOf).where(ArmyConsistsOf.army_id == army_id,
                                                 ArmyConsistsOf.troop_type == troop_type,
                                                 ArmyConsistsOf.rank == rank)

        results = await self.__session.execute(get_entry)
        result = results.scalar_one_or_none()

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

            result.size += amount

        """
        Flush is necessary in case multiple adds to an army are done before a commit, because we might need
        to alter the just created entry when the exact same troops are added to the army
        """
        await self.__session.flush()

    async def get_troops(self, army_id: int):
        """
        Get the troops that are part of the army

        :param: army_id: id of the army whose troops we want to retrieve
        return: list of ArmyConsistsOf objects
        """
        get_entry = Select(ArmyConsistsOf).where(ArmyConsistsOf.army_id == army_id)
        troops = await self.__session.execute(get_entry)
        return troops.scalars().all()

    async def get_army_by_id(self, army_id: int):
        """
        Get the army object corresponding to the army_id

        :param: army_id: id of the army we want to retrieve
        return: Army Object
        """
        get_entry = Select(Army).where(Army.id == army_id)
        result = await self.__session.execute(get_entry)
        army = result.scalars().first()
        return army

    async def get_user_armies(self, user_id: int):
        """
        Retrieve all armies belonging to a specific user

        :param: user_id: id of the user whose armies we want to retrieve
        return: List of Army Objects
        """
        get_entry = Select(Army).where(Army.user_id == user_id)
        armies = await self.__session.execute(get_entry)
        await self.__session.flush()
        armies = armies.scalars().all()
        return armies

    async def get_armies_on_planet(self, planet_id: int) -> list[Army]:
        """
        Get armies on a planet, but make sure not do give the armies that are inside a city

        :param: planet_id: id of the planet whose armies we want to retrieve
        return: List of Army Objects
        """

        """
        Get all the armies on the planet
        """
        get_entry = Select(Army).where(Army.planet_id == planet_id)
        armies = await self.__session.execute(get_entry)
        armies = armies.scalars().all()

        """
        Get all the armies on the planet, that are in a city
        """
        get_entry_in_city = Select(Army).join(ArmyInCity, ArmyInCity.army_id == Army.id).where(
            Army.planet_id == planet_id)
        city_armies = await self.__session.execute(get_entry_in_city)
        city_armies = city_armies.scalars().all()

        """
        Return the armies that are on the planet, but not inside a city
        """
        return list(set(armies) - set(city_armies))

    async def get_army_time_delta(self, army_id: int, distance: float, developer_speed: int = None) -> timedelta:
        """
        Calculate how long an army needs to travel a certain distance

        :param: army_id: id of the army whose time we want to calculate
        :param: distance:the distance we need to travel
        :param: developer_speed: an optional speed, making it possible for developers to manually set the time needed

        return: timedelta containing the time needed t0 travel the provided distance
        """

        """
        Get the army stats to determine the speed of an army
        """
        army_stats = await self.get_army_stats(army_id)

        """
        Calculate the travel time needed using the following formula
        
        1000/speed  (speed in range 149-350) * 3600 (= 1 hour)
        An army with a speed of 250 will take 4 hours to cross the entire map
        """

        map_cross_time = PropertyUtility.get_map_cross_time(army_stats["speed"])

        """
        let the developer speed override the calculated speed
        """
        if developer_speed is not None:
            map_cross_time = developer_speed

        return timedelta(seconds=map_cross_time * distance)

    async def change_army_direction(self, user_id: int, army_id: int, to_x: float, to_y: float) -> \
            tuple[bool, Optional[Army]]:
        """
        Change the position an army is going to.
        :param: user_id: id of the user who wants to change the army direction
        :param: army_id: id of the army whose direction we want to change
        :param: to_x, to_y: the position we want ti change to
        return: Tuple[bool, Army], Bool indicates whether the army has changed direction, and the army is the object
        itself
        """

        """
        Retrieve the army object
        """
        stmt = (
            select(Army).where(Army.id == army_id)
        )

        result = await self.__session.execute(stmt)
        army: Optional[Army] = result.scalar_one_or_none()

        """
        When the user is not the owner of the army, throw an exception
        """
        if army.user_id != user_id:
            raise PermissionException(user_id, f"change the direction of army {army_id} owned by {army.user_id}")

        """
        Calculate the difference between the army to position and its start position
        """
        x_diff = army.to_x - army.x
        y_diff = army.to_y - army.y

        """
        retrieve the current time
        """
        current_time = datetime.utcnow()

        total_time_diff = (army.arrival_time - army.departure_time).total_seconds()
        current_time_diff = (min(current_time, army.arrival_time) - army.departure_time).total_seconds()

        """
        change the army position to its current position by using linear interpolation
        
        Our army goes from A to B, over time
        current_time_diff / total_time_diff will give how much of the path is already passed
        By changing the army position (x, y) accordingly, we have the current position as army position (x, y)
        """
        if total_time_diff != 0:
            army.x += x_diff * (current_time_diff / total_time_diff)
            army.y += y_diff * (current_time_diff / total_time_diff)

        """
        change the to position to the new position
        """
        army.to_x = to_x
        army.to_y = to_y

        """
        Calculate the distance between the current position and the nwe position, and use it
        to calculate how long the army will need to move to this position (delta)
        """
        distance = dist((army.x, army.y), (army.to_x, army.to_y))
        delta = await self.get_army_time_delta(army_id, distance=distance, developer_speed=10)

        """
        Change the departure time to now and the arrival time to the moment our army will arrive
        """
        army.departure_time = current_time
        army.arrival_time = current_time + delta

        await self.__session.commit()
        await self.__session.refresh(army)

        """
        When an army was on route to attack someone, we will remove it when the army changes its position,
        because our army will not go to this target anymore
        """
        await self.cancel_attack(army_id)

        """
        Attackers cancel to, because the attacked army is not at the target location anymore,
        So the attacking army cannot combat the other army on arrival anymore
        """
        get_attackers = Select(AttackArmy).where(AttackArmy.target_id == army_id)
        results = await self.__session.execute(get_attackers)
        results = results.scalars().all()
        for r in results:
            await self.cancel_attack(r)

        return True, army

    async def attack_army(self, attack_id: int, target_id: int):
        """
        This function will make sure the database keeps in mind that an army has the intention to attack another
        army when it arrives at its position

        param: attack_id: the id of the army that is planning to attack
        param: target_id: the id of the army that will be attacked
        """

        same_owner, same_alliance = await self.check_army_relation(attack_id, target_id)
        """
        Check a user doesn't attack himself
        """
        if same_owner:
            raise InvalidActionException("You cannot attack your own army")

        """
        Check if users are not in the same alliance
        """
        if same_alliance:
            raise InvalidActionException("You cannot attack your allies")

        """
        add the attack event object to the database
        """
        attack_object = AttackArmy(army_id=attack_id, target_id=target_id)
        self.__session.add(attack_object)
        await self.__session.flush()

    async def attack_city(self, attack_id: int, target_id: int):
        """
        This function will make sure the database keeps in mind that an army has the intention to attack a city
        when it arrives at its position

        param: attack_id: the id of the army that is planning to attack
        param: target_id: the id of the city that will be attacked
        """

        """
        Check a user doesn't attack himself
        """
        city_owner = await CityAccess(self.__session).get_city_controller(target_id)
        if attack_id == city_owner:
            raise InvalidActionException("You cannot attack your own army")

        """
        add the attack event object to the database
        """
        attack_object = AttackCity(army_id=attack_id, target_id=target_id)
        self.__session.add(attack_object)
        await self.__session.flush()

    async def will_on_arrive(self, army_id):
        """
        Will return what an army will do when it arrives on this arrival position

        param: army_id: the id of the army that is planning to attack
        return: an SQL attackArmy, attackCity, mergeArmies, enterCity object or None in case we don't attack anything
        """

        get_on_arrive = Select(OnArrive).where(OnArrive.army_id == army_id)
        results = await self.__session.execute(get_on_arrive)
        result = results.scalar_one_or_none()

        """
        In case the army does nothing special when it arrives
        """
        if result is None:
            return None

        await self.__session.refresh(result)

        return result

    async def cancel_attack(self, army_id):
        """
        Cancel the on_arrive event with the target, if doing anything
        param: army_id: the id of the army whose on arrive event we want to cancel
        """
        d = delete(OnArrive).where(OnArrive.army_id == army_id)
        await self.__session.execute(d)

    async def get_army_stats(self, army_id: int, army_stats=None):
        """
        Get the stats of an army

        param: army_id: the id of the army whose stats we want to retrieve
        param: army_stats is an optional parm, In case we just want to append our stats to an already existing stats dict
        return: dict with the stats as keys and its stats as values
        """

        """
        Default initialize some basic entries, just in case this army does not have any units.
        """
        if army_stats is None:
            army_stats = {"attack": 0, "defense": 0, "city_defense": 0, "city_attack": 0}

        """
        Retrieve the troops of the army, to calculate the army stats
        """
        get_troops = Select(ArmyConsistsOf.size, ArmyConsistsOf.rank, TroopType).\
            join(TroopType, TroopType.type == ArmyConsistsOf.troop_type).where(
            ArmyConsistsOf.army_id == army_id)

        results = await self.__session.execute(get_troops)
        army_troops = results.all()

        """
        A dictionary that has all the stats of an army
        """
        total_troop_amount = 0

        for troop_tup in army_troops:
            """
            For each type of troop the army ahs, we will check it and append the army stats
            """
            troop_size = troop_tup[0]
            troop_rank = troop_tup[1]
            troop_stats = troop_tup[2].getStats(troop_rank, troop_size)

            total_troop_amount += troop_size

            for stat_name, stat_value in troop_stats.items():
                """
                Add the stat to a big dict containing all the stats of an army
                """
                val = army_stats.get(stat_name, 0)
                val += stat_value

                army_stats[stat_name] = val

        """
        Speed is expresses as a weighted average, In case no troops are present, our
        army will have a speed of 100
        """
        army_stats["speed"] = army_stats.get("speed", 100) / max(total_troop_amount, 1)

        return army_stats

    async def remove_army(self, army_id: int):
        """
        Remove the army and the troops that are a part of this army
        param: army_id: army we want to remove
        """

        s = Select(AttackArmy.army_id).where(AttackArmy.target_id == army_id)
        results = await self.__session.execute(s)
        results = results.scalars().all()

        d = delete(Army).where(Army.id == army_id)
        await self.__session.execute(d)

        """
        Proper removal (because SQL alchemy does not have cascade delete support for polymorphic tables, 
        when we need to remove the child, the parent is not removed)
        """
        for r in results:
            d = delete(OnArrive).where(OnArrive.army_id == r)
            await self.__session.execute(d)

    async def get_army_in_city(self, city_id: int) -> int:
        """
        Returns a list of army id's of armies that are inside a city
        param: city_id: the id of the city we want to check
        return: List of Army id's
        """

        armies_in_cities = Select(ArmyInCity.army_id).where(ArmyInCity.city_id == city_id)
        results = await self.__session.execute(armies_in_cities)
        result = results.scalar_one_or_none()

        if result is None:
            """
            When no army is inside the city put a default army inside the city
            """
            get_city = Select(City).where(City.id == city_id)
            city = await self.__session.execute(get_city)
            city = city.scalar_one()

            army_id = await self.create_army(city.controlled_by, city.region.planet_id, city.x, city.y)
            await self.enter_city(city.id, army_id)
            result = army_id

        return result

    async def enter_city(self, city_id: int, army_id: int):
        """
        let an army enter a city

        param: city_id: the city we want to enter
        param: army_id: the id of the army who wants to enter the city
        """

        in_city = ArmyInCity(army_id=army_id, city_id=city_id)
        self.__session.add(in_city)
        await self.__session.flush()

    async def get_army_owner(self, army_id: int) -> User:
        """
        Get the owner user of the army
        param: army_id: the id of the army whose owner we want
        return: User Object of the army owner
        """

        get_owner = Select(User).join(Army, Army.user_id == User.id).where(Army.id == army_id)
        results = await self.__session.execute(get_owner)

        result = results.scalars().first()
        return result

    async def army_arrived(self, army_id: int) -> bool:
        """
        Checks if an army is arrived at its end location
        param: army_id: the id of the army of the army we want to check
        return: all boolean indicating whether an army has already arrived
        """

        get_army = Select(Army).where(Army.id == army_id)
        results = await self.__session.execute(get_army)
        army = results.scalars().first()
        army = army

        return datetime.utcnow() > army.arrival_time

    async def get_pending_attacks(self, planet_id: int):
        """
        Get the pending attacks that are currently planned on a given planet
        param: planet_id: the id of the planet
        return: list of army_id's of attackers and their time of arrival
        """

        get_attackers = Select(OnArrive.army_id, Army.arrival_time).join(Army, OnArrive.army_id == Army.id).where(
            Army.planet_id == planet_id)
        results = await self.__session.execute(get_attackers)
        results = results.all()
        return results

    async def merge_armies(self, army_id: int, from_army_id):
        """
        Merge 2 armies
        param: army_id: is the army that will become stronger (added to)
        param: from_army_id: is the army that will give his units away
        """

        """
        Update the army ID's of the ArmyConsistOf to transfer the units
        But in case those entries already exist we just need to add values,
        So we will just 'add' our units to the first army
        """

        get_from_units = Select(ArmyConsistsOf).where(ArmyConsistsOf.army_id == from_army_id)
        from_troops = await self.__session.execute(get_from_units)
        from_troops = from_troops.scalars().all()

        """
        Add the units to the army
        """
        for ac in from_troops:
            await self.add_to_army(army_id, ac.troop_type, ac.rank, ac.size)

        """
        Remove original army
        """
        await self.remove_army(from_army_id)

    async def add_merge_armies(self, army_id: int, target_id: int):
        """
        This function will make sure the database keeps in mind that an army has the intention to merge with another
        army when it arrives at its position

        param: army_id: the id of the army that is planning to attack
        param: target_id: the id of the army that will be attacked
        """

        same_owner, same_alliance = await self.check_army_relation(army_id, target_id)
        """
        Check a user doesn't attack himself
        """
        if not same_owner:
            raise InvalidActionException("You cannot merge with another user their army")

        """
        Add army on arrive event to database
        """
        merge_object = MergeArmies(army_id=army_id, target_id=target_id)
        self.__session.add(merge_object)
        await self.__session.flush()

    async def add_enter_city(self, army_id: int, target_id: int):
        """
        This function will make sure the database keeps in mind that an army has the intention to enter a city
        when it arrives at its position

        param: army_id: the id of the army that is planning to attack
        param: target_id: the id of the city that will be attacked
        """

        """
        Check a user doesn't enter someone else their city
        """
        city_owner = await CityAccess(self.__session).get_city_controller(target_id)
        army: Army = await ArmyAccess(self.__session).get_army_by_id(army_id)

        if army.user_id != city_owner.id:
            raise InvalidActionException("You enter someone else their city")

        """
        Add army on arrive event to database
        """
        enter_object = EnterCity(army_id=army_id, target_id=target_id)
        self.__session.add(enter_object)
        await self.__session.flush()

    async def leave_city(self, army_id: int):
        """
        Let an army leave the city

        param: army_id: the id of the army that is planning to leave the city
        """

        d = delete(ArmyInCity).where(ArmyInCity.army_id == army_id)
        await self.__session.execute(d)

    async def check_army_relation(self, army_1: int, army_2: int) -> tuple[bool, bool]:
        """
        Determine the underlining relation between 2 armies

        param: army_1: the id of the army that want to check the relation
        param: army_2: the id of the army that want to check the relation
        return: Tuple[boll, bool],
        first bool indicates  whether the armies have the same owner,
        the second whether they are in the same alliance
        """

        """
        retrieve both users corresponding to the armies (being the owners of these armies)
        """
        army_owner = Select(User).join(Army, Army.user_id == User.id).where(
            (Army.id == army_1) | (Army.id == army_2))
        results = await self.__session.execute(army_owner)
        results = results.scalars().all()

        if len(results) != 2:
            raise Exception("One of the provided armies does not exist")

        same_owner = results[0].id == results[1].id
        same_alliance = results[0].alliance == results[1].alliance and results[0].alliance is not None

        return same_owner, same_alliance
