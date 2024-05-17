import copy
from math import floor
from statistics import mean, median
import scipy
import numpy
from typing import Tuple


class PropertyUtility:
    """
    This function will do game mechanic calculations
    """

    rate = 5
    base_point_bounds: tuple[int, int] = (0, 499)
    # BORM = battle outcome random modifier
    BORM_bounds: tuple[float, float] = (1/2, 3/2)
    BORM_std: float = 0.1

    @staticmethod
    def verifyBasePoint(base_point: int):
        """
        Check that the values are inside a certain range
        """
        assert base_point >= PropertyUtility.base_point_bounds[0] and base_point <= PropertyUtility.base_point_bounds[1]

    @staticmethod
    def verifyBasePoints(base_points: list[int]):
        """
        Check that all values are in range
        """
        for base_point in base_points:
            PropertyUtility.verifyBasePoint(base_point)

    @staticmethod
    def getGPC(base_price: int, base_points: list[int]) -> int:
        """
        generate the production cost, based on the points
        """
        PropertyUtility.verifyBasePoints(base_points)
        return base_price * int(floor(
            mean(base_points) /
            mean(PropertyUtility.base_point_bounds)) ** PropertyUtility.rate)

    @staticmethod
    def getUnitTrainCost(base_price: int, level: int) -> int:
        """
        General production cost for producing units
        """
        grow_rate = 1.2

        return base_price * int((grow_rate ** level))

    @staticmethod
    def getUnitStatsRanked(base_value: int, level: int):
        """
        Get the stat of a unit after the rank is applied
        """
        grow_rate = 1.4

        return base_value * int((grow_rate ** level))

    @staticmethod
    def getGUC(creation_cost: int, level: int) -> int:
        """
        Calculate the general upgrade cost, based on the base creation cost and the level
        """
        return int((creation_cost * (level+1)) / 2)

    @staticmethod
    def getGPR(modifier: float, base_rate: int, level: int, region_control: bool) -> int:
        """
        General production rate, decides how fast resources are produced
        """
        return int(floor(modifier * base_rate * (level ** 2) * (1.0 + 0.25* int(region_control))))

    @staticmethod
    def getArmyStrength(army_stats: dict[str, int], city_weight) -> float:
        """
        Calculate the army strength
        """

        """
        The city attack and defense have a low weight
        """
        army_stats = copy.copy(army_stats)

        army_stats["city_attack"] *= city_weight
        army_stats["city_defense"] *= city_weight

        army_stats["attack"] *= (1 - city_weight)
        army_stats["defense"] *= (1 - city_weight)

        """
        make recovery less important in battle
        """
        army_stats["recovery"] = 0.4*army_stats.get("recovery", 0)

        """
        strength is mean*median, thinks makes a well bal
        """
        strength = mean(army_stats.values())
        return strength

    @staticmethod
    def getTruncNormSample(mean: float, std: float, bounds: tuple[float, float]) -> float:
        return numpy.median(scipy.stats.truncnorm.rvs((bounds[0]-mean)/std,(bounds[1]-mean)/std,loc=mean, scale=std))

    @staticmethod
    def getBattleOutcome(army_1_stats: dict[str, int], army_2_stats: dict[str, int], city_weight=0.2) -> Tuple[int, float, float]:

        """
        Calculate the battle results for a Battle between 2 armies

        param: army_1_stats: is a dictionary of the stats of an army, the keys are the names of the army
        param: army_2_stats: is a dictionary of the stats of an army, the keys are the names of the army
        """

        random_1: float = PropertyUtility.getTruncNormSample(1, PropertyUtility.BORM_std, PropertyUtility.BORM_bounds)
        random_2: float = PropertyUtility.getTruncNormSample(1, PropertyUtility.BORM_std, PropertyUtility.BORM_bounds)

        strength_1 = random_1 * PropertyUtility.getArmyStrength(army_1_stats, city_weight)
        strength_2 = random_2 * PropertyUtility.getArmyStrength(army_2_stats, city_weight)

        stats = [army_1_stats, army_2_stats]
        versus = [strength_1, strength_2]

        winner_index = versus.index(max(versus))
        strength_ratio = versus[winner_index]/max(versus[(winner_index+1) % 2], 1)
        pbr_ratio = stats[winner_index].get("recovery", 1) / max(stats[(winner_index + 1) % 2].get("recovery", 1), 1)

        return winner_index, strength_ratio, pbr_ratio

    @staticmethod
    def getCityBattleOutcome(army_1_stats: dict[str, int], army_2_stats: dict[str, int]) -> Tuple[int, float, float]:
        """
        calculate the battle outcome, but keeps into account that the city stats, have a higher weight
        """
        return PropertyUtility.getBattleOutcome(army_1_stats, army_2_stats, 0.7)

    @staticmethod
    def getSurvivedUnitsAmount(pbr_ratio: float, strength_ratio, number_of_units: int) -> int:
        """
        Calculate the survival rate of the winner based on ratio

        The strength_ratio is army_strength/enemy_army_strength
        The pbr_ratio is army_recovery/enemy_recovery

        When You are better than the enemy those ratios will each be > 1
        """

        survival: float = PropertyUtility.getTruncNormSample(min(pbr_ratio*(1 - 1/strength_ratio), 1.06), 0.1, (0, 1))
        return round(survival*number_of_units)

    @staticmethod
    def get_map_cross_time(army_speed):
        """
        Calculate the time (in seconds) needed to cross the entire planet map based on the provided army speed

        """
        map_cross_time = 1000 / army_speed * 3600
        return map_cross_time

    @staticmethod
    def get_upgrade_city_costs(upgrade_time: int, upgrade_cost: list[tuple[int,int]],level: int):
        """
        Calculate the resource cost and the time (in seconds) needed to upgrade a city

        upgrade_cost: list with base cost to upgrade a city of the form [(resource_type, amount_required),...]
        upgrade_time: base time required to upgrade a city
        level: current level of the city
        """

        resource_cost=[(cost[0],PropertyUtility.getGUC(cost[1], level)) for cost in upgrade_cost]

        time_cost = floor(upgrade_time * pow(1.15,level+1))

        return resource_cost, time_cost

    @staticmethod
    def get_building_upgrade_time(tech_forge_cost: int, level: int) -> int:
        """
        Calculate the general upgrade Time, based on the base creation cost and the level
        """
        return floor(tech_forge_cost * pow(1.15, level + 1))

class PoliticalModifiers:
    """
    Do calculations based on political modifiers
    """

    @staticmethod
    def strength_modifier(stance: dict):
        """
        Calculate the strength modifier based on the political stance
        """
        strength = 1
        strength += ((stance.get("authoritarian", 0) * 30) - (stance.get("anarchism", 0) * 20) +
                     (stance.get("theocracy", 0) * 15) - (stance.get("democratic", 0) * 10)) / 100

        return strength

    @staticmethod
    def speed_modifier(stance: dict):
        """
        Calculate the speed modifier based on the political stance
        """

        speed_modifier = 1
        speed_modifier += ((stance.get("anarchism", 0) * 10) - (stance.get("corporate_state", 0) * 30)
                           - (stance.get("theocracy", 0) * 5)) / 100
        return speed_modifier

    @staticmethod
    def production_modifier(stance: dict):
        """
        Calculate the speed modifier based on the political stance
        """

        general_production_modifier = 1
        general_production_modifier += ((stance.get("anarchism", 0) * 10) + (stance.get("democratic", 0) * 3)
                            - (stance.get("theocracy", 0) * 10) - (
                            stance.get("technocracy", 0) * 5) + (stance.get("corporate_state", 0) * 20)) / 100
        return general_production_modifier

