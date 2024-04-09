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
import TrainingViewer from "../../../UI/TrainingUnits/TrainingViewer";


const ResourceButtonComponent = ({ data, cityId }) => {
    const buttonStyle = "wide-button";

    const collectResourcesHelper = async (cityId, buildingId) => {
        try {
            const response = await collectResources(cityId, buildingId);
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

const TrainButtonComponent = ({ data, setSelectedClick }) => {
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



const UpgradeButtonComponent = ({data, cityId, resources, upgradeCost}) => {

    const upgradeBuildingHelper = async (cityId, buildingId) => {
        try {
            await upgradeBuilding(cityId, buildingId);
        } catch (error) {
            console.error("Failed to upgrade building:", error);
        }
        /*refresh ugradeCostMap*/
    };


    // Set upgrade cost to loading while fetching/if undefined
    const buttonText = upgradeCost[data.id] === null ? 'Loading...' : `Upgrade: ${upgradeCost[data.id].cost} ${upgradeCost[data.id].cost_type}`;
    // Determine button style based upgrade cost
    const buttonStyle = upgradeCost[data.id] && upgradeCost[data.id].can_upgrade ? "wide-button" : "wide-button disabled";

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

    const [trainingMode, setTrainingMode] = useState(false);


    const columns = useMemo(() => [
        { headerName: "Building Type", field: "buildingType" },
        { headerName: "Building Rank", field: "buildingRank" },
        {
            headerName: "Function",
            field: "type",
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
                    onGridReady={params => params.api.sizeColumnsToFit()}
                    onGridSizeChanged={params => params.api.sizeColumnsToFit()}
                />
            </div>
            {!trainingMode && selectedImage && selectedClick[0] === -1 &&
            <div className="right-screen">
                    <div className="building_image">
                        <img src={selectedImage} alt="Building" className="selected-image"/>
                    </div>
                {selectedBuilding && selectedBuilding.type==="Barracks" &&
                    <TrainButtonComponent data={selectedBuilding} setSelectedClick={setSelectedClick}/>
                }
                {selectedBuilding && selectedBuilding.type === "productionBuilding" &&
                    <ResourceButtonComponent data={selectedBuilding} cityId={cityId} resources={resources} upgradeCost={upgradeCostMap[selectedBuilding.id]} />
                }
                {selectedBuilding &&
                    <UpgradeButtonComponent data={selectedBuilding} cityId={cityId} resources={resources} upgradeCost={upgradeCostMap} />
                }
            </div>
            }
        </>
    );
};

export default CurrentBuildingGrid;
