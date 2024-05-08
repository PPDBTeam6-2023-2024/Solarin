from sqlalchemy.ext.asyncio import AsyncSession
import random
import math

from ...database.database_access.planet_access import PlanetAccess
from ....logic.name_generator.random_name_generator import generate_planet_name


def fibonacci_spiral_point(index):
    """
    Generate a point on the fibonacci spiral depending on the index
    """
    theta = index * (math.pi / 2 + math.sqrt(5))  
    r = math.sqrt(index)
    r *= 0.5
    x = r * math.cos(theta)
    y = r * math.sin(theta)
    return x, y


def generate_regions(regions: list[str], row_col_count: int = 5) -> dict[str, list[tuple[float, float]]]:
    """
    Generate random points on the map.
    1 point represents a region. Using voronoi, we can see which region a position is in, by searching
    for the closest region coordinate
    """
    regions_dict = {region_type: [] for region_type in regions}
    cell_size = 1 / row_col_count

    for i in range(row_col_count):
        for j in range(row_col_count):
            region_type = random.choice(regions)
            x = random.uniform(i * cell_size, (i + 1) * cell_size)
            y = random.uniform(j * cell_size, (j + 1) * cell_size)
            regions_dict[region_type].append((x, y))

    return regions_dict


async def generate_random_planet(session: AsyncSession) -> int:
    """
    Function we use to create a new planet (in a random manner)
    """

    planet_access = PlanetAccess(session)

    """
    Choose a random planet type
    """
    random_planet_type_row = await planet_access.get_random_planet_type()
    new_index = await planet_access.get_planets_amount()
    
    x, y = fibonacci_spiral_point(new_index + 1)


    """
    Create the planet
    """
    planet_type = random_planet_type_row.type
    planet_id = await planet_access.create_planet(
        planet_name=generate_planet_name(),
        planet_type=planet_type,
        x=x,
        y=y
    )

    """
    Retrieve the region types, that can exist on a planet of its type
    """
    planet_region_types = await planet_access.get_planet_region_types(planet_type)

    planet_region_types = [region.region_type for region in planet_region_types]

    """
    Generate the regions
    """
    regions = generate_regions(planet_region_types)

    """
    Store the regions in the database
    """
    for region_type, coordinates in regions.items():
        for x,y in coordinates:
            await planet_access.create_planet_region(
                planet_id=planet_id,
                region_type=region_type,
                x=x,
                y=y
            )

    return planet_id
