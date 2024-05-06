import React, {useContext, useState, useEffect, useRef} from "react";
import {UserInfoContext} from "../Context/UserInfoContext";
import {Html, useContextBridge} from "@react-three/drei";
import {SocketContext} from "../Context/SocketContext";
import {ReactReduxContext} from "react-redux";
import {animated} from "@react-spring/three";
import {Box, List, ListItemButton, Popper} from "@mui/material";
import ArmyViewer from "../UI/ArmyViewer/ArmyViewer";
import {useFrame} from '@react-three/fiber'
import { Gltf} from "@react-three/drei";
import {MathUtils} from "three"

// spaceship model credit: "Ameaterasu" (https://skfb.ly/oTpuL) by gavinpgamer1

const Fleet = ({fleet, isMoveMode, toggleMoveMode, mapOnClick}) => {
    const fleetRef = useRef()
    const [userInfo, setUserInfo] = useContext(UserInfoContext);

    const [clicked, setClicked] = useState(false)
    const [detailsOpen, setDetailsOpen] = useState(false)
    const [anchorEl, setAnchorEl] = useState(null)

    const ContextBridge = useContextBridge(SocketContext, ReactReduxContext)

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

    useEffect(() => {}, [isMoveMode, toggleMoveMode])

    useFrame(() => {
        const arrivalTime = new Date(fleet.arrivalTime).getTime()
        const departureTime = new Date(fleet.departureTime).getTime()
        const currentPos = lerp({
            sourcePosition: {x: fleet.x, y: fleet.y}, targetPosition: {x: fleet.to_x, y: fleet.to_y},
            arrivalTime: arrivalTime, departureTime: departureTime
        })
        if(fleet.to_x !== currentPos.x || fleet.to_y !== currentPos.y) {
            const dx = fleet.to_x - currentPos.x;
            const dy = fleet.to_y - currentPos.y;
            const angle = Math.atan2(dx, dy) + Math.PI

            fleetRef.current.rotation.y = MathUtils.lerp(fleetRef.current.rotation.y, angle, 0.0005)
        }
        fleetRef.current.position.set(currentPos.x, 0, currentPos.y)
    })
    return (
        <animated.mesh key={fleet.id} onClick={(e) => {setClicked(!clicked);mapOnClick(e)}} ref={fleetRef}>
            <pointLight intensity={100} scale={2}/>
            <Gltf src={"/3dmodels/ameaterasu.glb"} scale={0.1} receiveShadow />
            {clicked &&
                <Html>
                    <Box className="bg-black rounded-xl border border-white">
                        <List>
                            {fleet.owner === userInfo.id && <ListItemButton
                                onClick={() => toggleMoveMode(fleet.id, fleetRef.current.position)}>{!isMoveMode() ? 'Move To' : "Cancel Move To"}</ListItemButton>}
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
                            <ArmyViewer armyId={fleet.id} is_owner={fleet.owner === userInfo.id}/>
                        </Popper>
                    </ContextBridge>
                </Html>
            }
        </animated.mesh>
    )
}
export default Fleet