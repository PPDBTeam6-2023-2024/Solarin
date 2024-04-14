import React, {useMemo, useState} from "react";
import {AgGridReact} from "ag-grid-react";
import {
    collectResources, getUpgradeCost,
    upgradeBuilding
} from "../BuildingManager";
import './NewBuildingGrid.css';


const ResourceButtonComponent = ({data, cityId, refreshResources}) => {
    const buttonStyle = "wide-button";

    const collectResourcesHelper = async (cityId, buildingId) => {
        try {
            await collectResources(cityId, buildingId);
            refreshResources();
        } catch (error) {
            console.error("Failed to collect resources:", error);
        }
    };
    if (data.type === "productionBuilding") {
        return (
            <button className={buttonStyle} onClick={() => collectResourcesHelper(cityId, data.id)}>
                Collect Resources
            </button>
        );
    }
    return null;
};

const TrainButtonComponent = ({data, setSelectedClick}) => {
    return (
        <button
            className="wide-button"
            onClick={(event) => {
                event.stopPropagation();
                setSelectedClick([data.id, "Barracks"]);
            }}
        >
            Train Troops
        </button>
    );
};


const UpgradeButtonComponent = ({data, cityId, setUpgradeCostMap, upgradeCost, refreshResources}) => {
    const upgradeBuildingHelper = async (cityId, buildingId) => {
        try {
            const upgradeSuccessful = await upgradeBuilding(cityId, buildingId);
            if (upgradeSuccessful.confirmed === true) {
                await getUpgradeCost(cityId).then(buildings => {
                    const costMap = buildings.reduce((acc, building) => {
                        acc[building.id] = building;
                        return acc;
                    }, {});
                    setUpgradeCostMap(costMap);
                    refreshResources();
                });
            }
        } catch (error) {
            console.error("Failed to upgrade building:", error);
        }
    };

    // Check if upgrade cost data is available, and if not, show "..loading"
    const costData = upgradeCost[data.id];
    const isCostAvailable = costData && costData.costs.length > 0;

    // Adjust buttonText based on availability of cost data
    const buttonText = isCostAvailable
        ? `Upgrade: ${costData.costs.map((cost) => {
            return `${cost[1]} ${cost[0]}`
        })}`
        : 'Loading...';

    // Determine button style based on availability of upgrade cost
    const buttonStyle = isCostAvailable && costData.can_upgrade
        ? "wide-button"
        : "wide-button disabled";

    return (
        <button className={buttonStyle} onClick={() => upgradeBuildingHelper(cityId, data.id)}
                disabled={!isCostAvailable || !costData.can_upgrade}>
            {buttonText}
        </button>
    );
};


const CurrentBuildingGrid = ({
                                 buildings,
                                 onRowMouseOver,
                                 setSelectedClick,
                                 selectedClick,
                                 selectedImage,
                                 cityId,
                                 resources,
                                 upgradeCostMap,
                                 setUpgradeCostMap,
                                 refreshResources
                             }) => {
    const [selectedBuilding, setSelectedBuilding] = useState(null);


    const columns = useMemo(() => [
        {headerName: "Building Type", field: "buildingType"},
        {headerName: "Building Rank", field: "buildingRank"},
        {headerName: "Function", field: "type", autoHeight: true},

    ], [cityId]);
    const rowData = useMemo(() => buildings.map((building, index) => ({
        buildingType: building.building_type,
        buildingRank: building.rank,
        index: index,
        id: building.id,
        type: building.type
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
                    <div className="building_image">
                        <img src={selectedImage} alt="Building" className="selected-image"/>
                    </div>
                    {selectedBuilding && selectedBuilding.type === "Barracks" &&
                        <TrainButtonComponent data={selectedBuilding} setSelectedClick={setSelectedClick}/>
                    }
                    {selectedBuilding && selectedBuilding.type === "productionBuilding" &&
                        <ResourceButtonComponent data={selectedBuilding} cityId={cityId}
                                                 refreshResources={refreshResources}/>
                    }
                    {selectedBuilding &&
                        <UpgradeButtonComponent data={selectedBuilding} cityId={cityId} upgradeCost={upgradeCostMap}
                                                setUpgradeCostMap={setUpgradeCostMap}
                                                refreshResources={refreshResources}/>
                    }
                </div>
            }
        </>
    );
};

export default CurrentBuildingGrid;
