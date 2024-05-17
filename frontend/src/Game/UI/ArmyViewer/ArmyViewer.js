import React, {useState, useEffect, useContext} from 'react';
import axios from 'axios';
import {TreeView, TreeItem} from '@mui/x-tree-view';
import WindowUI from '../WindowUI/WindowUI';
import {Button} from "@mui/material";
import ArmyViewTroopEntry from "./ArmyViewTroopEntry";
import ArmyViewStatEntry from "./ArmyViewStatEntry";
import {SocketContext} from "../../Context/SocketContext";
import GeneralView from "./GeneralView";
import statsJson from "../stats.json";
import ResourceCostEntry from "../ResourceViewer/ResourceCostEntry";

function ArmyViewer({armyId, onCityCreated, is_owner, in_space}) {
    const [troops, setTroops] = useState([]);
    const [stats, setStats] = useState([]);
    const [general, setGeneral] = useState({});
    const [socket, setSocket] = useContext(SocketContext);
    const [maintenance, setMaintenance] = useState([]);

    const fetchTroops = async () => {
        try {

            const response = await axios.get(`${process.env.REACT_APP_BACKEND_PATH}/army/troops/${armyId}`);
            if (response.status === 200) {
                setTroops(response.data.troops);

                setStats(response.data.stats);

                setGeneral(response.data.general);
                setMaintenance(response.data.maintenance)
            }
        } catch (error) {
            console.error("Failed to fetch troops", error);
        }
    };

    useEffect(() => {
        /*Update information like troop stats, general, ....*/
        fetchTroops();
    }, [armyId]);



    const createCity = async () => {
        /*Send a websocket message to create a city*/
        const data_json  = {
                        type: "create_city",
                        army_id: armyId
                };

        await socket.send(JSON.stringify(data_json));

    };

    // for every troop type in the army create a TroopEntry
    let troopsOutput = troops.map((troop, index) => (
        <>
            <ArmyViewTroopEntry key={index} troop_type={troop.troop_type} troop_size={troop.size} rank={troop.rank}/>
        </>

    ));

    /*displays the stats*/
    let statsOutput = Object.entries(stats).map(([key, value], index) => (
        <>
            <ArmyViewStatEntry key={index} stat_name={key} stat_value={value}/>
        </>

    ));

    /*Display the maintenance cost of the army*/
    let maintenanceOutput = maintenance.map((element, index) => (
        <>
            <ResourceCostEntry key={element[0]} resource={element[0]} cost={element[1]} percentage={false}/>
        </>

    ));

    let totalCount = troops.reduce((acc, troop) => acc + troop.size, 0);

    return (
        <WindowUI>
            <div className="bg-gray-600 border-4" style={{ padding: "1rem", zIndex: 1, position: 'absolute', top: '10%', left: '10%', width: '15vw', minWidth:"300px", height: 'auto',
                maxHeight: "60vh", "overflow": "scroll"}}>
                <TreeView aria-label="file system navigator">

                    <h1 className="text-2xl my-1">Army {armyId}</h1>

                    {/*Only display the create city button when the user is the owner of that army*/}
                    {is_owner && !in_space &&
                        <Button variant="contained" onClick={createCity} sx={{margin: "10px"}}>
                        Create City
                        </Button>
                    }

                    {is_owner &&
                    <TreeItem className="border-2" sx={{ padding: "0.2rem" }} nodeId={`general-${armyId}`} label={`General`}>
                        <GeneralView armyId={armyId} generalInfo={general} onChangeGeneral={fetchTroops}/>

                    </TreeItem>
                    }

                    <TreeItem className="border-2" sx={{ padding: "0.2rem" }} nodeId={`stats-${armyId}`} label={`Stats`}>
                        {statsOutput}
                    </TreeItem>

                    <TreeItem className="border-2" sx={{ padding: "0.2rem" }} nodeId={`total-${armyId}`}
                              label={`${totalCount >= 0 ? totalCount : "?"} Units`}>
                        {troopsOutput}
                    </TreeItem>

                    <TreeItem className="border-2" sx={{ padding: "0.2rem" }} nodeId={`maintenance-${armyId}`}
                              label={`Maintenance Cost /hour`}>
                        {maintenanceOutput}

                    </TreeItem>
                </TreeView>
            </div>
        </WindowUI>
    );
}

export default ArmyViewer;