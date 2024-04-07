import copy
from math import floor
from statistics import mean, median
import scipy
import numpy
from typing import Tuple


class PropertyUtility:
    rate = 5
    base_point_bounds: tuple[int, int] = (0, 499)
    # BORM = battle outcome random modifier
    BORM_bounds: tuple[float, float] = (1/2, 3/2)
    BORM_std: float = 0.1

    @staticmethod
    def verifyBasePoint(base_point: int):
        assert base_point >= PropertyUtility.base_point_bounds[0] and base_point <= PropertyUtility.base_point_bounds[1]

    @staticmethod
    def verifyBasePoints(base_points: list[int]):
        for base_point in base_points:
            PropertyUtility.verifyBasePoint(base_point)

    @staticmethod
    def getGPC(base_price: int, base_points: list[int]) -> int:
        PropertyUtility.verifyBasePoints(base_points)
        return base_price * int(floor(
            mean(base_points) /
            mean(PropertyUtility.base_point_bounds)) ** PropertyUtility.rate
                                )

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
        return int(floor((creation_cost * level) / 2))

    @staticmethod
    def getGPR(modifier: float, base_rate: int, level: int) -> int:
        """
        General production rate, decides how fast resources are produced
        """
        return int(floor(modifier * base_rate * (level ** 2)))

    @staticmethod
    def getUnitStrength(current_points: list[int], unit_rank: int) -> float:
        """
        Units have a lot of modifiers, the mean of these modifiers will be taken to calculate
        the strength of the amry
        """
        return (unit_rank*mean(current_points))/(mean(PropertyUtility.base_point_bounds))

    @staticmethod
    def getUnitCityStrength(non_city_points: list[int], city_points: list[int], unit_rank: int) -> float:
        return (unit_rank*(0.5*mean(non_city_points)+mean(city_points))) / mean(PropertyUtility.base_point_bounds)

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