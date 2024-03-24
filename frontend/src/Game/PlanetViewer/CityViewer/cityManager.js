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
    const [buildings, setBuildings] = useState([]);
    const [selectedImage, setSelectedImage] = useState(null);

    /*stores which building has been clicked*/
    const [selectedClick, setSelectedClick] = useState(-1);

    const [initialClick, setInitialClick] = useState(true);

    const columns = useMemo(() => [
        { headerName: "Building Type", field: "buildingType" },
        { headerName: "Building Rank", field: "buildingRank" },
        { headerName: "Resource Timer", field: "resourceTimer" }
    ]);

    useEffect(() => {
        if (cityId && buildings.length === 0) {
            getBuildings(cityId).then(buildings => {
                setBuildings(buildings)
            });
        }
    }, [cityId, buildings]);

    const getImageForBuildingType = (buildingType) => {
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

    const onRowMouseOver = event => {
        setSelectedImage(event.data.image);
    };

    useEffect(() => {
        const handleClickOutside = event => {
            const { target } = event;
            const agGridElement = document.querySelector('.building_view');
            const selectedImageElement = document.querySelector('.selected-image');

            if (agGridElement.contains(target) || (selectedImageElement && selectedImageElement.contains(target))) {
                return;
            }

            if (!initialClick) {
                {/*case: Clicked outside AG Grid and the selected image*/}
                onClose();
            } else {
                {/*case: log initial click*/}
                setInitialClick(false);
            }
        };

        document.addEventListener('click', handleClickOutside);
        return () => document.removeEventListener('click', handleClickOutside);
    }, [onClose, initialClick]);


    return (
        <div className="darken_background">
                <Draggable>
                    <div className="building_view">
                        <div className="ag-theme-alpine-dark buildings_grid">
                            <AgGridReact
                                rowData={
                                    /*maps the building to a row*/
                                    buildings.map((building, index) => ({
                                        buildingType: building.building_type,
                                        buildingRank: building.rank,
                                        resourceTimer: 'Unknown',
                                        image: getImageForBuildingType(building.building_type),
                                        index: index
                                    }))
                                }
                                columnDefs={columns}
                                domLayout='autoHeight'
                                suppressMovableColumns={true}
                                suppressDragLeaveHidesColumns={true}
                                onCellMouseOver={onRowMouseOver}
                                onCellClicked={(event) => setSelectedClick(event.data.index)}
                                onGridReady={params => params.api.sizeColumnsToFit()}
                                onGridSizeChanged={params => params.api.sizeColumnsToFit()}
                            />

                        </div>
                        <div className="building_image">
                            {selectedImage && <img src={selectedImage} alt="Building" className="selected-image" />}
                        </div>
                    </div>
                </Draggable>

        </div>
    );
};

export default CityManager;
