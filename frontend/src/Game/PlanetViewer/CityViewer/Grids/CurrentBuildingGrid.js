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
        console.log("collecting resources 1")
        try {
            await collectResources(cityId, buildingId);
        } catch (error) {
            console.error("Failed to collect resources:", error);
        }
    };

    if (data.type === "productionBuilding") {
        return (
            <button className={buttonStyle} onClick={() => collectResourcesHelper(cityId, data.id)}>
                Collect resources
            </button>
        );
    }
    return null;
};

const UpgradeButtonComponent = ({ data, cityId, resources, upgradeCost }) => {

    const upgradeBuildingHelper = async (cityId, buildingId) => {
        try {
            await upgradeBuilding(cityId, buildingId);
            console.log("Building upgraded successfully.");
        } catch (error) {
            console.error("Failed to upgrade building:", error);
        }
        /*refresh ugradeCostMap*/
    };


    // Set upgrade cost to loading while fetching/if undefined
    const buttonText = upgradeCost === null ? 'Loading...' : `Upgrade: ${upgradeCost.cost} ${upgradeCost.cost_type}`;
    // Determine button style based upgrade cost
    const buttonStyle = upgradeCost && upgradeCost.can_upgrade ? "wide-button" : "wide-button disabled";

    return (
        <button className={buttonStyle} onClick={() => upgradeBuildingHelper(cityId, data.id)}>
            {buttonText}
        </button>
    );
};



const CurrentBuildingGrid = ({ buildings, onRowMouseOver, setSelectedClick, selectedClick, selectedImage, cityId, resources, upgradeCostMap }) => {
    const [selectedBuilding, setSelectedBuilding] = useState(null);

    const upgradeButtonRenderer = useMemo(() => {
        return params => <UpgradeButtonComponent data={params.data} cityId={cityId} resources={resources} />;
    }, [cityId, resources]);

    const resourceButtonRenderer = useMemo(() => {
        return params => <ResourceButtonComponent data={params.data} cityId={cityId} />;
    }, [cityId, collectResources]);


    const columns = useMemo(() => [
        { headerName: "Building Type", field: "buildingType" },
        { headerName: "Building Rank", field: "buildingRank" },
        {
            headerName: "",
            field: "id",
            cellRenderer: resourceButtonRenderer,
        },
    ], [cityId]);

    return (
        <>
            <div className="ag-theme-alpine-dark buildings_grid">
                <AgGridReact
                    rowData={buildings.map((building, index) => ({
                        buildingType: building.building_type,
                        buildingRank: building.rank,
                        index: index,
                        id: building.id,
                        type: building.type
                    }))}
                    columnDefs={columns}
                    domLayout='normal'
                    suppressMovableColumns={true}
                    suppressDragLeaveHidesColumns={true}
                    onCellMouseOver={event => {
                        setSelectedBuilding(event.data);
                        onRowMouseOver(event);
                    }}
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
            <div className="right-screen">
                    <div className="building_image">
                        <img src={selectedImage} alt="Building" className="selected-image"/>
                    </div>

                {selectedBuilding &&
                    <UpgradeButtonComponent data={selectedBuilding} cityId={cityId} resources={resources} upgradeCost={upgradeCostMap[selectedBuilding.id]} />
                }
            </div>
                }
        </>
    );
};

export default CurrentBuildingGrid;
