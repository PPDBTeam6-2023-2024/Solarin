import {useState, useEffect, useMemo} from 'react';
import {Delaunay} from 'd3';
import axios from 'axios';


// get the correct image path for the given region
function GetImagePath(regionType) {
    const imagePaths = {
        "valley of shadow": '/images/region_types/valley_of_shadow.jpeg',
        "arctic": '/images/region_types/arctic.jpg',
        "plain": '/images/region_types/plain.jpeg',
        "magma": '/images/region_types/magma.jpg',
        "savannah": '/images/region_types/savannah.jpg',
        "silicaat": '/images/region_types/silicaat.jpg',
        "alpine": "/images/region_types/alpine.jpg",
        "desert": "/images/region_types/desert.jpg",
        "taiga": "/images/region_types/taiga.jpg",
        "polar": "/images/region_types/polar.jpg",
        "rainforest": "/images/region_types/rainforest.jpeg",
        "volcanic": "/images/region_types/volcanic.jpeg"
    };

    return imagePaths[regionType] || '/images/region_types/rocks.jpeg'; // default is rocks
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
                        href={imagePath}
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
        <svg style={{width: "100vw", height: "auto"}} viewBox={'0 0 ' + width + ' ' + height}
             preserveAspectRatio="none">
            {renderClippedImages()}
            <path key="voronoi-total" d={voronoi.render()} stroke="black" strokeWidth={2}/>
        </svg>
    );
}

export default PlanetSVG;