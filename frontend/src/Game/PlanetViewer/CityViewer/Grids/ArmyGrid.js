import React, { useMemo } from "react";
import { AgGridReact } from "ag-grid-react";
import './NewBuildingGrid.css';
import EntityViewer from "../../../UI/CityViewer/EntityViewer";
const ArmyGrid = ({ troops, onRowMouseOver, setSelectedClick, selectedClick, selectedImage }) => {
    const columns = useMemo(() => [
        { headerName: "Troop Type", field: "troopType" },
        { headerName: "Rank", field: "rank" },
        { headerName: "Size", field: "size" },
    ], []);

    const handleLeaveCity = () => {
            console.log("Leaving city..."); // Implement the logic for leaving the city
        };

    return (
        <>
            <div className="ag-theme-alpine-dark buildings_grid">
                <AgGridReact
                    rowData={troops.troops.map((troop, index) => ({
                        troopType: troop.troop_type,
                        rank: troop.rank,
                        size: troop.size,
                        id: troop.id
                    }))}
                    columnDefs={columns}
                    domLayout='normal'
                    suppressMovableColumns={true}
                    suppressDragLeaveHidesColumns={true}
                    onCellMouseOver={onRowMouseOver}
                    onCellClicked={(event) => {
                        setSelectedClick(event.data.index);
                    }}
                    onGridReady={params => params.api.sizeColumnsToFit()}
                    onGridSizeChanged={params => params.api.sizeColumnsToFit()}
                    onRowClicked={params => {
                        if (selectedClick[0] === params.data.index) {
                            setSelectedClick([-1]);
                        } else {
                            setSelectedClick([params.data.index]);
                        }
                    }}
                />
            </div>
            <div className="right-screen">
                {selectedImage &&
                    <div className="building_image">
                        <img src={selectedImage} alt="Troops" className="selected-image"/>
                    </div>
                }
                <button className="wide-button" onClick={handleLeaveCity}>
                    Leave City
                </button>
            </div>
        </>
    );
};

export default ArmyGrid;
