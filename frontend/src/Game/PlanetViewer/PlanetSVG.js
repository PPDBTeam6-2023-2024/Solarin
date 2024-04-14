import {useState, useEffect, useMemo} from 'react';
import {Delaunay} from 'd3';
import axios from 'axios';

import rocks from '../Images/region_types/rocks.jpeg'
import sandyrocks from '../Images/region_types/sandyrocks.jpeg'
import darkrocks from '../Images/region_types/darkrocks.jpeg'


function GetImagePath(regionType) {
    const imagePaths = {
        type1: rocks,
        "valley of death": sandyrocks,
        "dark valley": darkrocks,
    };

    return imagePaths[regionType] || rocks;
}

function PlanetSVG(props) {
    const [data, setData] = useState([]);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await axios.get(`${process.env.REACT_APP_BACKEND_PATH}/planet/regions/${props.planetId}`);
                if (response.status === 200) {
                    setData(response.data);
                } else {
                    setData([]);
                }
            } catch (e) {
                console.error('Error getting planet regions:', e);
                setData([]);
            }
        };

        fetchData();
    }, [props.planetId]);

    const width = 1920;
    const height = 1080;

    const delaunay = useMemo(() => {
        const formattedData = data.map((d) => [width * d.x, height * d.y]);
        return Delaunay.from(formattedData);
    }, [data, width, height]);

    const voronoi = useMemo(() => {
        return delaunay.voronoi([0, 0, width, height]);
    }, [delaunay]);

    const renderClippedImages = () => {
        return data.map((d, i) => {
            const regionPath = voronoi.renderCell(i);
            const imagePath = GetImagePath(d.region_type);
            return (
                <g key={`group-${i}`}>
                    <clipPath id={`clip-${i}`}>
                        <path d={regionPath}/>
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
        <svg style={{width: "100vw", height: "auto"}} viewBox={'0 0 ' + width + ' ' + height} preserveAspectRatio="none">
            {renderClippedImages()}
            <path key="voronoi-total" d={voronoi.render()} stroke="black" strokeWidth={2}/>
        </svg>
    );
}

export default PlanetSVG;