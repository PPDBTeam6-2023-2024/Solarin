from ...app.database.database_access.data_access import DataAccess
from ...app.database.models import AttackArmy, AttackCity, EnterCity, MergeArmies, EnterPlanet
from .ArmyCombat import ArmyCombat
from ...app.routers.cityManager.city_checker import CityChecker
from ...app.routers.logic.maintenance_socket_actions import MaintenanceSocketActions


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

        target_id = target.target_id

        """
        When we did not yet arrive, we don't need to fight yet
        """
        arrived = await da.ArmyAccess.army_arrived(army_id)
        if not arrived:
            return False

        if isinstance(target, AttackArmy):
            owner = await da.ArmyAccess.get_army_owner(target.target_id)

            """
            Update maintenance status of the target user
            """
            m = MaintenanceSocketActions(owner.id, da)
            await m.check_maintenance(False)

            """
            Update maintenance status of the attacker user
            """
            owner = await da.ArmyAccess.get_army_owner(army_id)
            m = MaintenanceSocketActions(owner.id, da)
            await m.check_maintenance(False)

            await ArmyCombat.computeBattle(army_id, target.target_id, da)

        if isinstance(target, AttackCity):
            """
            Update city before calculating attack
            """
            await da.session.flush()
            ch = CityChecker(target.target_id, da)
            await ch.check_all()
            await da.session.flush()

            """
            Update maintenance status of the target user
            """
            owner = await da.CityAccess.get_city_controller(target_id)
            m = MaintenanceSocketActions(owner.id, da)
            await m.check_maintenance(False)

            """
            Update maintenance status of the attacker user
            """
            owner = await da.ArmyAccess.get_army_owner(army_id)
            m = MaintenanceSocketActions(owner.id, da)
            await m.check_maintenance(False)

            await ArmyCombat.computeCityBattle(army_id, target_id, da)

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
                await da.ArmyAccess.merge_armies(army_in_city, army_id)

        if isinstance(target, EnterPlanet):
            """
            Enters the planet when it arrives
            """

            """
            When army is already in planet, don't add again
            """
            armies_on_planet = await da.ArmyAccess.get_armies_on_planet(target.target_id)
            if army_id in armies_on_planet:
                return

            await da.ArmyAccess.enter_planet(target.target_id, army_id)

        if isinstance(target, MergeArmies):
            """
            Merge 2 armies when needed
            """
            await da.ArmyAccess.merge_armies(target.target_id, army_id)

        await da.ArmyAccess.cancel_attack(army_id)
        await da.commit()

        return True
