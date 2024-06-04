from ..formula.compute_properties import *
from ...app.database.database_access.data_access import DataAccess

from ...app.routers.globalws.router import global_queue


class ArmyCombat:
    """
    This class will make sure that combat between 2 armies occurs correctly
    """
    @staticmethod
    async def handle_death(user_id: int, da: DataAccess):
        """
        Handle the death of a user
        """
        if await da.UserAccess.is_dead(user_id):
            await global_queue.put({"target": user_id, "type": "death"})

    @staticmethod
    async def computeBattle(army_1: int, army_2: int, da: DataAccess):
        """
        Compute the result of a battle between 2 armies
        """

        army_stats_1 = await da.ArmyAccess.get_army_stats(army_1)
        army_stats_2 = await da.ArmyAccess.get_army_stats(army_2)

        winner_index, strength_ratio, pbr_ratio = PropertyUtility.getBattleOutcome(army_stats_1, army_stats_2)
        army_tup = (army_1, army_2)

        winner = army_tup[winner_index]
        loser = army_tup[(winner_index+1) % 2]

        """
        remove lost army, and give combat losses to winning army
        """
        winner_id = (await da.ArmyAccess.get_army_owner(winner)).id
        loser_id = (await da.ArmyAccess.get_army_owner(loser)).id
        await da.ArmyAccess.remove_army(loser)

        army_troops = await da.ArmyAccess.get_troops(winner)

        """
        Change the surviving amount of units
        """
        for army_troop in army_troops:
            army_troop.size = PropertyUtility.getSurvivedUnitsAmount(pbr_ratio, strength_ratio, army_troop.size)

            """
            When troop type has 0 troops, remove entry
            """
            if army_troop.size == 0:
                await da.ArmyAccess.remove_troop(army_troop)

        await da.commit()

        await global_queue.put({"target": winner_id, "won": True, "own_target": f"army {winner}",
                                "other_target": f"army {loser}", "type": "combat_notification"})
        await global_queue.put({"target": loser_id, "won": False, "own_target": f"army {loser}",
                                "other_target": f"army {winner}", "type": "combat_notification"})

        await ArmyCombat.handle_death(loser_id, da)

    @staticmethod
    async def computeCityBattle(army_1: int, city_id: int, da: DataAccess):
        """
        Compute the result of a battle an attack army and a defending city
        """
        city_stats = await da.CityAccess.get_cities_stats(city_id)

        c_army_id = await da.ArmyAccess.get_army_in_city(city_id)
        """
        Calculate the stats based on the army that is inside the city
        """
        city_stats = await da.ArmyAccess.get_army_stats(c_army_id, city_stats)

        army_stats_1 = await da.ArmyAccess.get_army_stats(army_1)
        winner_index, strength_ratio, pbr_ratio = PropertyUtility.getBattleOutcome(army_stats_1, city_stats)

        if winner_index == 0:
            loss_army = army_1

            win_target = f"army {army_1}"
            loss_target = f"city {city_id}"

            """
            Remove the army inside a city if the city defense loses
            """
            winner_id = (await da.ArmyAccess.get_army_owner(army_1)).id
            loser_id = (await da.ArmyAccess.get_army_owner(c_army_id)).id
            await da.ArmyAccess.remove_army(c_army_id)

            """
            Let user become new owner of the city
            """
            owner = await da.ArmyAccess.get_army_owner(army_1)
            await da.CityAccess.set_new_controller(city_id, owner.id)

            """
            The conquering army will enter the city
            """
            await da.ArmyAccess.enter_city(city_id, army_1)

        else:
            win_target = f"city {city_id}"
            loss_target = f"army {army_1}"

            winner_id = (await da.ArmyAccess.get_army_owner(c_army_id)).id
            loser_id = (await da.ArmyAccess.get_army_owner(army_1)).id
            await da.ArmyAccess.remove_army(army_1)
            loss_army = c_army_id

        """
        change the casualties
        """
        army_troops = await da.ArmyAccess.get_troops(loss_army)

        """
        Change the surviving amount of units
        """
        for army_troop in army_troops:
            army_troop.size = PropertyUtility.getSurvivedUnitsAmount(pbr_ratio, strength_ratio,
                                                                     army_troop.size)

            """
            When troop type has 0 troops, remove entry
            """
            if army_troop.size == 0:
                await da.ArmyAccess.remove_troop(army_troop)

        await da.commit()

        await global_queue.put({"target": winner_id, "won": True, "own_target": win_target,
                                "other_target": loss_target, "type": "combat_notification"})
        await global_queue.put({"target": loser_id, "won": False, "own_target": loss_target,
                                "other_target": win_target, "type": "combat_notification"})

        await ArmyCombat.handle_death(loser_id, da)
