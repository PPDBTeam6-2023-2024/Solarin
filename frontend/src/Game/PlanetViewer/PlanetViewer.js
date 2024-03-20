import { MapInteractionCSS } from 'react-map-interaction';
import {useState, useEffect, useContext} from 'react';
import { RiArrowLeftSLine, RiArrowRightSLine } from "react-icons/ri";
import getCities from './CityViewer/getCities';
import CityManager from "./CityViewer/cityManager";
import {PlanetListContext} from "./../Context/PlanetListContext"
import ArmyViewer from '../UI/armyViewer/armyViewer'
import getArmies from "./getArmies";

const loadImage = async (imgPath, stateSetter) => {
    let img = new Image()
    img.src = imgPath
    img.onload = () => {
        stateSetter(img)
    }
}

function PlanetViewer(props) {

    const [mapState, setMapState] = useState({
        scale: 1,
        translation: {x: 0, y: 0},
    });
    const [image, setImage] = useState();
    const [armyImages, setArmyImages] = useState([]);
    const [activeArmyViewers, setActiveArmyViewers] = useState([]);
    const [updateTrigger, setUpdateTrigger] = useState(false);


    const toggleArmyViewer = (e, armyId) => {
        const overlayRect = e.target.getBoundingClientRect();
        const position = {
            x: overlayRect.left + window.scrollX,
            y: overlayRect.top + window.scrollY
        };

        setActiveArmyViewers(prev => {
            const index = prev.findIndex(viewer => viewer.id === armyId);
            if (index >= 0) {
                // Remove viewer if already active
                return prev.filter(viewer => viewer.id !== armyId);
            } else {
                return [...prev, {id: armyId, position}];
            }
        });
    };

    const updateArmyPosition = (armyId, newX, newY) => {
        setArmyImages(currentArmyImages => currentArmyImages.map(army => {
            if (army.id === armyId) {
                return {...army, x: newX, y: newY};
            }
            return army;
        }));
        setUpdateTrigger(prev => !prev)
    };

    useEffect(() => {
        loadImage(props.mapImage, setImage);
    }, [props.mapImage]);

    useEffect(() => {
        loadImage(props.mapImage, setImage)
    }, [props.mapImage])

    {/*Get images of cities on map cities on the map*/}
    const [selectedCityId, setSelectedCityId] = useState(null);
    const [showCities, setShowCities] = useState(true);
    const [citiesLoaded, setCitiesLoaded] = useState(false)

    const handleCityClick = (cityId) => {
        setSelectedCityId(cityId);
        setShowCityManager(true);
        setShowCities(false);
    };
    const [cityImages,setCityImages] = useState([]);
    {/*Load cities from databank, and get images*/}
    useEffect(() => {
        const fetchCities = async () => {
            const cities = await getCities(1); // replace with actual planetID
            const cityElements = cities.map(city => ({
                ...city,
                onClick: () => handleCityClick(city.id),
            }));
            setCityImages(cityElements);
            setCitiesLoaded(true);
        };
        if (!citiesLoaded) {
            fetchCities();
        }
    }, [props.planetId, handleCityClick, citiesLoaded]);

    {/*handle closing of cityManager window*/}
    const [showCityManager, setShowCityManager] = useState(true);
    const handleCloseCityManager = () => {
        setShowCityManager(false);
        setSelectedCityId(null);
        setShowCities(true);
    }

    const [planetList, setPlanetList] = useContext(PlanetListContext)
    const [planetListIndex, setPlanetListIndex] = props.planetListIndex;
    useEffect(() => {
        const fetchArmies = async () => {
            const armies = await getArmies(1);
            const armyElements = armies.map(army => ({
                ...army,
                onClick: (e) => toggleArmyViewer(e, army.id),
            }));
            setArmyImages(armyElements);
        };
        fetchArmies();

    }, [updateTrigger]); // get the armies again when an army has been moved


    return (
        <>
        <div className="bg-gray-800 mx-auto w-2/12 py-3 fixed inset-x-0 top-5 z-10 border-2 border-white md:text-3xl justify-between items-center flex z-30">
        <RiArrowLeftSLine className="transition ease-in-out hover:scale-150" onClick={() => {let new_id = planetListIndex-1; if (new_id < 0){new_id+= planetList.length;} setPlanetListIndex(new_id)}}/>
         <h1>{props.planetName}</h1>
         <RiArrowRightSLine className="transition ease-in-out hover:scale-150" onClick={() => {let new_id = planetListIndex+1; new_id = new_id % planetList.length; setPlanetListIndex(new_id)}}/>
         </div>
        {
        image &&
            <MapInteractionCSS
                    value={mapState}
                    onChange={(value) => setMapState(value)}
                    minScale={1}
                    maxScale={5}
                    translationBounds={{
                        xMin: image.width - mapState.scale * image.width,
                        xMax: 0,
                        yMin: image.height - mapState.scale * image.height,
                        yMax: 0,
                    }}
                >
                    <img src={image.src} alt="map"
                         style={{imageRendering: "pixelated", width: "100%", height: "auto"}}/>
                    {armyImages.map((army, index) => (
                        <img key={index} src={army.src} alt="army" style={army.style}
                             onClick={(e) => toggleArmyViewer(e, army.id)}/>
                    ))}

                </MapInteractionCSS>

        }

        </>
    );
}

export default PlanetViewer;
