from math import floor
from statistics import mean, median
import scipy
import numpy


class PropertyUtility:
    rate: int = 5
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
    def getGUC(creation_cost: int, level: int) -> int:
        return int(floor((creation_cost * (level+1)) / 2))

    @staticmethod
    def getGPR(modifier: float, base_rate: int, level: int) -> int:
        return int(floor(modifier * base_rate * (level ** 2)))

    @staticmethod
    def getUnitStrength(current_points: list[int], unit_rank: int) -> float:
        return (unit_rank*mean(current_points))/(mean(PropertyUtility.base_point_bounds))

    @staticmethod
    def getUnitCityStrength(non_city_points: list[int], city_points: list[int], unit_rank: int) -> float:
        return (unit_rank*(0.5*mean(non_city_points)+mean(city_points))) / mean(PropertyUtility.base_point_bounds)

    @staticmethod
    def getArmyStrength(units: list[list[dict[str, int]]]) -> float:
        return mean(list(map(lambda unit:PropertyUtility.getUnitStrength(unit["non_city_points"]+unit["city_points"], unit["rank"]), units)))

    @staticmethod
    def getArmyCityStrength(units: list[list[dict[str, int]]]) -> float:
        return mean(list(map(lambda unit:PropertyUtility.getUnitCityStrength(unit["non_city_points"], unit["city_points"], unit["rank"]), units)))

    @staticmethod
    def getTruncNormSample(mean: float, std: float, bounds: tuple[float, float]) -> float:
        return numpy.median(scipy.stats.truncnorm.rvs((bounds[0]-mean)/std,(bounds[1]-mean)/std,loc=mean, scale=std))
    @staticmethod
    def getBattleOutcome(army_1: list[list[dict[str, int]]], army_2: list[list[dict[str, int]]]) -> int:
        random_1: float = PropertyUtility.getTruncNormSample(1, PropertyUtility.BORM_std, PropertyUtility.BORM_bounds)
        random_2: float = PropertyUtility.getTruncNormSample(1, PropertyUtility.BORM_std, PropertyUtility.BORM_bounds)
        versus = [random_1*PropertyUtility.getArmyStrength(army_1), random_2*PropertyUtility.getArmyStrength(army_2)]
        return versus.index(max(versus))+1

    @staticmethod
    def getCityBattleOutcome(army_1: list[list[dict[str, int]]], army_2: list[list[dict[str, int]]]) -> int:
        random_1: float = PropertyUtility.getTruncNormSample(1, PropertyUtility.BORM_std, PropertyUtility.BORM_bounds)
        random_2: float = PropertyUtility.getTruncNormSample(1, PropertyUtility.BORM_std, PropertyUtility.BORM_bounds)
        versus = [random_1*PropertyUtility.getArmyCityStrength(army_1), random_2*PropertyUtility.getArmyCityStrength(army_2)]
        return versus.index(max(versus))+1

    @staticmethod
    def getSurvivedUnitsAmount(pbr: int, number_of_units: int) -> int:
        survival : float = PropertyUtility.getTruncNormSample(pbr/PropertyUtility.base_point_bounds[1], 0.1, (0,1))
        return int(round(survival*number_of_units))
