import React, {useContext, useMemo, useState, useRef, useEffect} from "react";
import {AgGridReact} from "ag-grid-react";
import './NewBuildingGrid.css';
import {SocketContext} from "../../../Context/SocketContext";
import ResourceCostEntry from "../../../UI/ResourceViewer/ResourceCostEntry";
import {SplitArmy} from "../BuildingManager";
import {getArmyInCity} from "../BuildingManager";
import { sort } from "d3";

const ArmyGrid = ({cityId, onRowMouseOver, selectedImage, refresh}) => {

    const [socket, setSocket] = useContext(SocketContext);
    const [gridApi, setGridApi] = useState()
    const [troops, setTroops] = useState({troops: [], maintenance: []})
    const websocket = useRef(null);

    useEffect(() => {
        websocket.current = new WebSocket(`${process.env.REACT_APP_BACKEND_PATH_WEBSOCKET}/unit/ws/${cityId}`, `${localStorage.getItem('access-token')}`);
        websocket.current.onopen = () => {
            console.log("Websocket connected");
        };

        websocket.current.onmessage = (event) => {
            getArmyInCity(cityId).then(setTroops);
            console.log(troops)
        };
        websocket.current.onclose = () => {
            console.log("Websocket closed");
        };

        return () => {
            websocket.current.close();
        };
    }, [setTroops, cityId]);

    useEffect(() => {
        getArmyInCity(cityId).then(setTroops);
    }, [cityId]);

    /* set column data */
    const columns = useMemo(() => [
        {headerName: "Troop Type", field: "troop_type", autoHeight: true, sortable: true},
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

        /*
        * When no units are selected to leave the city, we will let all troops leave (so in that case, they are also
        * all selected)
        * */
        const allSelected = (gridApi.getSelectedRows().length === gridApi.getDisplayedRowCount())
            || (gridApi.getSelectedRows().length === 0);

        if (!allSelected){
            /* if not all troops are selected, split army and leave city with selected troops */
            await SplitArmy(troops.army_id, selectedTroops)
            if (socket.readyState === WebSocket.OPEN) {
                socket.send(JSON.stringify({ type: "get_armies" }));
            } else {
                console.error("WebSocket is not open.");
            }
        } else{
            /* else have the whole army leave the city */
            const data_json = {
                type: "leave_city",
                army_id: troops.army_id
            };

            await socket.send(JSON.stringify(data_json));

            /*Makes it so that the access of armies arrives after the websocket arrives, a really short sleep*/
            await new Promise((resolve) => setTimeout(resolve, 300))
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
                    onGridReady={params => {
                        params.api.sizeColumnsToFit() // handle scaling
                        setGridApi(params.api); // set api for row selection
                    }}
                    onGridSizeChanged={params => params.api.sizeColumnsToFit()} // handle row selection
                    rowSelection="multiple" // handle row selection
                    rowMultiSelectWithClick={true}
                />

                <div>
                <h2 style={{"textAlign": "center"}}>Army Maintenance Cost /hour</h2>
                <div style={{"display": "flex", "flexDirection": "row", "alignItems": "center",
                    "justifyContent": "center", "overflow": "scroll"}}>
                    {troops.maintenance.map((element, index) => <ResourceCostEntry resource={element[0]}
                                                                                      cost={element[1]}
                                                                                      percentage={false}/>)}
                </div>
                </div>

            </div>
            <div style={{"width": "27%"}} className="right-screen">

                    <div className="building_image">
                        {selectedImage &&
                        <img src={selectedImage} alt="Troops" className="selected-image"/>
                        }
                    </div>

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
