import { useLoader, Canvas } from '@react-three/fiber'
import { TextureLoader } from 'three/src/loaders/TextureLoader'
import { OrbitControls, Bounds, useBounds } from '@react-three/drei'
import { useState, useEffect } from 'react'
import {useSpring, animated} from '@react-spring/three'
import axios from 'axios'

import {View} from "../Context/ViewModeContext"

// inspiration: https://codesandbox.io/p/sandbox/bounds-and-makedefault-rz2g0?file=%2Fsrc%2FApp.js%3A38%2C1-45%2C2

const SelectToZoom = ({ children }) => {
  const api = useBounds()
  return (
    <group onClick={(e) => (e.stopPropagation(), e.delta <= 2 && api.refresh(e.object).fit())} onPointerMissed={(e) => e.button === 0 && api.refresh().fit()}>
      {children}
    </group>
  )
}


function GalaxyViewer(props) {
    const [planets, setPlanets] = useState([])
    useEffect(() => {
        const fetchPlanets = async() => {
          const response = await axios.get(`${process.env.REACT_APP_BACKEND_PATH}/planet/planets/private`)
          setPlanets(response.data)
          console.log(response.data)
        }
        fetchPlanets()
    }, [])
    const planetMap = useLoader(TextureLoader, '/images/Planets/example.png')
    const [isHovering, setIsHovering] = useState(false)
    const {scale} = useSpring({scale: (isHovering) ? [1.05,1.05,1.05]: [1,1,1]})
    return (
        <Canvas camera={{ position: [0, -10, 80], fov: 50 }} dpr={[1, 2]} style={{position: "fixed"}}>
        <ambientLight intensity={(isHovering) ? 1.1 : 1} />
        <OrbitControls autoRotate autoRotateSpeed={0.1} enableZoom={false} enablePan={false} enableRotate/>
        <Bounds fit clip observe margin={1.2}>
          { planets.map((planet) => {
                <SelectToZoom>
              <animated.mesh scale={scale} onPointerEnter={() => setIsHovering(true)} onPointerLeave={() => setIsHovering(false)} onDoubleClick={() => {props.setViewMode(View.PlanetView)}}>
              <sphereGeometry args={[2]}/>
              <meshStandardMaterial map={planetMap}/>
              </animated.mesh>
              </SelectToZoom>
          })
          }
        </Bounds>

      </Canvas>
    )

}

export default GalaxyViewer