// CityManager.js
import React, {useState, useEffect, useMemo, useContext} from 'react';
import { AgGridReact } from 'ag-grid-react';
import 'ag-grid-community/styles/ag-grid.css';
import 'ag-grid-community/styles/ag-theme-alpine.css';
import './CityManager.css';
import Draggable from "react-draggable";
import { getBuildings, getImageForBuildingType } from './BuildingManager';
import {UserInfoContext} from "../../Context/UserInfoContext";

const CityManager = ({ cityId, primaryColor, secondaryColor, onClose }) => {
    const [buildings, setBuildings] = useState([]);
    const [selectedImage, setSelectedImage] = useState(null);

    const [userInfo, setUserInfo] = useContext(UserInfoContext)

    /* stores selected building*/
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
                console.log(buildings)
            });
        }
    }, [cityId, buildings]);

    const onRowMouseOver = event => {
        setSelectedImage(getImageForBuildingType(event.data.buildingType));
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
                console.log("test")
                console.log(userInfo)
                onClose();
            } else {
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
                            rowData={buildings.map((building, index) => ({
                                buildingType: building.building_type,
                                buildingRank: building.rank,
                                resourceTimer: 'Unknown',
                                image: getImageForBuildingType(building.building_type),
                                index: index
                            }))}
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
