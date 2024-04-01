import { MapInteractionCSS } from 'react-map-interaction';
import {useState, useEffect, useContext, useRef} from 'react';
import { RiArrowLeftSLine, RiArrowRightSLine } from "react-icons/ri";

import getCities from './CityViewer/getCities';
import CityManager from "./CityViewer/CityManager";

import {PlanetListContext} from "./../Context/PlanetListContext"
import ArmyViewer from '../UI/ArmyViewer/ArmyViewer'
import getArmies from "./getArmies";
import {UserInfoContext} from "../Context/UserInfoContext";
import PlanetSVG from './PlanetSVG';

import { Popper, Box, List, ListItemButton} from '@mui/material';

const loadImage = async (imgPath, stateSetter) => {
    let img = new Image()
    img.src = imgPath
    img.onload = () => {
        stateSetter(img)
    }
}



function generateData(width, height) {
    const data = [];
    const cellWidth = 1 / width;
    const cellHeight = 1 / height;

    for (let i = 0; i < height; i++) {
        for (let j = 0; j < width; j++) {
            const x = Math.random() * cellWidth + j * cellWidth;
            const y = Math.random() * cellHeight + i * cellHeight;
            const types = ['type1', 'type2', 'type3']
            const regionType = types[Math.floor(Math.random()*types.length)];
            data.push({ x, y, regionType });
        }
    }

    return data;
}

const data = generateData(10,10);


function PlanetViewer(props) {

    const [mapState, setMapState] = useState({
        scale: 1,
        translation: {x: 0, y: 0},
    });
    const [armyImages, setArmyImages] = useState([]);
    const [activeArmyViewers, setActiveArmyViewers] = useState([]);  // array of army ids
    const [updateTrigger, setUpdateTrigger] = useState(false);

    const toggleArmyDetails = (armyId) => {
        setActiveArmyViewers(activeArmyViewers.map((elem, i) => {
            if (elem.id == armyId) {
                elem.detailsOpen = !elem.detailsOpen
            }
            return elem
        }))
    }

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
                return [...prev, {id: armyId, position, anchorEl: e.target, detailsOpen: false}];
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


    {/*Get images of cities on map cities on the map*/}
    const [selectedCityId, setSelectedCityId] = useState(null);
    const [showCities, setShowCities] = useState(true);
    const [citiesLoaded, setCitiesLoaded] = useState(false)

    const [userInfo, setUserInfo] = useContext(UserInfoContext)

    const handleCityClick = (cityId, controlledBy) => {
        if (controlledBy === userInfo.id){
            setSelectedCityId(cityId);
            setShowCityManager(true);
            setShowCities(false);
        }
    };

    const [cityImages,setCityImages] = useState([]);
    {/*Load cities from databank, and get images*/}
    useEffect(() => {
        const fetchCities = async () => {
            const cities = await getCities(props.planetId);

            // replace with actual planetID
            const cityElements = cities.map(city => ({
                ...city,
                onClick: () => handleCityClick(city.id, city.controlled_by),
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
            const armies = await getArmies(props.planetId);
            const armyElements = armies.map(army => ({
                ...army,
                onClick: (e) => toggleArmyViewer(e, army.id),
            }));
            setArmyImages(armyElements);
        };
        fetchArmies();

    }, [updateTrigger, props.planetId]); // get the armies again when an army has been moved

    return (
        <>
        <div className="bg-gray-800 mx-auto w-2/12 py-3 fixed inset-x-0 top-5 z-10 border-2 border-white md:text-3xl justify-between items-center flex z-30">
        <RiArrowLeftSLine className="transition ease-in-out hover:scale-150" onClick={() => {let new_id = planetListIndex-1; if (new_id < 0){new_id+= planetList.length;} setPlanetListIndex(new_id)}}/>
         <h1>{props.planetName}</h1>
         <RiArrowRightSLine className="transition ease-in-out hover:scale-150" onClick={() => {let new_id = planetListIndex+1; new_id = new_id % planetList.length; setPlanetListIndex(new_id)}}/>
         </div>

            {
                activeArmyViewers.map(({id, position, anchorEl, detailsOpen}) => (
                    <>
                        <Popper open={true} anchorEl={anchorEl} placement='left-start'>
                        <Box className="bg-black rounded-3xl" >
                        <List>
                        <ListItemButton>Move</ListItemButton>
                        <ListItemButton onClick={() => toggleArmyDetails(id)}>Details</ListItemButton>
                        </List>
                        </Box>
                        </Popper>
                        <Popper open={detailsOpen} anchorEl={anchorEl} placement='right-start'>
                            <ArmyViewer armyId={id} onUpdatePosition={updateArmyPosition}/>
                        </Popper>
                        </>
                ))
            }


                {/*Display cityManager over the map*/}
                {selectedCityId && showCityManager && (
                        <div style={{ position: 'absolute', top: 0, left: 0, width: '100%', height: '100%', zIndex: 20 }}>
                            <CityManager cityId={selectedCityId} primaryColor="black" secondaryColor="black" onClose={handleCloseCityManager} />
                        </div>
                )}

        <MapInteractionCSS
                value={mapState}
                onChange={(value) => setMapState(value)}
                minScale={1}
                maxScale={5}
                translationBounds={{

                    xMin: 1920 - mapState.scale * 1920,
                    xMax: 0,
                    yMin: 1080 - mapState.scale * 1080,
                    yMax: 0,
                }}
            >

                {/*Display planet on the map*/}
                 <PlanetSVG planetId={props.planetId} />

                {armyImages.map((army, index) => (
                    <img key={index} src={army.src} alt="army" style={army.style}
                         onClick={(e) => toggleArmyViewer(e, army.id)}/>
                ))}

                {/*Display cities on the map*/}
                    {showCities && cityImages.map((city, index) => (
                      <img key={index} src={city.src} alt="city" style={city.style} onClick={city.onClick} />
                    ))}

            </MapInteractionCSS>



        </>
    );
}

export default PlanetViewer;
