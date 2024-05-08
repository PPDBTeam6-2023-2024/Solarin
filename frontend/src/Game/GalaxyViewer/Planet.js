import {animated} from "@react-spring/three";
import {View} from "../Context/ViewModeContext";
import {Html, useBounds} from "@react-three/drei";
import {IoMdClose} from "react-icons/io";
import Tooltip from "@mui/material/Tooltip";
import React, {Fragment, useState, useContext, useEffect} from "react";
import axios from "axios";
import {useLoader} from "@react-three/fiber";
import {TextureLoader} from "three/src/loaders/TextureLoader";

import {UserInfoContext} from "../Context/UserInfoContext";
import {SocketContext} from "../Context/SocketContext";

// inspiration: https://codesandbox.io/p/sandbox/bounds-and-makedefault-rz2g0?file=%2Fsrc%2FApp.js%3A38%2C1-45%2C2

const SelectToZoom = ({ children, planetId, setPlanetSelected, isMoveMode}) => {
    const api = useBounds()
    const onClick = (e) => {
        if(!isMoveMode) {
            setPlanetSelected(planetId)
            e.stopPropagation()
            return e.delta <= 2 && api.refresh(e.object).fit()
        }

    }
    return (
        <group onClick={onClick}>
            {children}
        </group>
    )
}
function Planet({planet, fleetsMoveMode, privatePlanets, changePlanetId, setViewMode, moveTo}) {
    const [planetSelected, setPlanetSelected] = useState(null)

    const [showListedFleets, setshowListedFleets] = useState(false)
    const [listedFleets, setListedFleets] = useState([])
    const [userInfo, setUserInfo] = useContext(UserInfoContext)
    const [socket, setSocket] = useContext(SocketContext)

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

    const planetImages = {
        "terrestrial": useLoader(TextureLoader, "/images/Planets/terrestrial.png"),
        "tropical": useLoader(TextureLoader, "/images/Planets/tropical.png"),
        "desert": useLoader(TextureLoader, "/images/Planets/desert.png"),
        "arctic": useLoader(TextureLoader, "/images/Planets/arctic.png"),
        "red": useLoader(TextureLoader, "/images/Planets/red_planet.jpg"),
        "dry": useLoader(TextureLoader, "/images/Planets/dry.jpg"),
        "shadow": useLoader(TextureLoader, "/images/Planets/shadow.png")
    }

    const [isHovering, setIsHovering] = useState(false)
    useEffect(() => {
        if(isHovering && fleetsMoveMode.length !== 0) {
            document.body.style.cursor = 'url(/images/cursors/enter_cursor.png) 1 1, auto'
        }
        else document.body.style.cursor = "auto"
    }, [isHovering])
    const planetOnClick = (e) => {
        if(fleetsMoveMode.length !== 0) {
            moveTo(e,
            {on_arrive: true, target_type: "enter_planet", target_id: planet.id}
            )
        }
    }
    return (
        <Fragment key={planet.id}>
            <SelectToZoom setPlanetSelected={setPlanetSelected} planetId={planet.id} isMoveMode={fleetsMoveMode.length !== 0}>
                <animated.mesh name={"planet"}
                                onClick={planetOnClick}
                                onPointerEnter={() => setIsHovering(true)}
                               onPointerLeave={() => setIsHovering(false)}
                               position={[50 * planet.x, 0, 50 * planet.y]} onDoubleClick={() => {
                    if (privatePlanets.find((privatePlanet) => privatePlanet.id === planet.id)) {
                        changePlanetId(planet.id);
                        setViewMode(View.PlanetView)
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
                                    <div className="overflow-y-auto bg-black mx-2 p-2 border border-white">
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
}
export default Planet
