import React, {useMemo, useCallback} from 'react';
import {AgGridReact} from 'ag-grid-react';
import './NewBuildingGrid.css';

const BuildButtonComponent = ({data}) => {
    return (
        <button className="build-button" onClick={() => console.log(data)}>Build</button>
    );
};

const BuildingGrid = ({buildings, onRowMouseOver, setSelectedClick, selectedImage}) => {
    const handleBuildClick = useCallback((data) => {
        console.log("Build button clicked for:", data);
    }, []);

    const columns = useMemo(() => [
        {headerName: "Building Type", field: "buildingType"},
        {headerName: "Building Rank", field: "buildingRank"},
        {
            headerName: "Build",
            field: "id", // This 'field' can be named anything as it doesn't bind to rowData here.
            cellRenderer: BuildButtonComponent
        }

    ], [handleBuildClick]);

    return (
        <>
            <div className="ag-theme-alpine-dark buildings_grid">
                <AgGridReact
                    rowData={buildings.map((building, index) => ({
                        buildingType: building.building_type,
                        buildingRank: building.rank,
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
                {selectedImage && <img src={selectedImage} alt="Building" className="selected-image"/>}
            </div>
        </>
    );
};

export default BuildingGrid;
