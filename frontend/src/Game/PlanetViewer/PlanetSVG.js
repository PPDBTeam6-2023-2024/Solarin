import { useMemo } from 'react';
import { Delaunay } from 'd3'; 

import rocks from '../Images/region_types/rocks.jpeg'
import sandyrocks from '../Images/region_types/sandyrocks.jpeg'
import darkrocks from '../Images/region_types/darkrocks.jpeg'


function getImagePath(regionType) {
    const imagePaths = {
        type1:  rocks,
        type2:  sandyrocks,
        type3:  darkrocks,
    };

    return imagePaths[regionType] || rocks;
}

function PlanetSVG(props) {    
    const width = 1920;
    const height = 1080;

    const delaunay = useMemo(() => {
        const formattedData = props.data.map((d) => [width*d.x, height*d.y]);
        return Delaunay.from(formattedData);
    }, [props.data, width, height]);


    const voronoi = useMemo(() => {
        return delaunay.voronoi([0, 0, width, height]);
      }, [delaunay]);

    const renderClippedImages = () => {
        return props.data.map((d, i) => {
            const regionPath = voronoi.renderCell(i);
            const imagePath = getImagePath(d.regionType);
            return (
                <g key={`group-${i}`}>
                    <clipPath id={`clip-${i}`}>
                        <path d={regionPath} />
                    </clipPath>
                    <image
                        key={`image-${i}`}
                        xlinkHref={imagePath}
                        clipPath={`url(#clip-${i})`}
                        width={width}
                        height={height}
                        preserveAspectRatio="none"
                        onError={(e) => console.error(`Error loading image: ${imagePath}`, e)}
                    />
                </g>
            );
        });
    };

    return (
        <svg width="100%" height="100%" viewBox={'0 0 ' + width + ' ' + height} preserveAspectRatio="none">
            {renderClippedImages()}
            <path key="voronoi-total" d={voronoi.render()} stroke="black" strokeWidth={2} />
        </svg>
    );
}

export default PlanetSVG;