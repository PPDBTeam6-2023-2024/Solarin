from sqlalchemy.ext.asyncio import AsyncSession
import random

from ...database.database_access.planet_access import PlanetAccess


def generate_regions(regions: list[str], row_col_count: int = 10) -> dict[str, list[tuple[float, float]]]:
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
    planet_access = PlanetAccess(session)

    random_planet_type_row = await planet_access.get_random_planet_type()

    planet_type = random_planet_type_row[0].type
    planet_id = await planet_access.createPlanet(
        planet_name="test",
        planet_type=planet_type,
        space_region_id=0
    )

    planet_region_types = await planet_access.get_planet_region_types(planet_type)

    planet_region_types = [region[0].region_type for region in planet_region_types]
    regions = generate_regions(planet_region_types)

    for region_type, coordinates in regions.items():
        for coordinate in coordinates:
            await planet_access.createPlanetRegion(
                planet_id=planet_id,
                region_type=region_type,
                coordinate=coordinate
            )

    return planet_id
