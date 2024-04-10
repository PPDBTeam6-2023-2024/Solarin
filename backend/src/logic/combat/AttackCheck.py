from ...app.database.database_access.data_access import DataAccess
from ...app.database.models import AttackArmy, AttackCity
from .ArmyCombat import ArmyCombat


class AttackCheck:
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
    async def check_attack(army_id: int, da: DataAccess):
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
            await ArmyCombat.computeCityBattle(army_id, target.target_id, da)
        return True
