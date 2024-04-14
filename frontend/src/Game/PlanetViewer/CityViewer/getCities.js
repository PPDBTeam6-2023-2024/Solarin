// getCities.js
import axios from "axios";
import {getCityImage} from "./getCityImage";

const getCities = async (planetId) => {
  try {
    axios.defaults.headers.common = {'Authorization': `Bearer ${localStorage.getItem('access-token')}`};
    const response = await axios.get(`${process.env.REACT_APP_BACKEND_PATH}/cityManager/cities?planet_id=${planetId}`);
    if (response.status === 200 && Array.isArray(response.data)) {
      return response.data.map(city => ({
        id: city.id,
        x: city.x,
        y: city.y,
        controlled_by: city.controlled_by,
        src: getCityImage(city.rank), // Assuming there's a 'type' field to determine the city image
        style: {
          position: 'absolute',
          left: `${city.x * 100}%`,
          top: `${city.y * 100}%`,
          transform: 'translate(-50%, -50%)',
          maxWidth: '15%',
          maxHeight: '15%',
          zIndex: 15
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

export default getCities;
