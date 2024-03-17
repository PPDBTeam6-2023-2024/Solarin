import { MapInteractionCSS } from 'react-map-interaction';
import { useState, useEffect } from 'react';
import { RiArrowLeftSLine, RiArrowRightSLine } from "react-icons/ri";
import getCities from './CityViewer/getCities';
import CityManager from "./CityViewer/cityManager";


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

    {/*Get images of cities on map cities on the map*/}
    const [selectedCityId, setSelectedCityId] = useState(null);
    const [showCities, setShowCities] = useState(true);
    const [citiesLoaded, setCitiesLoaded] = useState(false)

    const handleCityClick = (cityId) => {
        setSelectedCityId(cityId);
        setShowCityManager(true);
        setShowCities(false);
    };
    const [cityImages,setCityImages] = useState([]);
    {/*Load cities from databank, and get images*/}
    useEffect(() => {
        const fetchCities = async () => {
            const cities = await getCities(1); // replace with actual planetID
            const cityElements = cities.map(city => ({
                ...city,
                onClick: () => handleCityClick(city.id),
            }));
            setCityImages(cityElements);
            setCitiesLoaded(true);
        };
        if (!citiesLoaded) {
            fetchCities();
        }
    }, [props.planetId, handleCityClick, citiesLoaded]);

    {/*handle closing of cityManager window*/}
    const [showCityManager, setShowCityManager] = useState(true);
    const handleCloseCityManager = () => {
        setShowCityManager(false);
        setSelectedCityId(null);
        setShowCities(true);
    }

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

                        {/*Display cities on the map*/}
                        {showCities && cityImages.map((city, index) => (
                          <img key={index} src={city.src} alt="city" style={city.style} onClick={city.onClick} />
                        ))}

                        {/*Display cityManager over the map*/}
                        {selectedCityId && showCityManager && (
                            <div style={{ position: 'absolute', top: 0, left: 0, width: '100%', height: '100%', zIndex: 20 }}>
                                <CityManager cityId={selectedCityId} primaryColor="black" secondaryColor="black" onClose={handleCloseCityManager} />
                            </div>
                        )}

            </MapInteractionCSS>

        }
        </>
    )
}
export default PlanetViewer;