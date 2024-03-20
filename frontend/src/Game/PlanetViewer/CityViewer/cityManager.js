import React, { useState, useEffect, useMemo } from 'react';
import { AgGridReact } from 'ag-grid-react';
import 'ag-grid-community/styles/ag-grid.css';
import 'ag-grid-community/styles/ag-theme-alpine.css';
import './cityManager.css';
import Draggable from "react-draggable";
import barracks from "../../Images/building_images/Barracks.png";
import mine from "../../Images/building_images/Mine.png";
import factory from "../../Images/building_images/Factory.png";
import shipyard from "../../Images/building_images/Shipyard.png";
import axios from "axios";

const getBuildings = async (cityId) => {
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

const CityManager = ({ cityId, primaryColor, secondaryColor, onClose }) => {
    const [rowData, setRowData] = useState([]);
    const [selectedImage, setSelectedImage] = useState(null);
    const [initialClick, setInitialClick] = useState(true);
    const [buildings, setBuildings] = useState([]);

    const columns = useMemo(() => [
        { headerName: "Building Type", field: "buildingType" },
        { headerName: "Building Rank", field: "buildingRank" },
        { headerName: "Resource Timer", field: "resourceTimer" }
    ]);

    useEffect(() => {
        if (cityId && buildings.length === 0) {
            getBuildings(cityId).then(buildings => {
                setBuildings(buildings);
                setRowData(buildings.map(building => ({
                    buildingType: building.building_type,
                    buildingRank: building.rank,
                    resourceTimer: 'Unknown',
                    image: getImageForBuildingType(building.building_type)
                })));
            });
        }
    }, [cityId, buildings]);

    const getImageForBuildingType = (buildingType) => {
        switch (buildingType) {
            case 'barracks':
                return barracks;
            case 'reactor':
                return mine;
            case 'nexus':
                return factory;
            case 'space-dock':
                return shipyard;
            default:
                return barracks; // Default image or empty string if no match
        }
    };

    const onRowMouseOver = event => {
        setSelectedImage(event.data.image);
    };

    useEffect(() => {
        const handleClickOutside = event => {
            const { target } = event;
            const agGridElement = document.querySelector('.ag-theme-alpine-dark.ag-grid-container');
            const selectedImageElement = document.querySelector('.selected-image');

            if (agGridElement.contains(target) || (selectedImageElement && selectedImageElement.contains(target))) {
                return;
            }

            if (!initialClick) {
                console.log("Clicked outside AG Grid and the selected image!");
                onClose();
            } else {
                console.log("initial click logged");
                setInitialClick(false);
            }
        };

        document.addEventListener('click', handleClickOutside);
        return () => document.removeEventListener('click', handleClickOutside);
    }, [onClose, initialClick]);

    return (
        <div className="flex-container">
            <div className="left-container">
                <Draggable>
                    <div className="ag-theme-alpine-dark ag-grid-container">
                        <AgGridReact
                            rowData={rowData}
                            columnDefs={columns}
                            domLayout='autoHeight'
                            suppressMovableColumns={false}
                            suppressDragLeaveHidesColumns={true}
                            onCellMouseOver={onRowMouseOver}
                        />
                    </div>
                </Draggable>
            </div>
            <div className="right-container">
                {selectedImage && <img src={selectedImage} alt="Building" className="selected-image" />}
            </div>
        </div>
    );
};

export default CityManager;
