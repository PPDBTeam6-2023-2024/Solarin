import {MapInteractionCSS} from 'react-map-interaction';
import {useState, useEffect, useContext, useRef} from 'react';

import CityManager from "./CityViewer/CityManager";


import {UserInfoContext} from "../Context/UserInfoContext";
import PlanetSVG from './PlanetSVG';

import {toggleArmyViewer, closeArmyViewer} from './Helper/ArmyViewerHelper';
import {fetchCities} from './Helper/CityHelper';

import ArmyMapEntry from "./ArmyMapEntry";
import CityMapEntry from "./CityMapEntry";
import ArmyManageView from "../UI/ArmyViewer/ArmyManageView";
import {SocketContext} from "../Context/SocketContext";
import {PlanetIdContext} from "../Context/PlanetIdContext";
import PlanetSwitcher from "../UI/PlanetSwitcher/PlanetSwitcher";
import zIndex from "@mui/material/styles/zIndex";

function PlanetViewer(props) {
    /*
    *This component represents the view of a planet, when we visit another planet,
    * this component will be replaced by another planetViewer Component. This means that
    * this component manages a planet view of 1 specific planet
    * */

    /*Map information to support scrolling and moving on the MapInteractionCSS component*/
    const [mapState, setMapState] = useState({
        scale: 1,
        translation: {x: 0, y: 0},
    });

    /*State that keeps a list of all the armies that need to be displayed*/
    const [armyImages, setArmyImages] = useState([]);

    /*Keep track of all the army viewers (army menu) that are currently open*/
    const [activeArmyViewers, setActiveArmyViewers] = useState([]);  // array of army ids

    /*
    * SelectCityId stores an Id of the currently selected city, this makes it possible
    * To have the UI component, outside the MapInteractionCSS component
    * ShowCities decides, whether or not cities will be visualized on the map
    * */
    const [selectedCityId, setSelectedCityId] = useState(null);
    const [showCities, setShowCities] = useState(true);

    /*User account information*/
    const [userInfo, setUserInfo] = useContext(UserInfoContext)

    /*
    * When we click on a city, we want to open the city menu, but only when our user is the owner of this city
    * */
    const handleCityClick = (cityId, controlledBy) => {
        if (controlledBy === userInfo.id) {
            setSelectedCityId(cityId);
            setShowCityManager(true);
            setShowCities(false);
        }
    };

    /*Get images of cities on map cities on the map*/
    const [cityImages, setCityImages] = useState([]);

    /*Reload all the city information from the backend*/
    const reloadCities = () => {
        fetchCities({
                handleCityClick: handleCityClick,
                setCityImages: setCityImages
        }, props.planetId);
    }

    /*
    * When we load the planet:
    * Load cities from database, and get images
    */
    useEffect(() => {
        /*Load Cities*/
        reloadCities()
    }, []);

    /*handle closing of cityManager window*/
    const [showCityManager, setShowCityManager] = useState(true);
    const handleCloseCityManager = () => {
        setShowCityManager(false);
        setSelectedCityId(null);
        setShowCities(true);
    }

    /*This state and ref keep information about the websocket*/
    const isWebSocketConnected = useRef(false);
    const [socket, setSocket] = useState(null)

    useEffect(() => {
        if (isWebSocketConnected.current) return

        isWebSocketConnected.current = true;

        const webSocket = new WebSocket(`${process.env.REACT_APP_BACKEND_PATH_WEBSOCKET}/planet/ws/${props.planetId}`, `${localStorage.getItem('access-token')}`);
        setSocket(webSocket);
        webSocket.onopen = () => {
            webSocket.send(
                JSON.stringify(
                    {
                        type: "get_armies",
                    }))
        }

    }, []);

    // calculate position based on source- and target position and how much time has elapsed
    const lerp = ({sourcePosition, targetPosition, arrivalTime, departureTime}) => {
        let date = new Date()
        date.setHours(date.getHours() - 2)

        const elapsedTime = date - departureTime
        const totalTime = arrivalTime - departureTime
        const percentComplete = (elapsedTime < totalTime) ? elapsedTime / totalTime : 1;
        const currentX = sourcePosition.x + (targetPosition.x - sourcePosition.x) * percentComplete
        const currentY = sourcePosition.y + (targetPosition.y - sourcePosition.y) * percentComplete
        return {x: currentX, y: currentY}
    }
    const handleGetArmies = (data) => {
        return data.map(army => {
            const arrivalTime = new Date(army.arrival_time).getTime()
            const departureTime = new Date(army.departure_time).getTime()
            const currentPos = lerp({
                sourcePosition: {x: army.x, y: army.y}, targetPosition: {x: army.to_x, y: army.to_y},
                arrivalTime: arrivalTime, departureTime: departureTime
            })
            return {
                id: army.id,
                x: army.x,
                y: army.y,
                to_x: army.to_x,
                to_y: army.to_y,
                owner: army.owner,
                alliance: army.alliance,
                username: army.username,
                arrivalTime: arrivalTime,
                departureTime: departureTime,
                style: {
                    position: 'absolute',
                    left: `${currentPos.x * 100}%`,
                    top: `${currentPos.y * 100}%`,
                    transform: "translate(-50%, -50%)",
                    maxWidth: '10%',
                    maxHeight: '10%',
                    zIndex: 15,
                    transition: "all ease-linear",
                },
            }
        });
    }

    /*
    * Update the army location of the armies on the map in real time
    * by updating the army position, visually based on linear interpolation
    */
    useEffect(() => {
        const interval = setInterval(async () => {
            setArmyImages(armyImages.map((elem) => {
                const currentPosition = lerp({
                    sourcePosition: {x: elem.x, y: elem.y},
                    targetPosition: {x: elem.to_x, y: elem.to_y},
                    arrivalTime: elem.arrivalTime,
                    departureTime: elem.departureTime
                })
                return {...elem, curr_x: currentPosition.x, curr_y: currentPosition.y}
            }))
        }, 100);
        return () => {
            clearInterval(interval)
        }
    })

    /*
    * Handle when an army changes direction
    * */
    const handleChangeDirection = (data) => {
        return armyImages.map((army) => {
            if (army.id === data.id) {
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
        removed.forEach((r, index) => {
            closeArmyViewer(r, setActiveArmyViewers)
        });

    }, [armyImages.map(army => army.id).join(";").toString()]);

    /*
    * Listen to incoming websocket messages
    * */
    useEffect(() => {
        if (!socket) return
        socket.onmessage = async (event) => {
            let response = JSON.parse(event.data)
            /*Websocket cases depending on the type of request we receive from the abckend websockets*/
            switch (response.request_type) {
                case "get_armies":
                    const armies = await handleGetArmies(response.data)
                    console.log(armies)
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
                    await reloadCities()
                    socket.send(
                        JSON.stringify(
                            {
                                type: "get_armies",
                            })
                    )

                    break
                default:
                    break
            }
        }
    }, [socket, armyImages])

    /*
    * Keeps into account which armies are in Move mode.
    * Move mode means that an army is selected as an army that will move.
    * When we click a place on the map, all selected armies will move to this position
    * */
    const [armiesMoveMode, setArmiesMoveMode] = useState([])
    const isMoveMode = (armyId) => {
        return armiesMoveMode.indexOf(armyId) !== -1
    }
    const toggleMoveMode = (armyId) => {
        if (!isMoveMode(armyId)) setArmiesMoveMode(prev => [...prev, armyId])
        else setArmiesMoveMode(armiesMoveMode.filter((id) => armyId !== id))
    }

    /*For calculating the position 'move to' we need to know the size of the map on
    *the client, to calculate the position in range[0, 1]
    * */

    const screenSize = useRef();

    const mapOnClick = (e, action_json={}) => {
        /*
        * When we click on a map, we will move all our armies that are in MoveMode to the provided position
        * */

        /*
        * Let the armies change direction (movement) to the provided position
        * */
        e.stopPropagation()
        armiesMoveMode.forEach(async (armyId) => {
            const data_json = {
                type: "change_direction",
                to_x: e.pageX / screenSize.current?.clientWidth,
                to_y: e.pageY / screenSize.current?.clientHeight,
                army_id: armyId
            };

            const merged_data = Object.assign({}, data_json, action_json);

            /*Send websocket message about movement change*/
            await socket.send(JSON.stringify(merged_data));
            toggleMoveMode(armyId)
        })
    }
    return (
        <>
            {/*Make it possible to access the socket in the children without using props (because cleaner)*/}
            <PlanetIdContext.Provider value={props.planetId}>
                <SocketContext.Provider value={[socket, setSocket]}>

                    {/*Display planet switch component*/}
                    <PlanetSwitcher planetIndex={props.planetListIndex}/>

                    {
                        /*
                        This ArmyManageView is not a child component of the Army entry, because this is a UI component
                        That should be a part of the map itself
                        */
                        activeArmyViewers.map(({id, owner, anchorEl}) => (
                            <ArmyManageView key={id} id={id} owner={owner} anchorEl={anchorEl}
                                            toggleMoveMode={toggleMoveMode} isMoveMode={isMoveMode}
                                            onCityCreated={reloadCities}/>
                        ))
                    }


                    {/*Display cityManager over the map*/}
                    {selectedCityId && showCityManager && (
                        <div style={{ position: 'absolute', top: 0, left: 0, width: '100%', height: '100%', zIndex: 20 }}>
                            <CityManager key={selectedCityId} cityId={selectedCityId} primaryColor="black" secondaryColor="black" onClose={handleCloseCityManager}/>
                        </div>
                    )}

                    {/*Display the zoom-able map*/}
                    <MapInteractionCSS
                        value={mapState}
                        onChange={(value) => setMapState(value)}
                        minScale={1}
                        maxScale={5}
                        translationBounds={{
                            xMin: 1920 - mapState.scale * 1920,
                            xMax: 0,
                            yMin: 1010 - mapState.scale * 1010,
                            yMax: 0,
                        }}
                    >
                        <div ref={screenSize} style={{"width": "100%", "height": "100%"}} onClick={(e) => {
                            if(armiesMoveMode.length > 0) mapOnClick(e)
                        }}>
                            {/*Display planet on the map*/}
                            <PlanetSVG armyImages={armyImages} armiesMoveMode={armiesMoveMode} planetId={props.planetId} screenSize={screenSize}/>

                            {/*Display cities on the map*/}
                            {/*decide_moving, just passed whether a moving is selected, to change the cursor icon accordingly*/}
                            {showCities && cityImages.map((city, index) => (
                                <CityMapEntry key={index} city={city} onClick={(e, action_json) => {
                                    if(armiesMoveMode.length > 0) mapOnClick(e, action_json)
                                    else handleCityClick(city.id, city.controlled_by)
                                }} decide_moving={armiesMoveMode.length > 0}/>
                            ))}


                            {/*
                            decide_moving, just passed whether a moving is selected, to change the cursor icon accordingly
                            moving selected, just states whether the army is planning to move
                            */}
                            {armyImages.map((army, index) => (
                                <ArmyMapEntry key={army.id} army={army} onClick={(e, action_json) => {
                                    if (armiesMoveMode.length === 0) {
                                        toggleArmyViewer(e, army, setActiveArmyViewers);
                                    }
                                    else mapOnClick(e, action_json)
                                }}
                                              toggleArmyViewer={toggleArmyViewer}
                                              decide_moving={armiesMoveMode.length > 0}
                                              moving_Selected={isMoveMode(army.id)}/>
                            ))}
                        </div>

                    </MapInteractionCSS>

                </SocketContext.Provider>
            </PlanetIdContext.Provider>
        </>
    );
}

export default PlanetViewer;