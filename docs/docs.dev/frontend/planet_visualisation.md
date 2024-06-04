# [Planet visulaisation - PlanetSVG]

## Overview
How planets are visualised, planetSVG implementation

## Description
A planet region is defined by a point and a region type. The perimeter of the region is retrieved by applying the voronoi method.

The frontend retrieves the region data. It scales all the region data to 1920x1080. Then it generates the voronoi regions using the 'd3' library. Then it cuts out the image corresponding to the region type of each voronoi cell's clippath. The images are also 1920x1080 scaled. Then it returns the PlanetSVG object with extra css styling (100vw) so it can be used inside the MapInteractionCSS. MapInteractionCSS uses the window.InnerWidth and window.InnerHeight properties to determine the size of the map and scales accordingly.

## Issues

## Additional Information
