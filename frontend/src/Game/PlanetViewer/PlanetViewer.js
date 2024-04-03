import { MapInteractionCSS } from 'react-map-interaction';
import {useState, useEffect, useContext, useRef} from 'react';
import { RiArrowLeftSLine, RiArrowRightSLine } from "react-icons/ri";

import getCities from './CityViewer/getCities';
import CityManager from "./CityViewer/CityManager";

import {PlanetListContext} from "./../Context/PlanetListContext"
import ArmyViewer from '../UI/ArmyViewer/ArmyViewer'
import {UserInfoContext} from "../Context/UserInfoContext";
import PlanetSVG from './PlanetSVG';
import { Popper, Box, List, ListItemButton} from '@mui/material';
import WindowUI from '../UI/WindowUI/WindowUI';

import { fetchArmies, toggleArmyDetails, toggleArmyViewer, updateArmyPosition } from './Helper/ArmyHelper';
import { fetchCities } from './Helper/CityHelper';

import { IoMdClose } from "react-icons/io";

import army_example from "../Images/troop_images/Soldier.png"

import {ArcherContainer, ArcherElement} from 'react-archer'


function PlanetViewer(props) {
    const [hidePlanetSwitcherWindow, setHidePlanetSwitcherWindow] = useState(false)

    const [mapState, setMapState] = useState({
        scale: 1,
        translation: {x: 0, y: 0},
    });
    const [armyImages, setArmyImages] = useState([]);
    const [activeArmyViewers, setActiveArmyViewers] = useState([]);  // array of army ids
    const [updateTrigger, setUpdateTrigger] = useState(false);

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
        if (!citiesLoaded) {
            fetchCities({getCities:getCities, handleCityClick:handleCityClick, setCityImages:setCityImages, setCitiesLoaded:setCitiesLoaded});
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

    /*useEffect(() => {
        //fetchArmies(props.planetId, setArmyImages);
    }, [socket])*/
    
    const is_connected = useRef(false);
    const [socket, setSocket] = useState(null)

    useEffect(() => {
        if (is_connected.current) return
 
        is_connected.current = true;
 
        const web_socket = new WebSocket(`${process.env.REACT_APP_BACKEND_PATH_WEBSOCKET}/planet/ws/${props.planetId}`, `${localStorage.getItem('access-token')}`);
        setSocket(web_socket);
        web_socket.onopen = () => {
            web_socket.send(
            JSON.stringify(
                {
                        type: "get_armies",
                }))
            }
     }, []);

     const handleGetArmies = (data) => {
        return data.map(army => ({
            id: army.id,
            x: army.x,
            y: army.y,
            to_x: army.to_x,
            to_y: army.to_y,
            owner: army.owner,
            src: army_example,
            style: {
              position: 'absolute',
              left: `${army.x * 100}%`,
              top: `${army.y * 100}%`,
              transform: 'translate(-50%, -50%)',
              maxWidth: '10%',
              maxHeight: '10%',
              zIndex: 15,
              cursor: 'pointer'
            },
          }));
     }

     useEffect(() => {
        if (!socket) return;
        socket.onmessage = async(event) => {
            let response = JSON.parse(event.data)
            switch(response.request_type) {
                case "get_armies":
                    const armies = await handleGetArmies(response.data)
                    setArmyImages(armies);
                    break
                case "change_direction":
                    break
            }
        }
        return () => {
            socket.close()
        }
    }, [socket])

    const [unitsMoveMode, setUnitsMoveMode] = useState([])
    const isMoveMode = (armyId) => {
        return unitsMoveMode.indexOf(armyId) !== -1
    }
    const toggleMoveMode = (armyId) => {
        if (!isMoveMode(armyId)) setUnitsMoveMode([...unitsMoveMode, armyId])
        else setUnitsMoveMode(unitsMoveMode.filter((id) => armyId !== id))
    }
    const mapOnClick = (e) => {
        console.log(e.pageX/1920, e.pageY/1080)
        unitsMoveMode.forEach((armyId) => {
            socket.send(JSON.stringify(
                {
                        type: "change_direction",
                        to_x: e.pageX/1920,
                        to_y: e.pageY/1080,
                        army_id: armyId
                }))
        })
        setUnitsMoveMode([])
    }
     
    return (
        <>
        <WindowUI hideState={hidePlanetSwitcherWindow} windowName="Planet Switcher">
            <div className='bg-gray-800 mx-auto w-2/12 py-3 fixed inset-x-0 top-5 z-10 border-2 border-white md:text-3xl'>
            <IoMdClose className="top-0 text-sm ml-1 absolute mt-1 left-0" onClick={() => setHidePlanetSwitcherWindow(!hidePlanetSwitcherWindow)}/>
            <div className="justify-between items-center flex z-30">
            <RiArrowLeftSLine className="transition ease-in-out hover:scale-150" onClick={() => {let new_id = planetListIndex-1; if (new_id < 0){new_id+= planetList.length;} setPlanetListIndex(new_id)}}/>
            <h1>{props.planetName}</h1>
            <RiArrowRightSLine className="transition ease-in-out hover:scale-150" onClick={() => {let new_id = planetListIndex+1; new_id = new_id % planetList.length; setPlanetListIndex(new_id)}}/>
            </div>
            </div>
         </WindowUI>

            {
                activeArmyViewers.map(({id, owner, position, to_position, anchorEl, detailsOpen}) => (
                    <>
                        <Popper open={true} anchorEl={anchorEl} placement='left-start'>
                        <Box className="bg-black rounded-3xl" >
                        <List>
                        {owner === userInfo.id && <ListItemButton onClick={() => toggleMoveMode(id)}>{isMoveMode(id) ? 'Cancel Move To' : 'Move To'}</ListItemButton>}
                        <ListItemButton onClick={() => toggleArmyDetails(id, setActiveArmyViewers, activeArmyViewers)}>Details</ListItemButton>
                        </List>
                        </Box>
                        </Popper>
                        <Popper open={detailsOpen} anchorEl={anchorEl} placement='right-start'>
                            <ArmyViewer armyId={id} onUpdatePosition={() => {updateArmyPosition(id, position.x, position.y, setArmyImages, setUpdateTrigger)}}/>
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
                 <PlanetSVG planetId={props.planetId} onClick={mapOnClick}/>

                {armyImages.map((army, index) => (
                    <img key={index} src={army.src} alt="army" style={army.style}
                         onClick={(e) => toggleArmyViewer(e, army, setActiveArmyViewers)}/>
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