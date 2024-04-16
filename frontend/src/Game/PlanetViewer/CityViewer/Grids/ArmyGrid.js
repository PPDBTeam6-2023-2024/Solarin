import React, {useContext, useMemo} from "react";
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

    const handleLeaveCity = async () => {

        const data_json = {
            type: "leave_city",
            army_id: troops.army_id
        };

        await socket.send(JSON.stringify(data_json));

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
            <div style={{"width": "27%"}} className="right-screen">
                {selectedImage &&
                    <div className="building_image">
                        <img src={selectedImage} alt="Troops" className="selected-image"/>
                    </div>
                }

                {rowData.length > 0 &&
                    <button className="wide-button" onClick={handleLeaveCity}>
                        Leave City
                    </button>
                }

            </div>
        </>
    );
};

export default ArmyGrid;
