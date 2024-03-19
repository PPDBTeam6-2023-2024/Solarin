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
    });
    const [image, setImage] = useState();
    const [armyImages, setArmyImages] = useState([]);
    const [activeArmyViewers, setActiveArmyViewers] = useState([]);
    const [updateTrigger, setUpdateTrigger] = useState(false);


    const toggleArmyViewer = (e, armyId) => {
        const overlayRect = e.target.getBoundingClientRect();
        const position = {
            x: overlayRect.left + window.scrollX,
            y: overlayRect.top + window.scrollY
        };

        setActiveArmyViewers(prev => {
            const index = prev.findIndex(viewer => viewer.id === armyId);
            if (index >= 0) {
                // Remove viewer if already active
                return prev.filter(viewer => viewer.id !== armyId);
            } else {
                return [...prev, {id: armyId, position}];
            }
        });
    };

    const updateArmyPosition = (armyId, newX, newY) => {
        setArmyImages(currentArmyImages => currentArmyImages.map(army => {
            if (army.id === armyId) {
                return {...army, x: newX, y: newY};
            }
            return army;
        }));
        setUpdateTrigger(prev => !prev)
    };

    useEffect(() => {
        loadImage(props.mapImage, setImage);
    }, [props.mapImage]);

    useEffect(() => {
        const fetchArmies = async () => {
            const armies = await getArmies(1);
            const armyElements = armies.map(army => ({
                ...army,
                onClick: (e) => toggleArmyViewer(e, army.id),
            }));
            setArmyImages(armyElements);
        };
        fetchArmies();

    }, [updateTrigger]); // get the armies again when an army has been moved


    return (
        <>
            <div
                className="bg-gray-800 mx-auto w-2/12 py-3 fixed inset-x-0 top-5 z-10 border-2 border-white md:text-3xl justify-between items-center flex">
                <RiArrowLeftSLine className="transition ease-in-out hover:scale-150"/>
                <h1>{props.planetName}</h1>
                <RiArrowRightSLine className="transition ease-in-out hover:scale-150"/>
            </div>
            {
                activeArmyViewers.map(({id, position}) => (
                    <div key={id} style={{
                        position: 'absolute',
                        left: `${position.x}px`,
                        top: `${position.y}px`,
                    }}>
                        <ArmyViewer armyId={id} onUpdatePosition={updateArmyPosition}/>
                    </div>
                ))
            }
            {
                image &&
                <MapInteractionCSS
                    value={mapState}
                    onChange={(value) => setMapState(value)}
                    minScale={1}
                    maxScale={5}
                    translationBounds={{
                        xMin: image.width - mapState.scale * image.width,
                        xMax: 0,
                        yMin: image.height - mapState.scale * image.height,
                        yMax: 0,
                    }}
                >
                    <img src={image.src} alt="map"
                         style={{imageRendering: "pixelated", width: "100%", height: "auto"}}/>
                    {armyImages.map((army, index) => (
                        <img key={index} src={army.src} alt="army" style={army.style}
                             onClick={(e) => toggleArmyViewer(e, army.id)}/>
                    ))}

                </MapInteractionCSS>
            }
        </>
    );
}

export default PlanetViewer;
