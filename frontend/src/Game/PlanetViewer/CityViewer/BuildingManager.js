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

export const getNewBuildingTypes = async (cityId,cityRank) => {
    try {
        axios.defaults.headers.common = {'Authorization': `Bearer ${localStorage.getItem('access-token')}`};
        const response = await axios.get(`${process.env.REACT_APP_BACKEND_PATH}/cityManager/new_building_types?city_id=${cityId}&city_rank=${cityRank}`);
        if (response.status === 200 && Array.isArray(response.data)) {
            return response.data;
        }
        return [];
    } catch (e) {
        console.error('Error fetching new building types:', e);
        return [];
    }
};

export const createBuilding = async (cityId,BuildingType) => {
    try {
        axios.defaults.headers.common = {'Authorization': `Bearer ${localStorage.getItem('access-token')}`};
        const response = await axios.post(`${process.env.REACT_APP_BACKEND_PATH}/cityManager/create_new_building?city_id=${cityId}&building_type=${BuildingType}`);
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
        axios.defaults.headers.common = {'Authorization': `Bearer ${localStorage.getItem('access-token')}`};
        const response = await axios.get('/logic/resources');
        if (response.status === 200) {
            return response.data;
        }
    } catch (error) {
        console.error('Error fetching resources:', error);
        return [];
    }
};


export const refreshResourceAmount = async (cityId) => {
    try {
        axios.defaults.headers.common = {'Authorization': `Bearer ${localStorage.getItem('access-token')}`};
        const response = await axios.get(`${process.env.REACT_APP_BACKEND_PATH}/cityManager/update?city_id=${cityId}`);
        if (response.status === 200) {
            return response.data;
        }
        return null;
    } catch (error) {
        console.error('Error refreshing resources:', error);
        return null;
    }
};


export const collectResources = async (cityId, buildingId) => {
    try {
        axios.defaults.headers.common = {'Authorization': `Bearer ${localStorage.getItem('access-token')}`};
        const response = await axios.get(`${process.env.REACT_APP_BACKEND_PATH}/cityManager/collect?city_id=${cityId}&building_id=${buildingId}`);
        if (response.status === 200) {
            console.log(response.data);
            return response.data;
        }
    } catch (error) {
        console.error('Error collecting resources:', error);
        return null;
    }
};

export const upgradeBuilding = async (cityId, buildingId) => {
    try {
        axios.defaults.headers.common = {'Authorization': `Bearer ${localStorage.getItem('access-token')}`};
        const response = await axios.get(`${process.env.REACT_APP_BACKEND_PATH}/cityManager/upgrade_building?city_id=${cityId}&building_id=${buildingId}`);
        if (response.status === 200) {
            console.log(response.data);
            return response.data;
        }
    } catch (error) {
        console.error('Error upgrading building:', error);
        return null;
    }
};


export const getUpgradeCost = async (buildingId) => {
    try {
        axios.defaults.headers.common = {'Authorization': `Bearer ${localStorage.getItem('access-token')}`};
        const response = await axios.get(`${process.env.REACT_APP_BACKEND_PATH}/cityManager/get_upgrade_cost?building_id=${buildingId}`);
        if (response.status === 200) {
            console.log(response.data);
            return response.data;
        }
    } catch (error) {
        console.error('Error retrieving upgrade cost:', error);
        return null;
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
