import React, { useMemo, useState } from "react";
import { AgGridReact } from "ag-grid-react";
import './NewBuildingGrid.css';
import { ResourceButtonComponent, TrainButtonComponent, UpgradeButtonComponent } from "./Buttons";

const CurrentBuildingGrid = ({ buildings, onRowMouseOver, setSelectedClick, selectedClick, selectedImage, cityId, setCityInfo, setBuildings, upgradeCostMap, setUpgradeCostMap, refreshResources, resourcesInStorage, setResourcesInStorage }) => {
    const [selectedBuilding, setSelectedBuilding] = useState(null);

    const columns = useMemo(() => [
        { headerName: "Building Type", field: "buildingType" },
        { headerName: "Building Rank", field: "buildingRank" },
        { headerName: "Function", field: "type", autoHeight: true },
    ], [cityId]);

    const rowData = useMemo(() => buildings?.map((building) => ({
        buildingType: building?.building_type,
        buildingRank: building?.rank,
        id: building?.id,
        type: building?.type,
        remaining_update_time: building?.remaining_update_time
    })), [buildings]);

    return (
        <>
            <div className="ag-theme-alpine-dark buildings_grid">
                <AgGridReact
                    rowData={rowData}
                    columnDefs={columns}
                    domLayout='normal'
                    suppressMovableColumns={true}
                    suppressDragLeaveHidesColumns={true}
                    onCellMouseOver={event => {
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
                                    {resourcesInStorage[selectedBuilding.id]?.map((res, index) => (
                                        <tr key={index}>
                                            <td>{res.amount_in_stock} / {res.max_amount}  {res.resource_name}</td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        </div>
                    )}
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
                            />
                        }
                </div>
            }
        </>
    );
};

export default CurrentBuildingGrid;
