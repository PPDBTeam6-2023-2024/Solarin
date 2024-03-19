import {MapInteractionCSS} from 'react-map-interaction';
import {useState, useEffect} from 'react';
import {RiArrowLeftSLine, RiArrowRightSLine} from "react-icons/ri";
import ArmyViewer from '../UI/armyViewer/armyViewer'
import getArmies from "./getArmies";

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

    const [image, setImage] = useState()
    const [showArmyViewer, setShowArmyViewer] = useState(false)
    const [armiesLoaded, setArmiesLoaded] = useState(false)
    const [ArmyViewerPosition, setArmyViewerPosition] = useState({x: 0, y: 0});
    const [armyImages, setArmyImages] = useState([])

    const toggleArmyViewer = (e, armyid) => {
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
        const fetchArmies = async () => {
            const armies = await getArmies(1);
            const armyElements = armies.map(army => ({
                ...army,
                onClick: (e) => toggleArmyViewer(e, army.id),
            }));
            setArmyImages(armyElements)
            setArmiesLoaded(true);
        };
        if (!armiesLoaded) {
            fetchArmies();
        }
    }, [toggleArmyViewer, armiesLoaded]);

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

                    {armyImages.map((army, index) => (
                        <img key={index} src={army.src} alt="army" style={army.style} onClick={army.onClick}/>
                    ))}
                </MapInteractionCSS>
            }
        </>
    )
}

export default PlanetViewer;