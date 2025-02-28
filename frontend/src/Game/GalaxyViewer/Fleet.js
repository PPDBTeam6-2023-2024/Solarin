import React, {useContext, useState, useEffect, useRef} from "react";
import {UserInfoContext} from "../Context/UserInfoContext";
import {Html, useContextBridge} from "@react-three/drei";
import {SocketContext} from "../Context/SocketContext";
import {PrimaryContext, SecondaryContext, TertiaryContext, TextColorContext} from "../Context/ThemeContext";
import {ReactReduxContext} from "react-redux";
import {animated} from "@react-spring/three";
import {Box, List, ListItemButton, Popper} from "@mui/material";
import ArmyViewer from "../UI/ArmyViewer/ArmyViewer";
import {useFrame} from '@react-three/fiber'
import { Gltf} from "@react-three/drei";
import {MathUtils} from "three"
import {lerp} from "../Armies/ArmyMovement"
/* spaceship model credit: "Ameaterasu" (https://skfb.ly/oTpuL) by gavinpgamer1 */

const Fleet = ({moveTo, fleet, decideMoving, movingSelected, toggleMoveMode}) => {

    /**
     * Display a spaceship in space
     * */

    /*
    * Store reference to the fleet object, to be able to do some visual manipulation
    * */
    const fleetRef = useRef()

    /*
    * Store whether the fleet is clicked (selected)
    * */
    const [clicked, setClicked] = useState(false)
    const [userInfo] = useContext(UserInfoContext);

    /*
    * Keeps track whether the details menu of this army is opened
    * */
    const [detailsOpen, setDetailsOpen] = useState(false)
    const [anchorEl, setAnchorEl] = useState(null)

    /*
    * ContextBridge is used, to make sure certain contexts are still applicable
    * */
    const ContextBridge = useContextBridge(SocketContext, ReactReduxContext, PrimaryContext,
        SecondaryContext, TertiaryContext, TextColorContext)

    /*
    * Keep track of the current position of the army (=fleet)
    * */
    const [currentPos, setCurrentPos] = useState(lerp({
        sourcePosition: {x: fleet.x, y: fleet.y}, targetPosition: {x: fleet.to_x, y: fleet.to_y},
        arrivalTime:  new Date(fleet.arrivalTime).getTime(), departureTime: new Date(fleet.departureTime).getTime()
    }))

    /*
    * Rotate the fleet into the right direction
    * */
    useEffect(() => {
        fleetRef.current.rotation.y = Math.atan2(fleet.to_x - currentPos.x, fleet.to_y - currentPos.y) + Math.PI
    }, [])

    useFrame(() => {
        const currentPos = lerp({
            sourcePosition: {x: fleet.x, y: fleet.y}, targetPosition: {x: fleet.to_x, y: fleet.to_y},
            arrivalTime:  new Date(fleet.arrivalTime).getTime(), departureTime: new Date(fleet.departureTime).getTime()
        })
        const notArrived = fleet.to_x !== currentPos.x || fleet.to_y !== currentPos.y
        if(notArrived) {
            const dx = fleet.to_x - currentPos.x;
            const dy = fleet.to_y - currentPos.y;
            const angle = Math.atan2(dx, dy) + Math.PI

            fleetRef.current.rotation.y = MathUtils.lerp(fleetRef.current.rotation.y, angle, 0.05)
        }
        fleetRef.current.position.set(currentPos.x*50, 0, currentPos.y*50)
    })
    const [isHovering, setIsHovering] = useState(false)
    useEffect(() => {
        if(isHovering && decideMoving) {
        if(fleet.owner !== userInfo.id) document.body.style.cursor = "url(/images/cursors/attack_cursor.png) 1 1, auto"
        else if(!movingSelected) document.body.style.cursor = "url(/images/cursors/merge_cursor.png) 1 1, auto"
        }
        else document.body.style.cursor = "auto"
    }, [isHovering])
    const fleetOnClick = (e) => {
        e.stopPropagation()
        if(!decideMoving) setClicked(!clicked)
        else {
            if (fleet.owner !== userInfo.id) moveTo(e,
                {
                    on_arrive: true,
                    target_type: "attack_army",
                    target_id: fleet.id
                })
            else moveTo(e, {
                on_arrive: true,
                target_type: "merge",
                target_id: fleet.id
            })
        }
    }
    return (
        <animated.mesh name="fleet" onPointerLeave={() => setIsHovering(false)} onPointerEnter={() => setIsHovering(true)}
                        onClick={fleetOnClick} ref={fleetRef}>
            <spotLight target={fleetRef.current} distance={2} position={[0,0.75,0]} intensity={1} scale={1}/>
            <Gltf src={"/3dmodels/ameaterasu.glb"} scale={0.025} receiveShadow />
            {clicked &&
                <Html>
                    <Box className="bg-black rounded-xl border border-white">
                        <List>
                            {fleet.owner === userInfo.id && <ListItemButton
                                onClick={() => toggleMoveMode(fleet.id, fleetRef.current.position)}>{!movingSelected ? 'Move To' : "Cancel Move To"}</ListItemButton>}
                            <ListItemButton className="whitespace-nowrap" onClick={(e) => {
                                setDetailsOpen(!detailsOpen);
                                setAnchorEl(e.currentTarget)
                            }}>
                                {!detailsOpen ? "Open Stats" : "Close Stats"}
                            </ListItemButton>
                        </List>
                    </Box>
                    <ContextBridge>
                        <Popper open={detailsOpen} anchorEl={anchorEl} placement='right-start'>
                            <ArmyViewer armyId={fleet.id} is_owner={fleet.owner === userInfo.id} in_space={true}/>
                        </Popper>
                    </ContextBridge>
                </Html>
            }
        </animated.mesh>
    )
}
export default Fleet