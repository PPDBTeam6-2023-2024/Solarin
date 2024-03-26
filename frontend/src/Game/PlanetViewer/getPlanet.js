import axios from "axios";


export default async function getPlanet({planetId}) {
  try {
    const response = await axios.get(`${process.env.REACT_APP_BACKEND_PATH}/planet/${planetId}`);
    if (response.status === 200) {
      return response.data;
    }
    return null;
  } catch (e) {
    console.error('Error getting planet:', e);
    return null;
  }
};

