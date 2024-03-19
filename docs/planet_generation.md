# [Planet generation]

## Overview
How planets are generated and visualisezd

## Description
### Generation
- A PlanetRegion is defined by a singular point. The area of a region is the corresponding voronoi area. This makes our region datastructure really compact.
- For region generation a 1 by 1 square is devided in n by n cells. In each cell we take a random point inside that cell and assign a region type to that point. By doing this regions are random, but also somewhat the same size.
### Visulization
- We generate a voronoi csv from the given regionType. For every region type we cut out the image corresponding to its regionType.

## Issues
/

## Additional Information
/
