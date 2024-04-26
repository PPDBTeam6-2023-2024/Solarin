import { Canvas, useLoader} from '@react-three/fiber'
import { TextureLoader } from 'three/src/loaders/TextureLoader'
import { OrbitControls, Bounds, useBounds, Stars, Html} from '@react-three/drei'
import { useState, useRef, useEffect, Fragment } from 'react'
import {useSprings, animated} from '@react-spring/three'
import axios from 'axios'
import Tooltip from '@mui/material/Tooltip';


import {View} from "../Context/ViewModeContext"

// inspiration: https://codesandbox.io/p/sandbox/bounds-and-makedefault-rz2g0?file=%2Fsrc%2FApp.js%3A38%2C1-45%2C2

const SelectToZoom = ({ children, planetId, setPlanetSelected}) => {
  const api = useBounds()
  const pointerMissed = (e) => {
    setPlanetSelected(null)
    return e.button === 0 && api.refresh().fit()
  }
  return (
    <group onClick={(e) => (setPlanetSelected(planetId), e.stopPropagation(), e.delta <= 2 && api.refresh(e.object).fit())} onPointerMissed={pointerMissed}>
      {children}
    </group>
  )
}


function GalaxyViewer(props) {
    const [publicPlanets, setPublicPlanets] = useState([])
    const [privatePlanets, setPrivatePlanets] = useState([])
    const solarinRef = useRef(null)
    useEffect(() => {
        const fetchPublicPlanets = async() => {
          const response = await axios.get(`${process.env.REACT_APP_BACKEND_PATH}/planet/planets/public`)
          setPublicPlanets(response.data)
        }
        const fetchPrivatePlanets = async() => {
          const response = await axios.get(`${process.env.REACT_APP_BACKEND_PATH}/planet/planets/private`)
          console.log(response.data)
          setPrivatePlanets(response.data)
        }
        fetchPublicPlanets()
        fetchPrivatePlanets()

    }, [])
    const [isHovering, setIsHovering] = useState([])
    const [planetSelected, setPlanetSelected] = useState(null)
    const planetImages = {
      "terrestrial": useLoader(TextureLoader, "/images/Planets/terrestrial.png"),
      "tropical": useLoader(TextureLoader, "/images/Planets/tropical.png"),
      "desert": useLoader(TextureLoader, "/images/Planets/desert.png"),
      "arctic": useLoader(TextureLoader, "/images/Planets/arctic.png")
    }
    /*const getScale = (id) => {
      const {scale} = useSpring({scale: (isHovering.find((id) => id == )) ? [1.05,1.05,1.05]: [1,1,1]})
      return scale
    }*/
    return (
      <>
        <Canvas style={{position: "fixed", backgroundColor: "#0a0a0a"}} scene={{background: "black"}}>
        <Stars/>
        <ambientLight intensity={0.9}/>
        <mesh ref={solarinRef} position={[0,0,0]} scale={5}>
          <sphereGeometry args={[2]}/>
          <meshStandardMaterial emissive="white" emissiveIntensity={1} toneMapped={false}/>
          </mesh>
        <Bounds fit clip observe margin={1.2}>
          { publicPlanets.map((planet) => {
            return (
              <Fragment key={planet.id}>
              <SelectToZoom setPlanetSelected={setPlanetSelected} planetId={planet.id}>
              <animated.mesh position={[50*planet.x,0, 50*planet.y]} onPointerEnter={() => setIsHovering([...isHovering, planet.id])} onPointerLeave={() => setIsHovering(isHovering.filter(id => id !== planet.id))} onDoubleClick={() => {if(privatePlanets.find((privatePlanet) => privatePlanet.id === planet.id)) {props.changePlanetId(planet.id); props.setViewMode(View.PlanetView)}}}>
              <sphereGeometry args={[2]}/>
              <meshStandardMaterial map={planetImages[planet.planet_type]}/>
              { planetSelected === planet.id &&
              <Html>
                <div className="bg-black whitespace-nowrap p-2">
                Name: {planet.name} <br></br>
                Type: {planet.planet_type}
                {
                  !privatePlanets.find((privatePlanet) => privatePlanet.id === planet.id) ?
                  <p className="text-red-500">You have no armies or cities here</p>
                  : <p className="text-green-500">Double-click on planet to enter planet view</p>
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
        <OrbitControls enablePan={false} makeDefault minPolarAngle={0} maxPolarAngle={Math.PI / 1.75} />
      </Canvas>
      </>
    )

}

export default GalaxyViewer