import { MapInteractionCSS } from 'react-map-interaction';
import { useState, useEffect } from 'react';
import { RiArrowLeftSLine, RiArrowRightSLine } from "react-icons/ri";


const loadImage = async(imgPath, stateSetter) => {
    let img = new Image()
    img.src = imgPath
    img.onload = () => {
        stateSetter(img)
    }
}

function PlanetViewer(props) {
    const [mapState, setMapState] = useState({
        scale: 1,
        translation: {x: 0, y:0},
    })

    const [image, setImage] = useState()
    useEffect(() => {
        loadImage(props.mapImage, setImage)
    }, [props.mapImage])
    return (
        <>
        <div className="bg-gray-800 mx-auto w-2/12 py-3 fixed inset-x-0 top-5 z-10 border-2 border-white md:text-3xl justify-between items-center flex">
        <RiArrowLeftSLine className="transition ease-in-out hover:scale-150"/>
         <h1>{props.planetName}</h1>
         <RiArrowRightSLine className="transition ease-in-out hover:scale-150"/>
         </div>
        {
        image &&
    <MapInteractionCSS minScale={1} maxScale={5} translationBounds={{xMin: image.width-mapState.scale*image.width, xMax: 0, yMin: image.height-mapState.scale*image.height, yMax: 0}} value={mapState} onChange={(value) => {setMapState(value)}}>
      <img src={image.src} alt="map" style={{imageRendering: "pixelated", width:"100vw"}} />
    </MapInteractionCSS>
        }
        </>
    )
}
export default PlanetViewer;