from statistics import mean
from math import floor
from random import choice
class LogicUtility():
    @staticmethod
    def compute_strength(points: list[int], rank: int) -> int:
        return rank*floor(mean(points))

