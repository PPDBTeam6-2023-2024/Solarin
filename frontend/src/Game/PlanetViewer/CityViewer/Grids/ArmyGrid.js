import React, {useContext, useMemo, useState} from "react";
import {AgGridReact} from "ag-grid-react";
import './NewBuildingGrid.css';
import {SocketContext} from "../../../Context/SocketContext";
import {SplitArmy} from "../BuildingManager";

const ArmyGrid = ({troops, onRowMouseOver, setSelectedClick, selectedClick, selectedImage, refresh}) => {

    const [socket, setSocket] = useContext(SocketContext);
    const [gridApi, setGridApi] = useState()
    const [armyId, setArmyId] = useState(troops.army_id)

    /* set column data */
    const columns = useMemo(() => [
        {headerName: "Troop Type", field: "troop_type", autoHeight: true},
        {headerName: "Rank", field: "rank"},
        {headerName: "Size", field: "size"},
    ], []);

    /* set row data */
    const rowData = useMemo(() => troops.troops.map((troop, index) => ({
        troop_type: troop.troop_type,
        rank: troop.rank,
        size: troop.size,
        army_id: troop.army_id
    })), [troops]);

    /* handle troop selection */
    const toggleSelectAllTroops = () => {
    if (gridApi) {
        /* Check if the number of selected troops equals the total number of troops in grid */
        const allSelected = gridApi.getSelectedRows().length === gridApi.getDisplayedRowCount();

        if (allSelected) {
            gridApi.deselectAll(); /* Deselect all troops if they are all selected */
        } else {
            gridApi.selectAll(); /* Select all troops if they are not all selected */
        }
    }
};
    /* handle leaving city with selected troops */
    const handleLeaveCity = async () => {

        const selectedNodes = gridApi.getSelectedNodes();
        const selectedTroops = selectedNodes.map(node => node.data);
        const allSelected = gridApi.getSelectedRows().length === gridApi.getDisplayedRowCount();

        if (!allSelected){
            /* if not all troops are selected, split army and leave city with selected troops */
            setArmyId(await SplitArmy(troops.army_id,selectedTroops))
            if (socket.readyState === WebSocket.OPEN) {
                socket.send(JSON.stringify({ type: "get_armies" }));
            } else {
                console.error("WebSocket is not open.");
            }
        } else{
            /* else have the whole army leave the city */
            setArmyId(troops.army_id)
                    const data_json = {
            type: "leave_city",
            army_id: armyId
            };

            await socket.send(JSON.stringify(data_json));

            /*Makes it so that the access of armies arrives after the websocket arrives, a really short sleep*/
            await new Promise((resolve) => setTimeout(resolve, 50))
        }

        refresh()

    };

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
                    onCellClicked={(event) => { // handle clicks
                        setSelectedClick(event.data.index);
                    }}
                    onGridReady={params => {
                        params.api.sizeColumnsToFit() // handle scaling
                        setGridApi(params.api); // set api for row selection
                    }}
                    onGridSizeChanged={params => params.api.sizeColumnsToFit()} // handle row selection
                    rowSelection="multiple" // handle row selection
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
                            <button className="half-button" onClick={toggleSelectAllTroops}>
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
