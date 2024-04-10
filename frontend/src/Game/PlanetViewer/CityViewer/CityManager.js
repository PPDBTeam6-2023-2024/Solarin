// CityManager.js
import React, { useState, useEffect, useMemo, useContext} from 'react';
import 'ag-grid-community/styles/ag-grid.css';
import 'ag-grid-community/styles/ag-theme-alpine.css';
import './CityManager.css';
import {
    GetArmyInCity,
    getBuildings,
    getNewBuildingTypes,
    getResources, getUpgradeCost, refreshResourceAmount
} from './BuildingManager';
import {UserInfoContext} from "../../Context/UserInfoContext";
import NewBuildingGrid from './Grids/NewBuildingGrid';
import WindowUI from '../../UI/WindowUI/WindowUI';
import TrainingViewer from "../../UI/TrainingUnits/TrainingViewer";
import CurrentBuildingGrid from "./Grids/CurrentBuildingGrid"
import ArmyGrid from "./Grids/ArmyGrid";
import {getImageForBuildingType, getImageForTroopType} from "../../UI/CityViewer/EntityViewer";

const CityManager = ({ cityId, primaryColor, secondaryColor, onClose }) => {
    const [buildings, setBuildings] = useState([]);
    const [upgradeCostMap, setUpgradeCostMap] = useState([]);
    const [newBuildingTypes, setNewBuildingTypes] = useState([]);
    const [resources, setResources] = useState([]);
    const [selectedImage, setSelectedImage] = useState(null);

    const [userInfo, setUserInfo] = useContext(UserInfoContext)

    /* stores selected building*/
    const [selectedClick, setSelectedClick] = useState([-1, ""]);
    const [initialClick, setInitialClick] = useState(true);

    const [selectedTab, setSelectedTab] = useState('currentBuildings');

    const [troops, setTroops] = useState([]); // State for troops




    useEffect(() => {
        if (cityId && buildings.length === 0) {
            refreshResourceAmount(cityId) /*update resource viewer here*/
            getBuildings(cityId).then(buildings => {
                setBuildings(buildings)
            });
            getUpgradeCost(cityId).then(buildings => {
                  const costMap = buildings.reduce((acc, building) => {
                    acc[building.id] = building;
                    return acc;
                  }, {});
                  setUpgradeCostMap(costMap);
            });
            getNewBuildingTypes(cityId,0).then(newBuildingTypes => {
                setNewBuildingTypes(newBuildingTypes)
            });
            getResources().then(availableResources => {
                setResources(availableResources)
            })

            GetArmyInCity(cityId).then(setTroops); // Fetch and set troops

        }
    }, [cityId, buildings]);

    const updateBuildingsAndTypes = () => {
        {/* Refresh buildings and types after building/upgrading */}
        getBuildings(cityId).then(setBuildings);
        getNewBuildingTypes(cityId, 0).then(setNewBuildingTypes);
        getUpgradeCost(cityId).then(buildings => {
                  const costMap = buildings.reduce((acc, building) => {
                    acc[building.id] = building;
                    return acc;
                  }, {});
                  setUpgradeCostMap(costMap);
            });
    };

    const onRowMouseOver = event => {
        if (selectedTab === 'Army'){
            setSelectedImage(getImageForTroopType(event.data.troopType))
        } else if(selectedTab === "newBuildings"){
            setSelectedImage(getImageForBuildingType(event.data.name));
        } else{
            setSelectedImage(getImageForBuildingType(event.data.buildingType));
        }
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
                        <button onClick={() => setSelectedTab('Army')}>Army</button>
                    </div>

                    {selectedTab === 'currentBuildings' && <CurrentBuildingGrid
                        buildings={buildings}
                        onRowMouseOver={onRowMouseOver}
                        setSelectedClick={setSelectedClick}
                        selectedClick={selectedClick}
                        selectedImage={selectedImage}
                        cityId={cityId}
                        resources={resources}
                        upgradeCostMap={upgradeCostMap}
                        setUpgradeCostMap={setUpgradeCostMap}
                    />}
                    {selectedTab === 'newBuildings' &&
                              <NewBuildingGrid
                                buildings={newBuildingTypes}
                                onRowMouseOver={onRowMouseOver}
                                selectedImage={selectedImage}
                                cityId={cityId}
                                updateBuildingsAndTypes={updateBuildingsAndTypes}
                                resources={resources}
                              />
                            }

                    {selectedTab === 'Army' && <ArmyGrid
                        selectedClick={selectedClick}
                        onRowMouseOver={onRowMouseOver}
                        troops={troops}
                        setSelectedClick={setSelectedClick}
                        selectedImage={selectedImage}
                                />
                             }

                    {/*Displays a training menu*/}
                    {selectedTab === 'currentBuildings' && selectedClick[0] !== -1 && selectedClick[1] === "Barracks" &&
                        <TrainingViewer key={selectedClick[0]}
                                        building_id={selectedClick[0]}
                                        onClose={() => { selectedClick[0] = -1; selectedClick[1] = null}}

                        />}

                </div>
            </WindowUI>
        </div>
    );
};

export default CityManager;
