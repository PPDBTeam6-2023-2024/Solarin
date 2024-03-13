from dataclasses import dataclass
from typing import Tuple, Iterable


@dataclass
class Region:
    type: str
    coordinate: Tuple[float, float]


@dataclass
class Planet:
    type: str
    regions: Iterable[Region]


