import React, { useMemo, useCallback } from 'react';
import { AgGridReact } from 'ag-grid-react';
import { getImageForBuildingType } from '../BuildingManager';
import './NewBuildingGrid.css';
import { createBuilding} from '../BuildingManager';

const BuildButtonComponent = ({ data, cityId, updateBuildingsAndTypes, resources }) => {
    const handleBuild = () => {
        if (!data.can_build) {
            alert(`Not enough resources to build ${data.name}.`);
            return;
        }

        createBuilding(cityId, data.name)
            .then(() => {
                updateBuildingsAndTypes();
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


const BuildingGrid = ({ buildings, onRowMouseOver, setSelectedClick, selectedImage, cityId, updateBuildingsAndTypes, resources }) => {
    const columns = useMemo(() => [
        { headerName: "Name", field: "name" },
        { headerName: "Building Type", field: "buildingType" },
        { headerName: "Building Rank", field: "buildingRank" },
        { headerName: "Cost Type", field: "costType" },
        { headerName: "Amount", field: "costAmount" },
        {
            headerName: "Build",
            field: "id",
            cellRenderer: (params) => <BuildButtonComponent data={params.data} cityId={cityId} updateBuildingsAndTypes={updateBuildingsAndTypes} resources={resources} />
        },
    ], [cityId]);

    return (
        <>
            <div className="ag-theme-alpine-dark buildings_grid">
                <AgGridReact
                    rowData={buildings.map((building, index) => ({
                        name: building.name,
                        buildingType: building.type,
                        buildingRank: building.required_rank,
                        costType: building.cost_type,
                        costAmount: building.cost_amount,
                        can_build: building.can_build,
                        id: building.id,
                        index: index
                    }))}
                    columnDefs={columns}
                    suppressMovableColumns={true}
                    suppressDragLeaveHidesColumns={true}
                    onCellMouseOver={onRowMouseOver}
                    onCellClicked={(event) => setSelectedClick(event.data.index)}
                    onGridReady={params => params.api.sizeColumnsToFit()}
                    onGridSizeChanged={params => params.api.sizeColumnsToFit()}
                />
            </div>
            <div className="building_image">
                {selectedImage && <img src={selectedImage} alt="Building" className="selected-image" />}
            </div>
        </>
    );
};


export default BuildingGrid;
