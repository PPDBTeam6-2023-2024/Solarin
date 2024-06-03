import React, {useEffect, useMemo, useState} from 'react';
import {AgGridReact} from 'ag-grid-react';
import './NewBuildingGrid.css';
import {createBuilding} from '../BuildingManager';
import axios from "axios";
import statsJson from "../../../UI/stats.json";
import resourceJson from "../../../UI/ResourceViewer/resources.json";

const BuildButtonComponent = ({data, cityId, updateBuildingsAndTypes, refreshResources}) => {
    const handleBuild = (event) => {
        event.stopPropagation();
        if (!data.can_build) {
            alert(`Not enough resources to build ${data.name}.`);
            return;
        }

        createBuilding(cityId, data.name)
            .then(() => {
                updateBuildingsAndTypes();
                refreshResources()
            })
            .catch((error) => {
                console.error('Error creating building:', error);
            });
    };

    // Apply conditional styling
    const buttonStyle = data.can_build ? "build-button" : "build-button disabled";

    return (
        <button className={buttonStyle} onClick={handleBuild} disabled={!data.can_build}>Build</button>
    );
};


const BuildingGrid = ({
                          buildings,
                          onRowMouseOver,
                          selectedImage,
                          cityId,
                          updateBuildingsAndTypes,
                          refreshResources,
                          selectedBuilding,
                          selectedType
                      }) => {

    const [prodStats, setProdStats] = useState([])
    const [baseStats, setBaseStats] = useState([])

    useEffect(() => {

        const getProdStats = async () => {
            // get the base production stats of all the production buildings
            const response = await axios.get(`${process.env.REACT_APP_BACKEND_PATH}/building/get_production/`);
            setProdStats(response.data);
        }
        const getCombatStats = async () => {
            // get the base stats of the towers/walls
            const response = await axios.get(`${process.env.REACT_APP_BACKEND_PATH}/building/get_stats/`);
            setBaseStats(response.data);
        }
        getCombatStats();
        getProdStats();
    }, []);

    const columns = useMemo(() => [
        {headerName: "Name", field: "name"},
        {headerName: "Type", field: "buildingType", autoHeight: true},
        {headerName: "Rank", field: "buildingRank"},
        {headerName: "Cost", field: "cost"},
        {
            headerName: "Build",
            field: "id",
            cellRenderer: (params) => <BuildButtonComponent data={params.data} cityId={cityId}
                                                            updateBuildingsAndTypes={updateBuildingsAndTypes}
                                                            refreshResources={refreshResources}/>
        },
    ], [cityId]);

    const rowData = useMemo(() => buildings.map((building, index) => ({
        name: building.name,
        buildingType: building.type,
        buildingRank: building.required_rank,
        cost: building.costs.map((cost) => {
            return `${cost.cost_amount} ${cost.cost_type}`
        }),
        can_build: building.can_build,
        id: building.id,
        index: index
    })), [buildings]);
    return (
        <>
            <div className="ag-theme-alpine-dark buildings_grid">
                <AgGridReact
                    rowData={rowData}
                    columnDefs={columns}
                    suppressMovableColumns={true}
                    suppressDragLeaveHidesColumns={true}
                    onCellMouseOver={onRowMouseOver}
                    onGridReady={params => params.api.sizeColumnsToFit()}
                    onGridSizeChanged={params => params.api.sizeColumnsToFit()}
                />
            </div>
            {selectedImage &&
                <div className="right-screen">
                    <div style={{"height": "30%"}}>
                        {selectedType && selectedType === "tower" &&
                        <div className={"building-stats"}>
                            <img src={`/images/stats_icons/${statsJson.attack.icon}`} alt={"attack"}/>
                            <div>{baseStats[selectedBuilding]}</div>
                        </div>
                        }
                        {selectedType && selectedType === "wall" &&
                            <div className={"building-stats"}>
                                <img src={`/images/stats_icons/${statsJson.defense.icon}`} alt={"defense"}/>
                                <div>{baseStats[selectedBuilding]}</div>
                            </div>
                        }

                        {selectedType && selectedType === "productionBuilding" && selectedBuilding !== "" &&
                            <>
                                <div>Produces:</div>
                                <div className={"building-stats"}>
                                    {prodStats[selectedBuilding].map(resource => (
                                        <div key={selectedBuilding} className="resource-entry">
                                            <img src={`/images/resources/${resourceJson[resource.resource].icon}`}
                                                 alt={resource.resource}/>
                                            <div>{resource.amount}</div>
                                        </div>
                                    ))}
                                </div>
                            </>
                        }
                    </div>

                    <div style={{"height": "60%"}}>
                        <div className="building_image">
                        <img src={selectedImage} alt="Building" className="selected-image"/>
                        </div>
                    </div>

                </div>
            }
        </>
    )
        ;
};


export default BuildingGrid;
