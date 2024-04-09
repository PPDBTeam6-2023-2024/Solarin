import React, { useMemo } from "react";
import { AgGridReact } from "ag-grid-react";
import { getImageForBuildingType, collectResources } from "../BuildingManager";
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

    if (data.type === "productionBuilding") {
        return (
            <button className={buttonStyle} onClick={() => collectResourcesHelper(cityId, data.id)}>Collect resources</button>
        );
    }
    return null;
};


const RenderGrid = ({ buildings, onRowMouseOver, setSelectedClick, selectedClick, selectedImage, cityId, updateBuildingsAndTypes, resources }) => {
    const columns = useMemo(() => [
        { headerName: "Building Type", field: "buildingType" },
        { headerName: "Building Rank", field: "buildingRank" },
        {
            headerName: "",
            field: "id",
            cellRenderer: (params) => <ResourceButtonComponent data={params.data} cityId={cityId} />
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
