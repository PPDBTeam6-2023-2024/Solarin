import React, {useEffect, useMemo, useState} from "react";
import {AgGridReact} from "ag-grid-react";
import './NewBuildingGrid.css';
import { ResourceButtonComponent, TrainButtonComponent, UpgradeButtonComponent } from "./Buttons";
import axios from "axios";
import statsJson from "../../../UI/stats.json"
import {getProductionBuildingRates} from "../BuildingManager";

const CurrentBuildingGrid = ({ buildings, onRowMouseOver, setSelectedClick, selectedClick, selectedImage, cityId, setCityInfo, setBuildings, upgradeCostMap, setUpgradeCostMap, refreshResources, resourcesInStorage, setResourcesInStorage, timer, setTimer }) => {
    /**
     * Visualization of the grid of the current buildings the city currently has
     * */
    const [selectedBuilding, setSelectedBuilding] = useState(null);
    const [baseStats, setBaseStats] = useState(null)
    const [selectedBuildingStat, setSelectedBuildingStat] = useState(0)
    const [rates, setRates] = useState({})

    const columns = useMemo(() => [
        { headerName: "Building Type", field: "buildingType"},
        { headerName: "Building Rank", field: "buildingRank" },
        { headerName: "Function", field: "type", autoHeight: true },
    ], [cityId]);

    useEffect(() => {
    if (selectedBuilding) {
        const updatedBuilding = buildings.find(b => b.id === selectedBuilding.id);
        if (updatedBuilding) {
            setSelectedBuilding(updatedBuilding);
        } else {
            setSelectedBuilding(null);
        }
    }
    }, [buildings, selectedBuilding]);


    useEffect(() => {
        /*Get production rate for a building*/
        const fetchRates = async() => {
            setRates(await getProductionBuildingRates(cityId))
        }
        fetchRates()
        }, [])

    /*Get stats of a building in case we have a tower or a wall*/
    useEffect(() => {

        const getStats = async () => {
            // get the base stats of the towers/walls
            const response = await axios.get(`${process.env.REACT_APP_BACKEND_PATH}/building/get_stats/`);
            setBaseStats(response.data);
        }
        getStats()
    }, []);

    useEffect(() => {
        if (baseStats != null && selectedBuilding != null) {
            const base = baseStats[selectedBuilding.building_type];
            const rank = selectedBuilding.rank;
            setSelectedBuildingStat(base * Math.floor(1.4 ** rank));
        }
    }, [baseStats, selectedBuilding]);  // also depend on baseStats in case this useEffect is executed before the getStats

    const rowData = useMemo( () => buildings.map( (building) => ({
        buildingType: building?.building_type,
        buildingRank: building?.rank,
        id: building?.id,
        type: building?.type,
        remaining_update_time: building?.remaining_update_time})), [buildings]);
  
    return (
        <>
            <div className="ag-theme-alpine-dark buildings_grid">
                <AgGridReact
                    rowData={rowData}
                    columnDefs={columns}
                    domLayout='normal'
                    suppressMovableColumns={true}
                    suppressDragLeaveHidesColumns={true}
                    onCellMouseOver={async (event)=> {
                        setSelectedBuilding(event.data);
                        onRowMouseOver(event);
                    }}

                    onGridReady={params => params.api.sizeColumnsToFit()}
                    onGridSizeChanged={params => params.api.sizeColumnsToFit()}
                />
            </div>
            {selectedImage && selectedClick[0] === -1 &&
                <div className="right-screen">
                    {selectedBuilding && selectedBuilding.type === "productionBuilding" && (
                        <div>
                            <table>
                                <thead>
                                    <tr>
                                        <th>Amount in Stock</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {/*Display the production rates*/}
                                    {rates[selectedBuilding.id]?.map((res, index) => (
                                        <tr key={index}>
                                            <td>{res.amount_in_stock} / {res.max_amount}  {res.resource_name} {rates[selectedBuilding.id][res.resource_name] && <small>{String(rates[selectedBuilding.id][res.resource_name])}/hr</small>}</td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        </div>
                    )}
                    {selectedBuilding && selectedBuilding.type === "tower" &&
                        <div className={"building-stats"}>
                            <img src={`/images/stats_icons/${statsJson.attack.icon}`} alt={"attack"}/>
                            <div>{selectedBuildingStat}</div>
                        </div>
                    }
                    {selectedBuilding && selectedBuilding.type === "wall" &&
                        <div className={"building-stats"}>
                            <img src={`/images/stats_icons/${statsJson.defense.icon}`} alt={"defense"}/>
                            <div>{selectedBuildingStat}</div>
                        </div>
                    }
                    <div className="building_image">
                        <img src={selectedImage} alt="Building" className="selected-image"/>
                    </div>
                        {selectedBuilding && selectedBuilding.type==="Barracks" &&
                            <TrainButtonComponent data={selectedBuilding} setSelectedClick={setSelectedClick}/>
                        }
                        {selectedBuilding && selectedBuilding.type === "productionBuilding" &&
                            <ResourceButtonComponent data={selectedBuilding} cityId={cityId}
                                                     refreshResources={refreshResources}
                                                     resourcesInStorage={resourcesInStorage}
                                                     setResourcesInStorage={setResourcesInStorage}/>
                        }
                        {selectedBuilding &&
                            <UpgradeButtonComponent data={selectedBuilding}
                                                    cityId={cityId}
                                                    upgradeCost={upgradeCostMap}
                                                    setUpgradeCostMap={setUpgradeCostMap}
                                                    refreshResources={refreshResources}
                                                    setBuildings={setBuildings}
                                                    setCityInfo = {setCityInfo}
                                                    cityUpgradeBool={false}
                                                    totalTimePassed={timer}
                                                    setTotalTimePassed={setTimer}
                            />
                        }
                </div>
            }
        </>
    );
};

export default CurrentBuildingGrid;
