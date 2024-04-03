// CityManager.js
import React, { useState, useEffect, useMemo, useContext} from 'react';
import 'ag-grid-community/styles/ag-grid.css';
import 'ag-grid-community/styles/ag-theme-alpine.css';
import './CityManager.css';
import {
    getBuildings,
    getImageForBuildingType,
    getNewBuildingTypes,
    getResources, refreshResourceAmount
} from './BuildingManager';
import {UserInfoContext} from "../../Context/UserInfoContext";
import NewBuildingGrid from './Grids/NewBuildingGrid';
import WindowUI from '../../UI/WindowUI/WindowUI';
import TrainingViewer from "../../UI/TrainingUnits/TrainingViewer";
import RenderGrid from "./Grids/CurrentBuildingGrid"

const CityManager = ({ cityId, primaryColor, secondaryColor, onClose }) => {
    const [buildings, setBuildings] = useState([]);
    const [newBuildingTypes, setNewBuildingTypes] = useState([]);
    const [resources, setResources] = useState([]);
    const [selectedImage, setSelectedImage] = useState(null);

    const [userInfo, setUserInfo] = useContext(UserInfoContext)

    /* stores selected building*/
    const [selectedClick, setSelectedClick] = useState([-1, ""]);
    const [initialClick, setInitialClick] = useState(true);

    const [selectedTab, setSelectedTab] = useState('currentBuildings');



    useEffect(() => {
        if (cityId && buildings.length === 0) {
            getBuildings(cityId).then(buildings => {
                setBuildings(buildings)
            });
            getNewBuildingTypes(cityId,0).then(newBuildingTypes => {
                setNewBuildingTypes(newBuildingTypes)
            });
            refreshResourceAmount(cityId) /*update resource viewer here*/
            getResources().then(availableResources => {
                setResources(availableResources)
            })
        }
    }, [cityId, buildings]);

    const updateBuildingsAndTypes = () => {
    getBuildings(cityId).then(setBuildings);
    getNewBuildingTypes(cityId, 0).then(setNewBuildingTypes);
};


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
            <WindowUI>
                <div className="building_view">
                    <div className="tabs">
                        <button onClick={() => setSelectedTab('currentBuildings')}>Current Buildings</button>
                        <button onClick={() => setSelectedTab('newBuildings')}>New Buildings</button>
                        <button onClick={() => setSelectedTab('ArmyGrid')}>Army</button>
                        <button onClick={() => setSelectedTab('plus')}>+</button>
                    </div>

                    {selectedTab === 'currentBuildings' && <RenderGrid
                        buildings={buildings}
                        onRowMouseOver={onRowMouseOver}
                        setSelectedClick={setSelectedClick}
                        selectedClick={selectedClick}
                        selectedImage={selectedImage}
                        cityId={cityId}
                    />}
                    {selectedTab === 'newBuildings' && (
                              <NewBuildingGrid
                                buildings={newBuildingTypes}
                                onRowMouseOver={onRowMouseOver}
                                setSelectedClick={setSelectedClick}
                                selectedImage={selectedImage}
                                cityId={cityId}
                                updateBuildingsAndTypes={updateBuildingsAndTypes}
                                resources={resources}
                              />
                            )}

                    {selectedTab === 'plus' && <div>Additional content here</div>}

                    {/*Displays a training menu*/}
                    {selectedTab === 'currentBuildings' && selectedClick[0] !== -1 && selectedClick[1] === "Barracks" && <TrainingViewer key={selectedClick[0]} building_id={selectedClick[0]}/>}

                    {/*{selectedTab === 'currentBuildings' && selectedClick[0] !== -1 && selectedClick[1] === "productionBuilding">}*/}

                </div>
            </WindowUI>
        </div>
    );
};

export default CityManager;
