import axios from "axios";
import {getCityImage} from "./GetCityImage";

const GetCities = async (planetId) => {
    try {
        const response = await axios.get(`${process.env.REACT_APP_BACKEND_PATH}/cityManager/cities/${planetId}`);
        if (response.status === 200 && Array.isArray(response.data)) {
            return response.data.map(city => ({
                id: city.id,
                x: city.x,
                y: city.y,
                controlled_by: city.controlled_by,
                rank : city.rank,
                src: getCityImage(city.rank),
                alliance: city.alliance,
                style: {
                    position: 'absolute',
                    left: `${city.x * 100}%`,
                    top: `${city.y * 100}%`,
                    transform: 'translate(-50%, -50%)',
                    maxWidth: '15%',
                    maxHeight: '15%',
                    zIndex: 15,
                },
                onClick: () => {
                    console.log("handling click", city.id);
                },
            }));
        }
        return [];
    } catch (e) {
        console.error('Error fetching cities:', e);
        return [];
    }
};

export default GetCities;
