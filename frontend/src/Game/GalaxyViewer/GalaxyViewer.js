import { useLoader, Canvas } from '@react-three/fiber'
import { TextureLoader } from 'three/src/loaders/TextureLoader'
import { OrbitControls } from '@react-three/drei'
import { useState} from 'react'
import {useSpring, animated} from '@react-spring/three'

import {View} from "../Context/ViewModeContext"


function GalaxyViewer(props) {
    const planetMap = useLoader(TextureLoader, props.mapImage)
    const [isHovering, setIsHovering] = useState(false)
    const {scale} = useSpring({scale: (isHovering) ? [1.05,1.05,1.05]: [1,1,1]})
    return (
        <Canvas style={{position: "fixed"}}>
        <ambientLight intensity={(isHovering) ? 1.1 : 1} />
        <OrbitControls autoRotate autoRotateSpeed={0.1} enableZoom={false} enablePan={false} enableRotate/>

        <animated.mesh scale={scale} onPointerEnter={() => setIsHovering(true)} onPointerLeave={() => setIsHovering(false)} onDoubleClick={() => {props.setViewMode(View.PlanetView)}}>
        <sphereGeometry args={[2]}/>
        <meshStandardMaterial map={planetMap}/>
        </animated.mesh>

      </Canvas>
    )

}

export default GalaxyViewer