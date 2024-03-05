import { useLoader, Canvas} from '@react-three/fiber'
import { TextureLoader } from 'three/src/loaders/TextureLoader'
import { OrbitControls } from '@react-three/drei'

import planet00 from './planet_images/mars.svg'
import MilitaryViewer from '../UI/MilitaryViewer'


function PlanetViewer(props) {
    const planetMap = useLoader(TextureLoader, planet00)
    return (
        <>
        <MilitaryViewer/>
        <Canvas style={{position: "fixed"}}>
        <ambientLight intensity={2} />
        <OrbitControls autoRotate autoRotateSpeed={0.1} enableZoom={false} enablePan={false} enableRotate/>
        <mesh>
      <sphereGeometry args={[2]}/>
      <meshStandardMaterial map={planetMap}/>
        </mesh>
      </Canvas>
      </>
    )

}
export default PlanetViewer