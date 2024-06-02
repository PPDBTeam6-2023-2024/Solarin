import { Canvas} from '@react-three/fiber'
import { OrbitControls, Bounds, Stars, useContextBridge, Line} from '@react-three/drei'
import React, {useState, useRef, useEffect, Fragment, useContext} from 'react'
import axios from 'axios'

import {UserInfoContext} from "../Context/UserInfoContext";
import {SocketContext} from "../Context/SocketContext";
import {PlanetIdContext} from "../Context/PlanetIdContext";
import {ReactReduxContext} from "react-redux";

import Fleet from './Fleet'
import Planet from './Planet'
import {PlanetListContext} from "../Context/PlanetListContext";
import ColorManager from "../ColorManager";

function Scene(props) {
    const [socket, setSocket] = useContext(SocketContext)

    const [fleetsInSpace, setFleetsInSpace] = useState([])

    const [publicPlanets, setPublicPlanets] = useState([])
    const [privatePlanets, setPrivatePlanets] = useState([])
/* Handle when getting fleets */
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
            /* Websocket cases depending on the type of request we receive from the backend websockets */
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
    }, [socket, fleetsInSpace])


    useEffect(() => {
        if (!socket) return

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
    }, [socket])

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
    const moveTo = (e, action_json = {}) => {
        e.stopPropagation()
        fleetsMoveMode.forEach(async (fleet, i) => {
            const data_json = {
                type: "change_direction",
                to_x: e.point.x/50,
                to_y: e.point.z/50,
                army_id: fleet.id,
            };
            const merged_data = {...data_json, ...action_json}
            await socket.send(JSON.stringify(merged_data))
        })
        setFleetsMoveMode([])
    }
    /* In order to not lose contexts in child components when working with react-three-fiber */
    const ContextBridge = useContextBridge(SocketContext, UserInfoContext,  ReactReduxContext, PlanetListContext)

    return (
        <>
            {/* The stars enclosing the planets and sun */}
            <Stars/>
            {/* Ambient light to ensure objects are not completely dark*/}
            <ambientLight intensity={0.9}/>
            {/* Invisible plane to track hovers when having fleets on move mode */}
            <mesh name="plane" onClick={(e) => {
                if (fleetsMoveMode.length !== 0) moveTo(e)
            }} visible={false} onPointerMove={(e) => setHoverPos(e.point)} position={[0, 0, 0]}
                  scale={[1000, 0.1, 1000]}>
                <boxGeometry args={[1, 1, 1]}/>
            </mesh>
            {/* Render lines for fleets currently in move mode */}
            {
                fleetsMoveMode.map((obj, i) => {
                    return (
                        <Line color={"red"} key={i} name="line" points={[obj.pos, hoverPos]} lineWidth={2}/>
                    )
                })
            }
            {/* Bounds are for moving to the planet that was clicked last time*/}
            <Bounds fit clip observe margin={1.2}>
                {/*Display a sun in the center*/}
                <mesh position={[0, 0, 0]} scale={5} name={"solarin"}>
                    <sphereGeometry args={[2]}/>
                    <meshStandardMaterial emissive="white" emissiveIntensity={1} toneMapped={false}/>
                </mesh>
                {/*Display the fleets in the galaxy view */}
                {
                    fleetsInSpace.map((fleet,i) => {
                        return (
                            <Fleet key={i} fleet={fleet} moveTo={moveTo} toggleMoveMode={toggleMoveMode} decideMoving={fleetsMoveMode.length > 0} movingSelected={isMoveMode(fleet.id)}/>
                        )
                    })
                }
                {/* Propagating contexts */}
                <ContextBridge>
                    {/*Display the planets in the galaxy view*/}
                    {publicPlanets.map((planet, i) => {
                    return (
                        <Planet key={i} planet={planet}
                                privatePlanets={privatePlanets}
                                changePlanetId={props.changePlanetId}
                                fleetsMoveMode={fleetsMoveMode}
                                setViewMode={props.setViewMode}
                                moveTo={moveTo}
                        />
                    )
                })
                }
                </ContextBridge>
            </Bounds>
            <OrbitControls enablePan={false} makeDefault minPolarAngle={0} maxPolarAngle={Math.PI / 1.75}/>
        </>)
}

function ForwardCanvas(props) {
    const ContextBridge = useContextBridge(SocketContext, UserInfoContext,  ReactReduxContext, PlanetListContext);
    return (
        <Canvas
        flat shadows style={{position: "fixed", backgroundColor: "#0a0a0a"}} scene={{background: "black"}}>
            {/* Propagating contexts */}
            <ContextBridge>
                <Scene planetListIndex={props.planetListIndex} setViewMode={props.setViewMode} changePlanetId={props.changePlanetId}/>
            </ContextBridge>
      </Canvas>
    )

}
function GalaxyViewer(props) {
    /**
    * This component visualizes the view we would see when we are in space
    * */

    /*
     * This state and ref keep information about the websocket
     * */
    const isWebSocketConnected = useRef(false);
    const [socket, setSocket] = useState(null)
    useEffect(() => {
        if (isWebSocketConnected.current) return
        isWebSocketConnected.current = true;
        /*
        * The galaxy can be seen as planet 0, and so we can easily reuse all the logic for planets
        * */
        const webSocket = new WebSocket(`${process.env.REACT_APP_BACKEND_PATH_WEBSOCKET}/planet/ws/0`, `${localStorage.getItem('access-token')}`);
        setSocket(webSocket)



    },[])

    useEffect(() => {
        if (!socket) return
        socket.onclose = async (event) => {
            isWebSocketConnected.current = false;
            socket.close();
        }
    }, [socket])

    return (

        <PlanetIdContext.Provider value={0}>
        <SocketContext.Provider value={[socket, setSocket]}>
            <ForwardCanvas planetListIndex={props.planetListIndex} setViewMode={props.setViewMode} changePlanetId={props.changePlanetId}/>
        </SocketContext.Provider>
        </PlanetIdContext.Provider>
    )
}

export default GalaxyViewer