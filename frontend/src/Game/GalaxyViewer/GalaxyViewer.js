import { useLoader, Canvas, } from '@react-three/fiber'
import { TextureLoader } from 'three/src/loaders/TextureLoader'
import { OrbitControls } from '@react-three/drei'
import { WebGL1Renderer } from 'three'


function GalaxyViewer(props) {
    const planetMap = useLoader(TextureLoader, props.mapImage)
    return (
        <WebGL1Renderer>
        <Canvas style={{position: "fixed"}}>
        <ambientLight intensity={1} />
        <OrbitControls autoRotate autoRotateSpeed={0.1} enableZoom={false} enablePan={false} enableRotate/>
        <mesh>
      <sphereGeometry args={[2]}/>
      <meshStandardMaterial map={planetMap}/>
        </mesh>
      </Canvas>
      </WebGL1Renderer>
    )

}
export default GalaxyViewer