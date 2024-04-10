from ..utils.compute_properties import *
from ...app.database.database_access.data_access import DataAccess


class ArmyCombat:
    """
    This class will make sure that combat between 2 armies occurs correctly
    """

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
        await da.ArmyAccess.remove_army(loser)

        army_troops = await da.ArmyAccess.get_troops(winner)

        """
        Change the surviving amount of units
        """
        for army_troop in army_troops:
            army_troop[0].size = PropertyUtility.getSurvivedUnitsAmount(pbr_ratio, strength_ratio, army_troop[0].size)
        await da.commit()

    @staticmethod
    async def computeCityBattle(army_1: int, city_id: int, da: DataAccess):
        """
        Compute the result of a battle an attack army and a defending city
        """
        city_stats = await da.CityAccess.get_cities_stats(city_id)

        city_armies = await da.ArmyAccess.get_army_in_city(city_id)
        """
        Calculate the stats based on all the armies that are inside the city
        """
        for c_army_id in city_armies:
            city_stats = await da.ArmyAccess.get_army_stats(c_army_id, city_stats)

        army_stats_1 = await da.ArmyAccess.get_army_stats(army_1)
        winner_index, strength_ratio, pbr_ratio = PropertyUtility.getBattleOutcome(army_stats_1, city_stats)

        if winner_index == 0:
            loss_list = [army_1]

            """
            Remove all armies inside a city if the city defense loses
            """
            for c in city_armies:
                await da.ArmyAccess.remove_army(c)

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
            await da.ArmyAccess.remove_army(army_1)
            loss_list = city_armies

        """
        change the casualties
        """
        for l in loss_list:
            army_troops = await da.ArmyAccess.get_troops(l)

            """
            Change the surviving amount of units
            """
            for army_troop in army_troops:
                army_troop[0].size = PropertyUtility.getSurvivedUnitsAmount(pbr_ratio, strength_ratio,
                                                                            army_troop[0].size)

        await da.commit()