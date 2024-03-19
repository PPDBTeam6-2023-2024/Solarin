import axios from "axios";
import army_example from "../Images/troop_images/Soldier.png"

const getArmies = async (planetId) => {
  try {
    axios.defaults.headers.common = {'Authorization': `Bearer ${localStorage.getItem('access-token')}`};
    const response = await axios.get(`${process.env.REACT_APP_BACKEND_PATH}/army/armies?planet_id=${planetId}`);
    if (response.status === 200 && Array.isArray(response.data)) {
      return response.data.map(army => ({
        id: army.id,
        x: army.x,
        y: army.y,
        src: army_example,
        style: {
          position: 'absolute',
          left: `${army.x * 100}%`,
          top: `${army.y * 100}%`,
          transform: 'translate(-50%, -50%)',
          maxWidth: '10%',
          maxHeight: '10%',
          zIndex: 15,
          cursor: 'pointer'
        },
        onClick: () => {
          console.log("handling click", army.id);
        },
      }));
    }
    return [];
  } catch (e) {
    console.error('Error getting armies:', e);
    return [];
  }
};

export default getArmies