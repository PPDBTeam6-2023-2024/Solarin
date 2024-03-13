import random

from . import datatypes, enums


def get_region_types(planet_type: enums.PlanetType) -> list[enums.RegionType]:
    return []


def generate_regions(
        width: int,
        height: int,
        region_types: list[enums.RegionType],
        region_scale: float
) -> list[datatypes.Region]:
    regions = []

    cell_width = int(width * region_scale)
    cell_height = int(height * region_scale)

    for j in range(0, height, cell_height):
        for i in range(0, width, cell_width):
            x = random.randint(i, i+cell_width)
            y = random.randint(j, j+cell_height)
            region = datatypes.Region(
                type=random.choice(region_types),
                coordinate=(x, y)
            )
            regions.append(region)
    return regions


def get_distance_formula(
        planet_type: enums.PlanetType
) -> datatypes.DistanceFormula:
    return datatypes.DistanceFormula.EUCLIDEAN


def generate_planet(planet_type: enums.PlanetType, width: int, region_scale: float) -> datatypes.Planet:
    height = int(width/16*9)
    region_types = get_region_types(planet_type)
    regions = generate_regions(width, height, region_types, region_scale)
    distance_formula = get_distance_formula(planet_type)

    return datatypes.Planet(
        type=planet_type,
        regions=regions,
        width=width,
        height=height,
        distance_formula=distance_formula
    )


def generate_planet_random() -> datatypes.Planet:
    return generate_planet(
        planet_type=random.choice(list(enums.PlanetType)),
        width=1920,
        region_scale=0.10
    )
