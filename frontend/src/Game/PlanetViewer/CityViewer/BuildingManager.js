// BuildingManager.js
import axios from "axios";
import barracks from "../../Images/building_images/Barracks.png";
import mine from "../../Images/building_images/Mine.png";
import factory from "../../Images/building_images/Factory.png";
import shipyard from "../../Images/building_images/Shipyard.png";

export const getBuildings = async (cityId) => {
    try {
        axios.defaults.headers.common = {'Authorization': `Bearer ${localStorage.getItem('access-token')}`};
        const response = await axios.get(`${process.env.REACT_APP_BACKEND_PATH}/cityManager/buildings?city_id=${cityId}`);
        console.log('Response data:', response.data);
        if (response.status === 200 && Array.isArray(response.data)) {
            return response.data;
        }
        return [];
    } catch (e) {
        console.error('Error fetching buildings:', e);
        return [];
    }
};

export const getImageForBuildingType = (buildingType) => {
    switch (buildingType) {
        case 'barracks':
            return barracks;
        case 'The mines of moria':
            return mine;
        case 'Solarin mansion':
            return factory;
        case 'space-dock':
            return shipyard;
        default:
            return barracks;
    }
};
