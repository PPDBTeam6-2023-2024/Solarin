import axios from "axios";
import Records from "./../../UI/buildingImages.json"

// get all the buildings inside a given city
export const getBuildings = async (cityId) => {
    try {
        const response = await axios.get(`${process.env.REACT_APP_BACKEND_PATH}/cityManager/buildings/${cityId}`);
        if (response.status === 200 && Array.isArray(response.data)) {
            return response.data;
        }
        return [];
    } catch (e) {
        console.error('Error fetching buildings:', e);
        return [];
    }
};

export const getNewBuildingTypes = async (cityId) => {
    try {
        const response = await axios.get(`${process.env.REACT_APP_BACKEND_PATH}/cityManager/new_building_types/${cityId}`);
        if (response.status === 200 && Array.isArray(response.data)) {
            return response.data;
        }
        return [];
    } catch (e) {
        console.error('Error fetching new building types:', e);
        return [];
    }
};

export const createBuilding = async (cityId, BuildingType) => {
    try {
        const response = await axios.post(`${process.env.REACT_APP_BACKEND_PATH}/building/create_new_building/${cityId}/${BuildingType}`);
        if (response.status === 200) {
            return response.data;
        }
        return [];
    } catch (e) {
        console.error('Error creating new building:', e);
        return [];
    }
};

export const getResources = async () => {
    try {
        const response = await axios.get(`${process.env.REACT_APP_BACKEND_PATH}/logic/resources`);
        if (response.status === 200) {
            return response.data;
        }
    } catch (error) {
        console.error('Error fetching resources:', error);
        return [];
    }
};


export const collectResources = async (cityId, buildingId) => {
    try {
        const response = await axios.post(`${process.env.REACT_APP_BACKEND_PATH}/building/collect/${buildingId}`);
        if (response.status === 200) {
            return response.data;
        }
    } catch (error) {
        console.error('Error collecting resources:', error);
        return null;
    }
};

export const upgradeBuilding = async (cityId, buildingId) => {
    try {
        const response = await axios.post(`${process.env.REACT_APP_BACKEND_PATH}/building/upgrade_building/${buildingId}`);
        if (response.status === 200) {
            return response.data;
        }
    } catch (error) {
        console.error('Error upgrading building:', error);
        return null;
    }
};


export const getUpgradeCost = async (cityId) => {
    try {
        const response = await axios.get(`${process.env.REACT_APP_BACKEND_PATH}/cityManager/get_upgrade_cost/${cityId}`);
        if (response.status === 200) {
            return response.data;
        }
    } catch (error) {
        console.error('Error retrieving upgrade cost:', error);
        return null;
    }
};

// get all the armies that are currently in the given city
export const getArmyInCity = async (cityId) => {
    try {
        const response = await axios.get(`${process.env.REACT_APP_BACKEND_PATH}/army/army_in_city/${cityId}`);
        if (response.status === 200) {
            return response.data;
        }
    } catch (error) {
        console.error('Error retrieving armies in a city:', error);
        return null;
    }
};


export const getImageForBuildingType = (buildingType) => {
    if (Records && Records[buildingType]) {
        return `${process.env.PUBLIC_URL}/Images/building_images/${Records[buildingType].icon}`;
    }
    return null;
}

export const upgradeCity = async (cityId) => {
    try {
        const response = await axios.get(`${process.env.REACT_APP_BACKEND_PATH}/cityManager/upgrade_city/${cityId}`);
        if (response.status === 200) {
            return response.data;
        }
    } catch (error) {
        console.error('Error upgrading city', error);
        return null;
    }
    return null;
}

export const getResourcesInStorage = async (cityId) =>{
    try{
        const response = await axios.get(`${process.env.REACT_APP_BACKEND_PATH}/cityManager/get_resource_stocks/${cityId}`);
        if (response.status === 200) {
            return response.data;
        }
    } catch (error){
        console.error('Error retrieving resources in storage', error);
        return null;
    }
}
