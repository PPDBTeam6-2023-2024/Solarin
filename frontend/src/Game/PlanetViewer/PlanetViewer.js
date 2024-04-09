import { MapInteractionCSS } from 'react-map-interaction';
import {useState, useEffect, useContext, useRef, Fragment} from 'react';
import { RiArrowLeftSLine, RiArrowRightSLine } from "react-icons/ri";

import getCities from './CityViewer/getCities';
import CityManager from "./CityViewer/CityManager";

import {PlanetListContext} from "../Context/PlanetListContext"
import ArmyViewer from '../UI/ArmyViewer/ArmyViewer'
import {UserInfoContext} from "../Context/UserInfoContext";
import PlanetSVG from './PlanetSVG';
import { Popper, Box, List, ListItemButton} from '@mui/material';
import WindowUI from '../UI/WindowUI/WindowUI';

import {toggleArmyViewer, closeArmyViewer } from './Helper/ArmyViewerHelper';
import { fetchCities } from './Helper/CityHelper';

import { IoMdClose } from "react-icons/io";

import army_example from "../Images/troop_images/Soldier.png"
import ArmyMapEntry from "./ArmyMapEntry";
import CityMapEntry from "./CityMapEntry";
import {string} from "three/examples/jsm/nodes/shadernode/ShaderNode";
import ArmyManageView from "../UI/ArmyViewer/ArmyManageView";

function PlanetViewer(props) {
    const [hidePlanetSwitcherWindow, setHidePlanetSwitcherWindow] = useState(false)

    const [mapState, setMapState] = useState({
        scale: 1,
        translation: {x: 0, y: 0},
    });
    const [armyImages, setArmyImages] = useState([]);
    const [activeArmyViewers, setActiveArmyViewers] = useState([]);  // array of army ids

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

    useEffect(() => {
        setCitiesLoaded(false)
    }, [props.planetId])

    const [cityImages,setCityImages] = useState([]);

    const reloadCities = () => {
        setCitiesLoaded(false)
    }

    {/*Load cities from databank, and get images*/}
    useEffect(() => {
        if (!citiesLoaded) {
            fetchCities({getCities:getCities, handleCityClick:handleCityClick, setCityImages:setCityImages, setCitiesLoaded:setCitiesLoaded});
        }
    }, [handleCityClick, citiesLoaded]);

    {/*handle closing of cityManager window*/}
    const [showCityManager, setShowCityManager] = useState(true);
    const handleCloseCityManager = () => {
        setShowCityManager(false);
        setSelectedCityId(null);
        setShowCities(true);
    }

    const [planetList, setPlanetList] = useContext(PlanetListContext)
    const [planetListIndex, setPlanetListIndex] = props.planetListIndex;
    
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
     const lerp = ({source_position, target_position, arrival_time, departure_time}) => {
        var d  = new Date()
        d.setHours(d.getHours()-2)
        const elapsedTime = d - departure_time
        const totalTime = arrival_time - departure_time
        const percentComplete = (elapsedTime < totalTime) ? elapsedTime / totalTime : 1;
        const currentX = source_position.x + (target_position.x - source_position.x) * percentComplete
        const currentY = source_position.y + (target_position.y - source_position.y) * percentComplete
        return {x: currentX, y: currentY}
     }
     const handleGetArmies = (data) => {
        return data.map(army => {
            const arrival_time = new Date(army.arrival_time).getTime()
            const departure_time = new Date(army.departure_time).getTime()
            const current_pos = lerp({source_position: {x: army.x, y: army.y}, target_position: {x: army.to_x, y: army.to_y}, 
                arrival_time: arrival_time, departure_time: departure_time})
            return {
            id: army.id,
            x: army.x,
            y: army.y,
            to_x: army.to_x,
            to_y: army.to_y,
            owner: army.owner,
            arrival_time: arrival_time,
            departure_time: departure_time,
            src: army_example,
            style: {
              position: 'absolute',
              left: `${current_pos.x * 100}%`,
              top: `${current_pos.y * 100}%`,
              transform: 'translate(-50%, -50%)',
              maxWidth: '10%',
              maxHeight: '10%',
              zIndex: 15,
              transition: "all ease-linear",
            },
            }
            });
     }
     useEffect(() => {
        const interval = setInterval(async() => {
            setArmyImages(armyImages.map((elem) => {
            const current_position = lerp({source_position: {x: elem.x, y: elem.y}, 
                target_position: {x: elem.to_x, y: elem.to_y}, arrival_time: elem.arrival_time, departure_time: elem.departure_time})
            return {...elem, curr_x: current_position.x, curr_y: current_position.y}
            }))
          }, 100);
          return () => {
            clearInterval(interval)
          }
     })
     const handleChangeDirection = (data) => {
        return armyImages.map((army) => {
            if(army.id === data.id) {
                return {...army, ...handleGetArmies([data])[0]}
            }
            return army
        })
     }
     useEffect(() => {
        if (!socket) return
        return () => {
            socket.close()
        }
    }, [socket])


    /*
    Close the ArmyViewers for armies that are not visible anymore
    When armies are not visualized anymore (When entering a city, being killed, ...)
    We want to make sure the Army viewer will be closed.
    */
    useEffect(() => {
        let removed = activeArmyViewers.filter(army => !armyImages.some(new_army => new_army.id === army.id))
        removed.forEach((r, index) => {closeArmyViewer(r, setActiveArmyViewers)});

    }, [armyImages.map(army => army.id).join(";").toString()]);


    useEffect(() => {
        if(!socket) return
        socket.onmessage = async(event) => {
            let response = JSON.parse(event.data)
            switch(response.request_type) {
                case "get_armies":
                    const armies = await handleGetArmies(response.data)
                    setArmyImages(armies);

                    break
                case "change_direction":
                    const newArmies = handleChangeDirection(response.data)
                    setArmyImages(newArmies)
                    break
                case "reload":
                    /*
                    This event just indicates that frontend needs to reload both armies and cities,
                    to be consistent with the backend
                    * */
                    fetchCities({getCities:getCities, handleCityClick:handleCityClick, setCityImages:setCityImages, setCitiesLoaded:setCitiesLoaded});
                    socket.send(
                        JSON.stringify(
                            {
                                    type: "get_armies",
                            })
                    )

                    break
            }
        }
    }, [socket, armyImages])

    const [armiesMoveMode, setArmiesMoveMode] = useState([])
    const isMoveMode = (armyId) => {
        return armiesMoveMode.indexOf(armyId) !== -1
    }
    const toggleMoveMode = (armyId) => {
        if (!isMoveMode(armyId)) setArmiesMoveMode(prev => [...prev, armyId])
        else setArmiesMoveMode(armiesMoveMode.filter((id) => armyId !== id))
    }

    {/*For calculating the position we need to know the size of the map on the client, to calculate the position in range[0, 1]*/}
    const screenSize = useRef();

    const mapOnClick = (e) => {

        let action_json = {}

        const image_type = e.target.getAttribute("image_type")
        if (image_type !== null){
            const clickedArmy = image_type === "army";
            const clickedCity = image_type === "city";

            const index = parseInt(e.target.getAttribute("index"));
            const is_owner = Boolean(parseInt(e.target.getAttribute("is_owner")));

            /*Decide which target action to do*/
            let target = ""

            if (clickedCity){
                if (!is_owner){
                    target = "attack_city"
                }else{
                    target = "enter"
                }

            }else if (clickedArmy){
                if (!is_owner){
                    target = "attack_army"
                }else{
                    target = "merge"
                }
            }

            action_json = {
                on_arrive: true,
                target_type: target,
                target_id: index

            }
        }

        
        armiesMoveMode.forEach(async(armyId) => {
            const data_json  = {
                        type: "change_direction",
                        to_x: e.pageX/screenSize.current?.clientWidth,
                        to_y: e.pageY/screenSize.current?.clientHeight,
                        army_id: armyId
                };

            const merged_data = Object.assign({}, data_json, action_json);

            await socket.send(JSON.stringify(merged_data));
            toggleMoveMode(armyId)
        })
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
                /*
                This ArmyManageView is not a child component of the Army entry, because this is a rela UI component
                That should be a part of the map itself
                * */
                activeArmyViewers.map(({id, owner, position, anchorEl}) => (
                    <ArmyManageView key={id} id={id} owner={owner} anchorEl={anchorEl} toggleMoveMode={toggleMoveMode} isMoveMode={isMoveMode} onCityCreated={reloadCities}/>
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
                <div ref={screenSize} style={{"width": "100%", "height": "100%"}} onClick={mapOnClick}>
                    {/*Display planet on the map*/}
                     <PlanetSVG planetId={props.planetId}/>

                    {/*
                    decide_moving, just passed whether a moving is selected, to change the cursor icon accordingly
                    moving selected, just states whether the army is planning to move
                    */}
                    {armyImages.map((army, index) => (
                        <ArmyMapEntry key={index} army={army} onClick={(e) => {if (armiesMoveMode.length === 0){toggleArmyViewer(e, army, setActiveArmyViewers);}}}
                         decide_moving={armiesMoveMode.length > 0} moving_Selected={isMoveMode(army.id)}/>
                    ))}


                    {/*Display cities on the map*/}
                    {/*decide_moving, just passed whether a moving is selected, to change the cursor icon accordingly*/}
                    {showCities && cityImages.map((city, index) => (
                        <CityMapEntry key={index} city={city} onClick={()=>{if (armiesMoveMode.length === 0){city.onClick();}}}
                        decide_moving={armiesMoveMode.length > 0}/>
                    ))}
                </div>


            </MapInteractionCSS>



        </>
    );
}

export default PlanetViewer;