import React, {useState, useEffect, useCallback} from 'react';
import 'ag-grid-community/styles/ag-grid.css';
import 'ag-grid-community/styles/ag-theme-alpine.css';
import './CityManager.css';
import {
    getArmyInCity,
    getBuildings,
    getNewBuildingTypes, getResourcesInStorage,
    getUpgradeCost
} from './BuildingManager';
import NewBuildingGrid from './Grids/NewBuildingGrid';
import WindowUI from '../../UI/WindowUI/WindowUI';
import TrainingViewer from "../../UI/TrainingUnits/TrainingViewer";
import CurrentBuildingGrid from "./Grids/CurrentBuildingGrid"
import ArmyGrid from "./Grids/ArmyGrid";
import {getImageForBuildingType, getImageForTroopType} from "../../UI/CityViewer/EntityViewer";
import {initializeResources} from "../../UI/ResourceViewer/ResourceViewer"
import {useDispatch} from 'react-redux'
import CityInfoGrid from "./Grids/CityInfoGrid";
import {getCityImage} from "./GetCityImage";


const CityManager = ({ cityId, cityRankInput, primaryColor, secondaryColor, onClose}) => {
    /*
    * This component represents the City Menu
    * */

    const dispatch = useDispatch();

    /*List of the buildings inside the city*/
    const [buildings, setBuildings] = useState([]);
    const [resourcesInStorage, setResourcesInStorage] = useState([])
    const [cityUpgradeTimer, setCityUpgradeTimer] = useState([])

    const [upgradeCostMap, setUpgradeCostMap] = useState([]);
    const [cityUpgradeInfo, setCityUpgradeInfo] = useState([]);
    const [cityRank, setCityRank] = useState(cityRankInput);
    const [newBuildingTypes, setNewBuildingTypes] = useState([]);
    const [troops, setTroops] = useState([]); // State for troops

    const [selectedImage, setSelectedImage] = useState(null);

    /* stores selected building*/
    const [selectedClick, setSelectedClick] = useState([-1, ""]);
    const [initialClick, setInitialClick] = useState(true);

    const [selectedTab, setSelectedTab] = useState('currentBuildings');

    // load city context (buildings, troops, etc.) either from API or from context map
    const cityContextLoader = (() => {
        /*Load city information*/
        updateBuildingsAndTypes()
        /*Load army information*/
        getArmyInCity(cityId).then(setTroops); // Fetch and set troops
    })

    /*Update the buildings their information*/
    const updateBuildingsAndTypes = () => {
        /* Refresh buildings and types, by loading its current information from the backend*/

        /*Get information about the current buildings inside the city*/
        getBuildings(cityId).then(buildings => {
                setBuildings(buildings[0])
                setCityUpgradeTimer(buildings[1].remaining_update_time)
            });

        /*Get information about the upgrade cost of a building*/
        getUpgradeCost(cityId).then(buildings => {
                const building_costs = buildings?.[0];
            if (!Array.isArray(building_costs)) {
                console.error("Invalid or no data for building costs:", building_costs);
                return;
            }
            const costMap = building_costs.reduce((acc, building) => {
                acc[building.id] = building;
                return acc;
            }, {});
            setCityUpgradeInfo(buildings?.[1]);
            setUpgradeCostMap(costMap);
        });
        getNewBuildingTypes(cityId).then(newBuildingTypes => {
            setNewBuildingTypes(newBuildingTypes)
        });
        getResourcesInStorage(cityId).then(resourcesInStorage=> {
            setResourcesInStorage(resourcesInStorage.overview);
        }
    )
    };

    const onRowMouseOver = event => {
        if (selectedTab === 'Army') {
            setSelectedImage(getImageForTroopType(event.data.troopType))
        } else if (selectedTab === "newBuildings") {
            setSelectedImage(getImageForBuildingType(event.data.name));
        } else {
            setSelectedImage(getImageForBuildingType(event.data.buildingType));
        }
    };

    useEffect(() => {
        cityContextLoader()
        setInitialClick(false);
    }, [])

    useEffect(() => {
        /*Refresh information on change*/
        const handleClickOutside = event => {
            const {target} = event;
            const agGridElement = document.querySelector('.building_view');
            const selectedImageElement = document.querySelector('.selected-image');

            if (!initialClick && !(agGridElement.contains(target) || (selectedImageElement && selectedImageElement.contains(target)))) {
                onClose();
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
                        <button onClick={() => setSelectedTab('City')}>City</button>
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
                        setBuildings={setBuildings}
                        refreshResources={() => initializeResources(dispatch)}
                        setCityUpgradeInfo={setCityUpgradeInfo}
                        resourcesInStorage={resourcesInStorage}
                        setResourcesInStorage={setResourcesInStorage}
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
                        refresh={cityContextLoader}
                    />
                    }

                    {selectedTab === 'City' && <CityInfoGrid
                        cityUpgradeInfo={cityUpgradeInfo}
                        onRowMouseOver={onRowMouseOver}
                        selectedImage={selectedImage}
                        refresh={cityContextLoader}
                        setBuildings={setBuildings}
                        refreshResources={() => initializeResources(dispatch)}
                        setCityUpgradeInfo={setCityUpgradeInfo}
                        setUpgradeCostMap={setUpgradeCostMap}
                        setSelectedClick={setSelectedClick}
                        selectedClick={selectedClick}
                        CityRank = {cityRank}
                        cityId = {cityId}
                        upgradeCost={cityUpgradeInfo}
                        cityUpgradeTimer={cityUpgradeTimer}
                        setCityUpgradeTimer={setCityUpgradeTimer}
                    />

                    }


                    {/*Displays a training menu*/}
                    {selectedTab === 'currentBuildings' && selectedClick[0] !== -1 && selectedClick[1] === "Barracks" &&

                        <TrainingViewer key={selectedClick[0]}
                                        buildingId={selectedClick[0]}
                                        onClose={() => { selectedClick[0] = -1; selectedClick[1] = null}}
                                        refreshResources={() => initializeResources(dispatch)}

                        />}

                </div>
            </WindowUI>
        </div>
    );
};

export default CityManager;
