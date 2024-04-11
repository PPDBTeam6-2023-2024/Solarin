from ...app.database.database_access.data_access import DataAccess
from ...app.database.models import AttackArmy, AttackCity, EnterCity, MergeArmies
from .ArmyCombat import ArmyCombat
from ...app.routers.cityManager.city_checker import CityChecker


class ArriveCheck:
    """
    This class will make sure all information about an attack is correctly set up
    """

    @staticmethod
    async def will_attack(army_id: int, target_army_id: int, da: DataAccess):
        """

        param: army_id: the id of the army that is planning an attack
        param: target_army_id: the army we are going to attack
        """

        await da.ArmyAccess.attack_army(army_id, target_army_id)

    @staticmethod
    async def check_arrive(army_id: int, da: DataAccess):
        """
        Checks if an army is attacking something, and if so check if he arrived at his target location
        """

        target = await da.ArmyAccess.will_on_arrive(army_id)

        """
        When we attack nothing stop checking
        """
        if target is None:
            return False

        """
        When we did not yet arrive, we don't need to fight yet
        """
        arrived = await da.ArmyAccess.army_arrived(army_id)
        if not arrived:
            return False

        if isinstance(target, AttackArmy):
            await ArmyCombat.computeBattle(army_id, target.target_id, da)

        if isinstance(target, AttackCity):
            """
            Update city before calculating attack
            """
            ch = CityChecker(target.target_id, da)
            await ch.check_all()

            await ArmyCombat.computeCityBattle(army_id, target.target_id, da)

        if isinstance(target, EnterCity):
            """
            Enters the city when it arrives
            """

            """
            When army is already in city, don't add again
            """
            army_in_city = await da.ArmyAccess.get_army_in_city(target.target_id, False)
            if army_id == army_in_city:
                return

            if army_in_city is None:
                await da.ArmyAccess.enter_city(target.target_id, army_id)
            else:
                await da.ArmyAccess.merge_armies(army_in_city, target.target_id)

        if isinstance(target, MergeArmies):
            """
            Merge 2 armies when needed
            """
            await da.ArmyAccess.merge_armies(target.target_id, army_id)

        await da.ArmyAccess.cancel_attack(army_id)
        await da.commit()

        return True
