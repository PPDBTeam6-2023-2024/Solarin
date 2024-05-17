import React, {useContext, useMemo, useState} from "react";
import {AgGridReact} from "ag-grid-react";
import './NewBuildingGrid.css';
import {SocketContext} from "../../../Context/SocketContext";

const ArmyGrid = ({troops, onRowMouseOver, setSelectedClick, selectedClick, selectedImage, refresh}) => {
    const columns = useMemo(() => [
        {headerName: "Troop Type", field: "troopType", autoHeight: true},
        {headerName: "Rank", field: "rank"},
        {headerName: "Size", field: "size"},
    ], []);

    const rowData = useMemo(() => troops.troops.map((troop, index) => ({
        troopType: troop.troop_type,
        rank: troop.rank,
        size: troop.size,
        id: troop.id
    })), [troops]);

    const [socket, setSocket] = useContext(SocketContext);
    const [gridApi, setGridApi] = useState()

    const selectAllRows = () => {
    if (gridApi) {
        // Check if the number of selected rows equals the total number of rows
        const allSelected = gridApi.getSelectedRows().length === gridApi.getDisplayedRowCount();

        if (allSelected) {
            gridApi.deselectAll(); // Deselect all rows if they are all selected
        } else {
            gridApi.selectAll(); // Select all rows if they are not all selected
        }
    }
};
    const handleLeaveCity = async () => {

        const selectedNodes = gridApi.getSelectedNodes();
        const selectedData = selectedNodes.map(node => node.data);

        const allSelected = gridApi.getSelectedRows().length === gridApi.getDisplayedRowCount();
        if (allSelected){
            const data_json = {
            type: "leave_city",
            army_id: troops.army_id
            };

            await socket.send(JSON.stringify(data_json));

            /*Makes it so that the access of armies arrives after the websocket arrives, a really short sleep*/
            await new Promise((resolve) => setTimeout(resolve, 50))
            refresh()
        }

    };
    // const handleLeaveCity = async () => {

    //
    //     setselectTroopsMode(true)
    //
    //     const data_json = {
    //         type: "leave_city",
    //         army_id: troops.army_id
    //     };
    //
    //     await socket.send(JSON.stringify(data_json));
    //
    //     /*Makes it so that the access of armies arrives after the websocket arrives, a really short sleep*/
    //     await new Promise((resolve) => setTimeout(resolve, 50))
    //     refresh()
    // };

    return (
        <>
            <div className="ag-theme-alpine-dark buildings_grid">
                <AgGridReact
                    rowData={rowData}
                    columnDefs={columns}
                    domLayout='normal'
                    suppressMovableColumns={true}
                    suppressDragLeaveHidesColumns={true}
                    onCellMouseOver={onRowMouseOver}
                    onCellClicked={(event) => {
                        setSelectedClick(event.data.index);
                    }}
                    onGridReady={params => {
                        params.api.sizeColumnsToFit()
                        setGridApi(params.api);
                    }}
                    onGridSizeChanged={params => params.api.sizeColumnsToFit()}
                    rowSelection="multiple"
                    rowMultiSelectWithClick={true}
                />
            </div>
            <div style={{"width": "27%"}} className="right-screen">
                {selectedImage &&
                    <div className="building_image">
                        <img src={selectedImage} alt="Troops" className="selected-image"/>
                    </div>
                }
                {rowData.length > 0 &&
                    <div className="container">
                        <div className="instruction-text">Click on troops to select</div>
                        <div className="button-container">
                            <button className="half-button" onClick={selectAllRows}>
                                Select All
                            </button>
                            <button className="half-button" onClick={handleLeaveCity}>
                                Leave City
                            </button>
                        </div>
                    </div>

                }

            </div>
        </>
    )
};

export default ArmyGrid;
