import { useMemo } from 'react';
import { Delaunay } from 'd3'; 
import * as d3 from "d3";

function getImagePath(regionType) {
    const imagePaths = {
        type1: 'https://dfstudio-d420.kxcdn.com/wordpress/wp-content/uploads/2019/06/digital_camera_photo-1080x675.jpg',
        type2: 'https://letsenhance.io/static/8f5e523ee6b2479e26ecc91b9c25261e/1015f/MainAfter.jpg',
        type3: 'https://upload.wikimedia.org/wikipedia/commons/b/b6/Image_created_with_a_mobile_phone.png',
    };

    return imagePaths[regionType] || '.Game/Images/Planets/example.png';
}

function PlanetViewer(props) {
    const xScale = d3.scaleLinear().domain([0, 1]).range([0, props.width]);
    const yScale = d3.scaleLinear().domain([0, 1]).range([0, props.height]);

    const delaunay = useMemo(() => {
        const formattedData = props.data.map((d) => [xScale(d.x), yScale(d.y)]);
        return Delaunay.from(formattedData);
    }, [props.data, xScale, yScale]);

    const voronoi = useMemo(() => {
        return delaunay.voronoi([0, 0, props.width, props.height]);
      }, [props.width, props.height, delaunay]);

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
                        // href={imagePath}
                        clipPath={`url(#clip-${i})`}
                        width={props.width}
                        height={props.height}
                        onError={(e) => console.error(`Error loading image: ${imagePath}`, e)}
                    />
                </g>
            );
        });
    };

    return (
        <svg width={props.width} height={props.height}>
            {renderClippedImages()}
            <path key={`voronoi-total`} d={voronoi.render()} stroke="orange" fill="none" />
        </svg>
    );
}

export default PlanetViewer;
