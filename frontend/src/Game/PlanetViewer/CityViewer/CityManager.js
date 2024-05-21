import React, {useState, useEffect, useCallback, useContext} from 'react';
import 'ag-grid-community/styles/ag-grid.css';
import 'ag-grid-community/styles/ag-theme-alpine.css';
import './CityManager.css';
import {
    getArmyInCity,
    getCityData,
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


const CityManager = ({ cityId, onClose}) => {
    /**
    * This component represents the City Menu, for when you click on 1 of your own cities
    * */

    const dispatch = useDispatch();

    /*List of the buildings inside the city*/
    const [buildings, setBuildings] = useState([]);
    const [resourcesInStorage, setResourcesInStorage] = useState([])

    const [upgradeCostMap, setUpgradeCostMap] = useState([]);
    const [cityUpgradeInfo, setCityUpgradeInfo] = useState([]);
    const [cityInfo, setCityInfo] = useState([])
    const [newBuildingTypes, setNewBuildingTypes] = useState([]);
    const [troops, setTroops] = useState([]); // State for troops

    const [selectedImage, setSelectedImage] = useState(null);

    /* stores selected building*/
    const [selectedClick, setSelectedClick] = useState([-1, ""]);
    const [initialClick, setInitialClick] = useState(true);

    const [selectedTab, setSelectedTab] = useState('currentBuildings');

    const [selectedNewBuilding, setSelectedNewBuilding] = useState("");
    const [selectedType, setSelectedType] = useState("");

    /*
    * Central Timer for updates
    * */
    const [timer, setTimer] = useState(0);

    /*Timer to increment total time passed*/
    useEffect(() => {
        const timerInterval = setInterval(() => {
            setTimer(prevTotalTimePassed => prevTotalTimePassed + 1);
        }, 1000);

        return () => clearInterval(timerInterval);
    }, [timer, setTimer]);

    // load city context (buildings, troops, etc.) either from API or from context map
    const cityContextLoader = (() => {
        /*Load city information*/
        updateBuildingsAndTypes()
        /*Load army information*/
        getArmyInCity(cityId).then(setTroops); // Fetch and set troops
    })

    /*Update the buildings their information*/
    const updateBuildingsAndTypes = async() => {
        /* Refresh buildings and types, by loading its current information from the backend*/

        /*Get information about the current buildings inside the city*/
        await getCityData(cityId).then(cityData => {
                    setBuildings(cityData?.buildings)
                    setCityInfo(cityData?.city)

        });

        /*Get information about the upgrade cost of a building*/
        await getUpgradeCost(cityId).then(buildings => {

            const costMap = buildings?.[0].reduce((acc, building) => {
                acc[building?.id] = building;
                return acc;
            }, {});

            setCityUpgradeInfo(buildings?.[1]);
            setUpgradeCostMap(costMap);


        });

        /*
        * Get information about the buildings we can still build
        * */
        await getNewBuildingTypes(cityId).then(newBuildingTypes => {
                setNewBuildingTypes(newBuildingTypes)
                getResourcesInStorage(cityId).then(resourcesInStorage=> {
                setResourcesInStorage(resourcesInStorage?.overview);
                });

        });
    };

    /*
    * Make sure when we hover over a row entry, that we know what we are hovering over
    * */
    const onRowMouseOver = event => {
        if (selectedTab === 'Army') {
            setSelectedImage(getImageForTroopType(event.data.troop_type))
        } else if (selectedTab === "newBuildings") {
            setSelectedImage(getImageForBuildingType(event.data.name));
            setSelectedNewBuilding(event.data.name);
            setSelectedType(event.data.buildingType);
        } else {
            setSelectedImage(getImageForBuildingType(event.data.buildingType));
        }
    };

    useEffect(() => {
        cityContextLoader()
        setInitialClick(false);
    }, [])

    /*
    * When clicking outside the window, we want to automatically close the window
    * This useEffect will check whether we click outside, and if so close the menu
    * */
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
                    {/*Visualizes the tab options*/}
                    <div className="tabs">
                        <button onClick={() => setSelectedTab('currentBuildings')}>Current Buildings</button>
                        <button onClick={() => setSelectedTab('newBuildings')}>New Buildings</button>
                        <button onClick={() => setSelectedTab('Army')}>Army</button>
                        <button onClick={() => setSelectedTab('City')}>City</button>
                    </div>

                    {/*Displays the Tab of current buildings*/}
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
                        resourcesInStorage={resourcesInStorage}
                        setResourcesInStorage={setResourcesInStorage}
                        setCityInfo={setCityInfo}
                        timer={timer}
                        setTimer={setTimer}
                    />}

                    {/*Displays the Tab to add new buildings*/}
                    {selectedTab === 'newBuildings' &&
                              <NewBuildingGrid
                                buildings={newBuildingTypes}
                                onRowMouseOver={onRowMouseOver}
                                selectedImage={selectedImage}
                                cityId={cityId}
                                updateBuildingsAndTypes={updateBuildingsAndTypes}
                                refreshResources={() => initializeResources(dispatch)}
                                selectedBuilding = {selectedNewBuilding}
                                selectedType = {selectedType}
                              />
                            }

                    {/*Displays the Army Tab*/}
                    {selectedTab === 'Army' && <ArmyGrid
                        onRowMouseOver={onRowMouseOver}
                        troops={troops}
                        selectedImage={selectedImage}
                        refresh={cityContextLoader}
                    />
                    }

                    {/*Displays the City Tab*/}
                    {selectedTab === 'City' &&

                        <CityInfoGrid
                        setBuildings={setBuildings}
                        refreshResources={() => initializeResources(dispatch)}
                        setUpgradeCostMap={setUpgradeCostMap}
                        cityId = {cityId}
                        upgradeCost={cityUpgradeInfo}
                        cityInfo = {cityInfo}
                        setCityInfo = {setCityInfo}
                        timer={timer}
                        setTimer={setTimer}
                        />


                    }


                    {/*Displays a training menu*/}
                    {selectedTab === 'currentBuildings' && selectedClick[0] !== -1 && selectedClick[1] === "Barracks" &&

                        <TrainingViewer key={selectedClick[0]}
                                        buildingId={selectedClick[0]}
                                        onClose={() => { selectedClick[0] = -1; selectedClick[1] = null}}
                                        refreshResources={() => initializeResources(dispatch)}
                                        buildingType={selectedClick[2]}

                        />}

                </div>
            </WindowUI>
        </div>
    );
};

export default CityManager;
