import React, { useMemo, useState, useEffect  } from "react";
import { AgGridReact } from "ag-grid-react";
import {
    getImageForBuildingType,
    collectResources,
    upgradeBuilding,
    getUpgradeCost,
    getResources
} from "../BuildingManager";
import './NewBuildingGrid.css';

const ResourceButtonComponent = ({ data, cityId }) => {
    const buttonStyle = "build-button";

    const collectResourcesHelper = async (cityId, buildingId) => {
        try {
            await collectResources(cityId, buildingId);
            console.log("Resources collected successfully.");
        } catch (error) {
            console.error("Failed to collect resources:", error);
        }
    };

    getResources()

    if (data.type === "productionBuilding") {
        return (
            <button className={buttonStyle} onClick={() => collectResourcesHelper(cityId, data.id)}>Collect resources</button>
        );
    }
    return null;
};

const UpgradeButtonComponent = ({ data, cityId, resources }) => {
    const [upgradeCost, setUpgradeCost] = useState(null);

    useEffect(() => {
        const fetchUpgradeCost = async () => {
            const cost = await getUpgradeCost(data.id);
            setUpgradeCost(cost);
        };

        fetchUpgradeCost();
    }, [data.id]);

    const upgradeBuildingHelper = async (cityId, buildingId) => {
        try {
            await upgradeBuilding(cityId, buildingId);
            console.log("Building upgraded successfully.");
        } catch (error) {
            console.error("Failed to upgrade building:", error);
        }
    };


    // Set upgrade cost to loading while fetching/if undefined
    const buttonText = upgradeCost === null ? 'Loading...' : `${upgradeCost.cost} ${upgradeCost.cost_type}`;
    // Determine button style based upgrade cost
    const buttonStyle = upgradeCost && upgradeCost.can_upgrade ? "build-button" : "build-button disabled";

    return (
        <button className={buttonStyle} onClick={() => upgradeBuildingHelper(cityId, data.id)} disabled={!(upgradeCost && resources >= upgradeCost.cost)}>
            {buttonText}
        </button>
    );
};


const RenderGrid = ({ buildings, onRowMouseOver, setSelectedClick, selectedClick, selectedImage, cityId, resources }) => {
    const upgradeButtonRenderer = useMemo(() => {
        return params => <UpgradeButtonComponent data={params.data} cityId={cityId} resources={resources} />;
    }, [cityId, resources]);  // Add resources as a dependency

    const resourceButtonRenderer = useMemo(() => {
        return params => <ResourceButtonComponent data={params.data} cityId={cityId} />;
    }, [cityId]);


    const columns = useMemo(() => [
        { headerName: "Building Type", field: "buildingType" },
        { headerName: "Building Rank", field: "buildingRank" },
        {
            headerName: "",
            field: "id",
            cellRenderer: resourceButtonRenderer,
        },{
            headerName: "Upgrade",
            field: "id",
            cellRenderer: upgradeButtonRenderer,
        },
    ], [cityId]);

    return (
        <>
            <div className="ag-theme-alpine-dark buildings_grid">
                <AgGridReact
                    rowData={buildings.map((building, index) => ({
                        buildingType: building.building_type,
                        buildingRank: building.rank,
                        image: getImageForBuildingType(building.building_type),
                        index: index,
                        id: building.id,
                        type: building.type
                    }))}
                    columnDefs={columns}
                    domLayout='normal'
                    suppressMovableColumns={true}
                    suppressDragLeaveHidesColumns={true}
                    onCellMouseOver={onRowMouseOver}
                    onCellClicked={(event) => { setSelectedClick(event.data.index); }}
                    onGridReady={params => params.api.sizeColumnsToFit()}
                    onGridSizeChanged={params => params.api.sizeColumnsToFit()}
                    onRowClicked={params => {
                        if (selectedClick[0] === params.data.id && selectedClick[1] === params.data.type) {
                            setSelectedClick([-1, ""]);
                        } else {
                            setSelectedClick([params.data.id, params.data.type]);
                        }
                    }}
                />
            </div>

            {selectedImage && selectedClick[0] === -1 &&
                <div className="building_image">
                    <img src={selectedImage} alt="Building" className="selected-image" />
                </div>
            }
        </>
    );
};

export default RenderGrid;
