import {MapInteractionCSS} from 'react-map-interaction';
import {useState, useEffect} from 'react';
import {RiArrowLeftSLine, RiArrowRightSLine} from "react-icons/ri";
import ArmyViewer from '../UI/armyViewer/armyViewer'

const loadImage = async (imgPath, stateSetter) => {
    let img = new Image()
    img.src = imgPath
    img.onload = () => {
        stateSetter(img)
    }
}

function PlanetViewer(props) {

    const [mapState, setMapState] = useState({
        scale: 1,
        translation: {x: 0, y: 0},
    })
    // temporary constant position of the army until we can get the positions from the backend

    const temparmyPos = {x: 0.25, y: 0.5}
    const [image, setImage] = useState()
    const [overlayImage, setOverlayImage] = useState()
    const [showArmyViewer, setShowArmyViewer] = useState(false)

    const [ArmyViewerPosition, setArmyViewerPosition] = useState({x: 0, y: 0});

    const toggleArmyViewer = (e) => {
        const overlayRect = e.target.getBoundingClientRect();
        setArmyViewerPosition({
            x: overlayRect.left + window.scrollX,
            y: overlayRect.top + window.scrollY
        });
        setShowArmyViewer(!showArmyViewer);
    };


    useEffect(() => {
        loadImage(props.mapImage, setImage)
    }, [props.mapImage])

    useEffect(() => {
        if (props.armyImage) {
            loadImage(props.armyImage, setOverlayImage);
        }
    }, [props.armyImage]); // Dependency array containing props.overlayImageSrc

    return (
        <>
            <div
                className="bg-gray-800 mx-auto w-2/12 py-3 fixed inset-x-0 top-5 z-10 border-2 border-white md:text-3xl justify-between items-center flex">
                <RiArrowLeftSLine className="transition ease-in-out hover:scale-150"/>
                <h1>{props.planetName}</h1>
                <RiArrowRightSLine className="transition ease-in-out hover:scale-150"/>
            </div>
            {showArmyViewer && (
                <div style={{
                    position: 'absolute',
                    left: `${ArmyViewerPosition.x}px`,
                    top: `${ArmyViewerPosition.y}px`,
                }}>
                    <ArmyViewer/>
                </div>
            )}

            {
                image &&
                <MapInteractionCSS
                    minScale={1}
                    maxScale={5}
                    translationBounds={{
                        xMin: image.width - mapState.scale * image.width,
                        xMax: 0,
                        yMin: image.height - mapState.scale * image.height,
                        yMax: 0,
                    }}
                    value={mapState}
                    onChange={(value) => setMapState(value)}
                >
                    <img src={image.src} alt="map"
                         style={{imageRendering: "pixelated", width: "100%", height: "auto"}}/>
                    {overlayImage && (
                        <img
                            src={overlayImage.src}
                            alt="overlay"
                            onClick={toggleArmyViewer}
                            draggable={false}
                            style={{
                                position: 'absolute',
                                left: `${temparmyPos.x * 100}%`, // use value from db instead of temparmypos
                                top: `${temparmyPos.y * 100}%`,
                                width: "2vw", // this value was chosen arbitrarily, subject to change
                                height: "3vw",
                                cursor: "pointer",
                                transform: 'translate(-50%, -50%)',
                            }}
                        />
                    )}
                </MapInteractionCSS>
            }
        </>
    )
}

export default PlanetViewer;