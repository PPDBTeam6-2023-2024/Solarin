import { Canvas, useLoader} from '@react-three/fiber'
import { TextureLoader } from 'three/src/loaders/TextureLoader'
import { OrbitControls, Bounds, useBounds, Stars, Html, useContextBridge, Line} from '@react-three/drei'
import React, {useState, useRef, useEffect, Fragment, useContext} from 'react'
import {animated} from '@react-spring/three'
import axios from 'axios'
import Tooltip from '@mui/material/Tooltip';

import {View} from "../Context/ViewModeContext"
import {UserInfoContext} from "../Context/UserInfoContext";
import {SocketContext} from "../Context/SocketContext";
import {PlanetIdContext} from "../Context/PlanetIdContext";
import {ReactReduxContext} from "react-redux";

import {IoMdClose} from 'react-icons/io';
import Fleet from './Fleet'

// inspiration: https://codesandbox.io/p/sandbox/bounds-and-makedefault-rz2g0?file=%2Fsrc%2FApp.js%3A38%2C1-45%2C2

const SelectToZoom = ({ children, planetId, setPlanetSelected}) => {
  const api = useBounds()
  return (
    <group onClick={(e) => (setPlanetSelected(planetId), e.stopPropagation(), e.delta <= 2 && api.refresh(e.object).fit())}>
      {children}
    </group>
  )
}

function Scene(props) {
    const [userInfo, setUserInfo] = useContext(UserInfoContext);
    const [socket, setSocket] = useContext(SocketContext)

    const [planetSelected, setPlanetSelected] = useState(null)

    const [showListedFleets, setshowListedFleets] = useState(false)
    const [listedFleets, setListedFleets] = useState([])

    const [fleetsInSpace, setFleetsInSpace] = useState([])



    const planetImages = {
        "terrestrial": useLoader(TextureLoader, "/images/Planets/terrestrial.png"),
        "tropical": useLoader(TextureLoader, "/images/Planets/tropical.png"),
        "desert": useLoader(TextureLoader, "/images/Planets/desert.png"),
        "arctic": useLoader(TextureLoader, "/images/Planets/arctic.png")
    }

    const [publicPlanets, setPublicPlanets] = useState([])
    const [privatePlanets, setPrivatePlanets] = useState([])


    const handleGetFleets = (data) => {
        return data.map(fleet => {
            const arrivalTime = new Date(fleet.arrival_time).getTime()
            const departureTime = new Date(fleet.departure_time).getTime()
            return {
                id: fleet.id,
                x: fleet.x,
                y: fleet.y,
                to_x: fleet.to_x,
                to_y: fleet.to_y,
                owner: fleet.owner,
                arrivalTime: arrivalTime,
                departureTime: departureTime,
            }
        });
    }
    /*
* Handle when an army changes direction
* */
    const handleChangeDirection = (data) => {
        return fleetsInSpace.map((fleet) => {
            if (fleet.id === data.id) {
                return {...fleet, ...handleGetFleets([data])[0]}
            }
            return fleet
        })
    }


    useEffect(() => {
        if (!socket) return
        socket.onmessage = async (event) => {
            let response = JSON.parse(event.data)
            /*Websocket cases depending on the type of request we receive from the abckend websockets*/
            switch (response.request_type) {
                case "get_armies":
                    const fleets = await handleGetFleets(response.data)
                    setFleetsInSpace(fleets)
                    break
                case "change_direction":
                    const newFleets = handleChangeDirection(response.data)
                    setFleetsInSpace(newFleets)
                    break
                case "reload":
                    /*
                    This event just indicates that frontend needs to reload both armies and cities,
                    to be consistent with the backend
                    * */
                    //await reloadCities()
                    /*socket.send(
                        JSON.stringify(
                            {
                                type: "get_armies",
                            })
                    )*/

                    break
                default:
                    break
            }
        }
    }, [socket, fleetsInSpace])

    const fetchFleetsOnPlanet = async(planetId) => {
        const response = await axios.get(`${process.env.REACT_APP_BACKEND_PATH}/army/fleets?user_id=${userInfo.id}&planet_id=${planetId}`)
        setListedFleets(response.data)
    }
    const leavePlanet = async(fleetId) => {
        const data_json  = {
            type: "leave_planet",
            army_id: fleetId
        };
        await socket.send(JSON.stringify(data_json));
        await socket.send(
            JSON.stringify(
                {
                    type: "get_armies",
                }))
        setListedFleets(listedFleets.filter(fleet => fleet.id !== fleetId))
    }
    useEffect(() => {
        const fetchPublicPlanets = async() => {
            const response = await axios.get(`${process.env.REACT_APP_BACKEND_PATH}/planet/planets/public`)
            setPublicPlanets(response.data)
        }
        const fetchPrivatePlanets = async() => {
            const response = await axios.get(`${process.env.REACT_APP_BACKEND_PATH}/planet/planets/private`)
            setPrivatePlanets(response.data)
        }
        fetchPublicPlanets()
        fetchPrivatePlanets()
        socket.send(
            JSON.stringify(
                {
                    type: "get_armies",
                }))
    }, [])

    const [fleetsMoveMode, setFleetsMoveMode] = useState([])
    const [hoverPos, setHoverPos] = useState([0,0,0])
    const isMoveMode = (fleetId) => {
        return fleetsMoveMode.find((fleet) => fleet.id === fleetId) !== undefined
    }
    const toggleMoveMode = (fleetId, fleetPos) => {
        const obj = {"id": fleetId, "pos": fleetPos}
        if (!isMoveMode(fleetId)) setFleetsMoveMode(prev => [...prev, obj])
        else setFleetsMoveMode(fleetsMoveMode.filter((fleet) => fleet.id !== fleetId))
    }
    const mapOnClick = (e) => {
        let action_json = {}

        //const clickedArmy = imageType === "army";
        //const clickedPlanet = imageType === "city";

        //const index = parseInt(e.target.getAttribute("index"));
        //const isOwner = Boolean(parseInt(e.target.getAttribute("is_owner")));

        /*Decide which target action to do*/
        let target = ""

        console.log(e)

        /*if (clickedPlanet) {
            target = "enter_planet"
        }
        } else if (clickedArmy) {
            if (!isOwner) {
                target = "attack_army"
            } else {
                target = "merge"
            }
        }

        action_json = {
            on_arrive: true,
            target_type: target,
            target_id: index

        }*/

        fleetsMoveMode.forEach(async fleet => {
            const data_json = {
                type: "change_direction",
                to_x: e.point.x,
                to_y: e.point.z,
                army_id: fleet.id,
            };

            const merged_data = Object.assign({}, data_json, action_json);

            /*Send websocket message about movement change*/
            await socket.send(JSON.stringify(data_json));
        })
        setFleetsMoveMode([])
    }
    return (
        <>
            <Stars/>
            <ambientLight intensity={0.9}/>
            <mesh onClick={(e) => {
                if (fleetsMoveMode !== []) mapOnClick(e)
            }} visible={false} onPointerMove={(e) => setHoverPos(e.point)} position={[0, 0, 0]}
                  scale={[1000, 0.1, 1000]}>
                <boxGeometry args={[1, 1, 1]}/>
            </mesh>
            {
                fleetsMoveMode.map((obj) => {
                    return (
                        <Line color={"red"} points={[obj.pos, hoverPos]} lineWidth={2}/>
                    )
                })
            }
            <Bounds fit clip observe margin={1.2}>
                {/*Display a sun in the center*/}
                <mesh position={[0, 0, 0]} scale={5}>
                    <sphereGeometry args={[2]}/>
                    <meshStandardMaterial emissive="white" emissiveIntensity={1} toneMapped={false}/>
                </mesh>
                {/*Display the fleets in the galaxy view */}
                {
                    fleetsInSpace.map((fleet) => {
                        return (
                            <Fleet fleet={fleet} isMoveMode={() => isMoveMode(fleet.id)}
                                   toggleMoveMode={toggleMoveMode} mapOnClick={mapOnClick}/>
                        )
                    })
                }
                {/*Display the planets in the galaxy view*/}
                {publicPlanets.map((planet) => {
                    return (
                        <Fragment key={planet.id}>
                            <SelectToZoom setPlanetSelected={setPlanetSelected} planetId={planet.id}>
                                <animated.mesh onClick={mapOnClick} position={[50 * planet.x, 0, 50 * planet.y]} onDoubleClick={() => {
                                    if (privatePlanets.find((privatePlanet) => privatePlanet.id === planet.id)) {
                                        props.changePlanetId(planet.id);
                                        props.setViewMode(View.PlanetView)
                                    }
                                }}>
                                    <sphereGeometry args={[2]}/>
                                    <meshStandardMaterial map={planetImages[planet.planet_type]}/>
                                    {planetSelected === planet.id &&
                                        <Html>
                                            <div className='grid grid-flow-col auto-cols-max'>
                                                <div className="bg-black whitespace-nowrap p-2 border border-white">
                                                    <IoMdClose onClick={() => setPlanetSelected(null)}/>
                                                    Planet Name: {planet.name} <br></br>
                                                    Planet Type: {planet.planet_type}
                                                    <div>
                                                        {
                                                            !privatePlanets.find((privatePlanet) => privatePlanet.id === planet.id) ?
                                                                <span className="text-red-500">You have no armies or cities here</span>
                                                                : <>
                                                                    <Tooltip
                                                                        title={"Armies with a Mothership are considered fleets."}>
                                                                        <button
                                                                            className="bg-red-800 hover:bg-red-900 p-1 my-2"
                                                                            onClick={() => {
                                                                                setshowListedFleets(!showListedFleets);
                                                                                fetchFleetsOnPlanet(planet.id)
                                                                            }}>Your Fleets
                                                                        </button>
                                                                    </Tooltip>
                                                                    <p className="text-green-500">Double-click on planet to
                                                                        enter planet view</p></>

                                                        }
                                                    </div>
                                                </div>
                                                {
                                                    showListedFleets &&
                                                    <div className="bg-black mx-2 p-2 border border-white">
                                                        <h1>Fleets</h1>
                                                        {listedFleets.map((fleet) => {
                                                            return <h1 key={fleet.id}>
                                                                <span>Fleet {fleet.id}</span>
                                                                <button onClick={() => leavePlanet(fleet.id)}
                                                                        className="bg-red-800 hover:bg-red-900 p-1">Leave
                                                                    Planet
                                                                </button>
                                                            </h1>
                                                        })}
                                                    </div>
                                                }
                                            </div>
                                        </Html>
                                    }
                                </animated.mesh>
                            </SelectToZoom>
                        </Fragment>
                    )
                })
                }
            </Bounds>
            <OrbitControls enablePan={false} makeDefault minPolarAngle={0} maxPolarAngle={Math.PI / 1.75}/>
        </>)
}

function ForwardCanvas(props) {
    const ContextBridge = useContextBridge(SocketContext, UserInfoContext, PlanetIdContext, ReactReduxContext);
    return (
        <Canvas
        flat shadows style={{position: "fixed", backgroundColor: "#0a0a0a"}} scene={{background: "black"}}>
            <ContextBridge>
                <Scene setViewMode={props.setViewMode} changePlanetId={props.changePlanetId}/>
            </ContextBridge>
      </Canvas>
    )

}
function GalaxyViewer(props) {
    /*This state and ref keep information about the websocket*/
    const isWebSocketConnected = useRef(false);
    const [socket, setSocket] = useState(null)
    useEffect(() => {
        if (isWebSocketConnected.current) return
        isWebSocketConnected.current = true;
        const webSocket = new WebSocket(`${process.env.REACT_APP_BACKEND_PATH_WEBSOCKET}/planet/ws/0`, `${localStorage.getItem('access-token')}`);
        setSocket(webSocket)
    },[])

    useEffect(() => {
        if (!socket) return
        return () => {
            socket.close()
        }
    }, [socket])

    return (
        <PlanetIdContext.Provider value={0}>
        <SocketContext.Provider value={[socket, setSocket]}>
            <ForwardCanvas setViewMode={props.setViewMode} changePlanetId={props.changePlanetId}/>
        </SocketContext.Provider>
        </PlanetIdContext.Provider>
    )
}

export default GalaxyViewer