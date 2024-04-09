import React from "react";
import { AgGridReact } from "ag-grid-react";
import { getImageForBuildingType } from "../BuildingManager";

const RenderGrid = ({ buildings, columns, onRowMouseOver, setSelectedClick, selectedClick, selectedImage }) => (
    <>
        <div className="ag-theme-alpine-dark buildings_grid">
            <AgGridReact
                rowData={buildings.map((building, index) => ({
                    buildingType: building.building_type,
                    buildingRank: building.rank,
                    resourceTimer: 'Unknown',
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

export default RenderGrid;
