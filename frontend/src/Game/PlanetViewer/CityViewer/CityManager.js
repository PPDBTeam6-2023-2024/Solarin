// CityManager.js
import React, {useState, useEffect, useMemo, useContext, useCallback} from 'react';
import 'ag-grid-community/styles/ag-grid.css';
import 'ag-grid-community/styles/ag-theme-alpine.css';
import './CityManager.css';
import {
    getArmyInCity,
    getBuildings,
    getNewBuildingTypes,
    getResources, getUpgradeCost, refreshResourceAmount
} from './BuildingManager';
import NewBuildingGrid from './Grids/NewBuildingGrid';
import WindowUI from '../../UI/WindowUI/WindowUI';
import TrainingViewer from "../../UI/TrainingUnits/TrainingViewer";
import CurrentBuildingGrid from "./Grids/CurrentBuildingGrid"
import ArmyGrid from "./Grids/ArmyGrid";
import {getImageForBuildingType, getImageForTroopType} from "../../UI/CityViewer/EntityViewer";
import { initializeResources } from "../../UI/ResourceViewer/ResourceViewer"
import {useDispatch} from 'react-redux'


const CityManager = ({ cityId, primaryColor, secondaryColor, onClose , cityContextMap, setCityContextMap}) => {
     const dispatch = useDispatch();
    const [buildings, setBuildings] = useState([]);
    const [upgradeCostMap, setUpgradeCostMap] = useState([]);
    const [newBuildingTypes, setNewBuildingTypes] = useState([]);
    const [troops, setTroops] = useState([]); // State for troops

    const [selectedImage, setSelectedImage] = useState(null);

    /* stores selected building*/
    const [selectedClick, setSelectedClick] = useState([-1, ""]);
    const [initialClick, setInitialClick] = useState(true);

    const [selectedTab, setSelectedTab] = useState('currentBuildings');


    const cityContextLoader = (() => {

        if (!(cityId in cityContextMap)) {
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
            getNewBuildingTypes(cityId).then(newBuildingTypes => {
                setNewBuildingTypes(newBuildingTypes)
            });
            getArmyInCity(cityId).then(setTroops); // Fetch and set troops
        } else {
            setBuildings(cityContextMap[cityId].buildings)
            setUpgradeCostMap(cityContextMap[cityId].upgradeCostMap)
            setNewBuildingTypes(cityContextMap[cityId].newBuildingTypes)
            setTroops(cityContextMap[cityId].troops)
        }
    })


    const updateBuildingsAndTypes = () => {
        {/* Refresh buildings and types after building/upgrading */}
        getBuildings(cityId).then(setBuildings);
        getNewBuildingTypes(cityId).then(setNewBuildingTypes);
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
        cityContextLoader()
        setInitialClick(false);
    },[])

    const cityContextSaver = useCallback(() => {
        setCityContextMap(prevMap => ({
            ...prevMap,
            [cityId]: {
                buildings: buildings,
                upgradeCostMap: upgradeCostMap,
                newBuildingTypes: newBuildingTypes,
                troops: troops
            }
        }));
    }, [buildings, upgradeCostMap, newBuildingTypes, troops, cityId,setCityContextMap]);

    useEffect(() => {
        const handleClickOutside = event => {
            const { target } = event;
            const agGridElement = document.querySelector('.building_view');
            const selectedImageElement = document.querySelector('.selected-image');

            if (!initialClick && !(agGridElement.contains(target) || (selectedImageElement && selectedImageElement.contains(target)))) {
                onClose();
                cityContextSaver()
            }
        };

        document.addEventListener('click', handleClickOutside);
        return () => document.removeEventListener('click', handleClickOutside);
    }, [initialClick]);

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
                        upgradeCostMap={upgradeCostMap}
                        setUpgradeCostMap={setUpgradeCostMap}
                        refreshResources={() => initializeResources(dispatch)}
                    />}
                    {selectedTab === 'newBuildings' &&
                              <NewBuildingGrid
                                buildings={newBuildingTypes}
                                onRowMouseOver={onRowMouseOver}
                                selectedImage={selectedImage}
                                cityId={cityId}
                                updateBuildingsAndTypes={updateBuildingsAndTypes}
                                refreshResources={() => initializeResources(dispatch)}
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
                                        buildingId={selectedClick[0]}
                                        onClose={() => { selectedClick[0] = -1; selectedClick[1] = null}}

                        />}

                </div>
            </WindowUI>
        </div>
    );
};

export default CityManager;
