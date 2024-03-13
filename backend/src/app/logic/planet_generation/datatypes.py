from dataclasses import dataclass
from typing import Tuple, Iterable

from .enums import RegionType, PlanetType, DistanceFormula


@dataclass
class Region:
    type: RegionType
    coordinate: Tuple[float, float]


@dataclass
class Planet:
    type: PlanetType
    regions: Iterable[Region]
    distance_formula: DistanceFormula


