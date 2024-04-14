import React, {useMemo} from 'react';
import {AgGridReact} from 'ag-grid-react';
import './NewBuildingGrid.css';
import {createBuilding} from '../BuildingManager';

const BuildButtonComponent = ({data, cityId, updateBuildingsAndTypes}) => {
    const handleBuild = (event) => {
        event.stopPropagation();
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


const BuildingGrid = ({buildings, onRowMouseOver, selectedImage, cityId, updateBuildingsAndTypes, resources}) => {
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
                                                            resources={resources}/>
        },
    ], [cityId]);

    const rowData = useMemo(() => buildings.map((building, index) => ({
        name: building.name,
        buildingType: building.type,
        buildingRank: building.required_rank,
        cost: building.costs.map((cost) => {
            return (cost.cost_amount + " " + cost.cost_type)
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
                    <div className="building_image">
                        <img src={selectedImage} alt="Building" className="selected-image"/>
                    </div>
                </div>
            }
        </>
    );
};


export default BuildingGrid;
