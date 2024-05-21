import {useState, useEffect, useMemo, Fragment} from 'react';
import {Delaunay} from 'd3';
import axios from 'axios';


// get the correct image path for the given region
function GetImagePath(regionType) {
    /*
    * For each planet region type, we take the corresponding image
    * */
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
        "volcanic": "/images/region_types/volcanic.jpeg",
        "steppe": "/images/region_types/steppe.jpeg",
        "dark forest":"/images/region_types/dark_forest.jpeg"
    };

    return imagePaths[regionType] || '/images/region_types/rocks.jpeg'; // default is rocks
}

function PlanetSVG(props) {
    /**
     * This component visualizes the planet background with all its regions
     * */

    /*
    * Load the planet regions data into the data state
    * */
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

    /*
    * Predefined resolution for the map
    * */
    const width = 1920;
    const height = 1010;

    /*
    * Convert relative coordinates into absolute coordinates
    * */
    const delaunay = useMemo(() => {
        const formattedData = data.map((d) => [width * d.x, height * d.y]);
        return Delaunay.from(formattedData);
    }, [data, width, height]);

    /*
    * Regions are positioned using 1 point, using this voronoi, we can handle all its logic
    * */
    const voronoi = useMemo(() => {
        return delaunay.voronoi([0, 0, width, height]);
    }, [delaunay]);

    /*
    * Creates a clipped region. Regions are clipped based on their voronoi coverage
    * */
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
    /* calculate travel time to a coordinate in seconds (for army movement) */
    const getTravelTime = (from, to) => {
        /*to change when army speed is taken into account*/
        return Math.round(Math.hypot(to[0]-from[0], to[1]-from[1])*(100000/3600))
    }

    /*
    * Keep track of the mouse position
    * */
    const [mousePos, setMousePos] = useState([0,0]);
    return (
        <svg onPointerMove={(e) =>
            setMousePos([e.pageX / props.screenSize.current?.clientWidth,
                e.pageY / props.screenSize.current?.clientHeight])}
             style={{width: "100vw", height: "auto"}} viewBox={'0 0 ' + width + ' ' + height}
             preserveAspectRatio="none">
            {renderClippedImages()}
            <path key="voronoi-total" d={voronoi.render()} stroke="black" strokeWidth={2}/>
            {/* For the help lines when in move mode*/}
            {
                props.armiesMoveMode.map((army, i) => {
                    const armyImage = props.armyImages.find((elem) => elem.id === army);
                    return <Fragment key={i}>
                    <line stroke={"red"} strokeWidth={3} key={i} x1={armyImage.curr_x*width} y1={armyImage.curr_y*height} x2={mousePos[0]*width} y2={mousePos[1]*height}/>
                    <circle cx={mousePos[0]*width} cy={mousePos[1]*height} r={10} fill={"red"}/>
                    <text fill="white" x={(mousePos[0]+armyImage.curr_x)*width/2} y={(mousePos[1]+armyImage.curr_y)*height/2-20}>
                        {getTravelTime([armyImage.curr_x, armyImage.curr_y], mousePos)} seconds
                    </text>
                    </Fragment>
                })
            }
            {
                props.armyImages.map((army, i) => {
                        return !(army.curr_x === army.to_x && army.curr_y === army.to_y) ? <Fragment key={army.id}>
                            <line stroke={"lightblue"} strokeWidth={3} x1={army.curr_x * width}
                                  y1={army.curr_y * height} x2={army.to_x * width} y2={army.to_y * height}/>
                            <circle cx={army.to_x * width} cy={army.to_y * height} r={10} fill={"lightblue"}/>
                            <text fill="white" x={(army.to_x + army.curr_x) * width / 2}
                                  y={(army.to_y + army.curr_y) * height / 2-20}>
                                {getTravelTime([army.curr_x, army.curr_y], [army.to_x, army.to_y])} seconds
                            </text>
                        </Fragment> : <></>
                })
            }
        </svg>
    );
}

export default PlanetSVG;