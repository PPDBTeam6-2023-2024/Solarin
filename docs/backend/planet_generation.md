# [Planet generation]

## Overview
How planets are generated

## Description
A planet region is defined by a point and a region type. The perimeter of the region is retrieved by applying the voronoi method.

- To generate a random planet call this function `generate_random_planet(session: AsyncSession, space_region_id: int)` it is inside src/app/routers/spawn/planet_generation.py. This method will generate a random planet_region. From this planet_region it will generate a 10 x 10 grid. In each grid a random point is picked and a random region type is selected. This region type corresponds to the previously retrieved planet type. This function will return the id of the generated planet.

## Issues
- The space region id must exits.

## Additional Information
- This feature is fully tested using pytest.