from math import floor
from statistics import mean


class PropertyUtility():
    rate: int = 5
    base_point_bounds: tuple[int, int] = (0, 499)

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
        return int(floor((creation_cost * level) / 2))

    @staticmethod
    def getGPR(modifier: float, base_rate: int, level: int) -> int:
        return int(floor(modifier * base_rate * (level ** 2)))

    @staticmethod
    def getUnitStrength(self, current_points: list[int], unit_rank: int) -> float:
        return (unit_rank*mean(current_points))/(mean(PropertyUtility.base_point_bounds))
    
