from enum import Enum


class PlanetType(Enum):
    ...


class RegionType(Enum):
    ...


class DistanceFormula(Enum):
    CHEBYSHEV="chebyshev"
    EUCLIDEAN="euclidean"
    CITYBLOCK="cityblock"
