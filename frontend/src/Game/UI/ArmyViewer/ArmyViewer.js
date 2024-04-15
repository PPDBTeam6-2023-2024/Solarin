import React, {useState, useEffect, useContext} from 'react';
import axios from 'axios';
import {TreeView, TreeItem} from '@mui/x-tree-view';
import WindowUI from '../WindowUI/WindowUI';
import {Button} from "@mui/material";
import ArmyViewTroopEntry from "./ArmyViewTroopEntry";
import ArmyViewStatEntry from "./ArmyViewStatEntry";
import {SocketContext} from "../../Context/SocketContext";
import statsJson from "../stats.json";

function ArmyViewer({armyId, onCityCreated, is_owner}) {
    const [troops, setTroops] = useState([]);
    const [stats, setStats] = useState([]);
    const [socket, setSocket] = useContext(SocketContext);

    useEffect(() => {
        const fetchTroops = async () => {
            try {

                const response = await axios.get(`${process.env.REACT_APP_BACKEND_PATH}/army/troops/${armyId}`);
                if (response.status === 200) {
                    setTroops(response.data.troops);

                    setStats(response.data.stats);
                }
            } catch (error) {
                console.error("Failed to fetch troops", error);
            }
        };
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

    let totalCount = troops.reduce((acc, troop) => acc + troop.size, 0);

    return (
        <WindowUI>
            <div className="bg-gray-600 border-4" style={{ padding: "1rem", zIndex: 1, position: 'absolute', top: '10%', left: '10%', width: '15vw', minWidth:"300px", height: 'auto',
                maxHeight: "60vh", "overflow": "scroll"}}>
                <TreeView aria-label="file system navigator">
                    <h1 className="text-2xl my-1">Army {armyId}</h1>

                    {/*Only display the create city button when the user is the owner of that army*/}
                    {is_owner &&
                        <Button variant="contained" onClick={createCity} sx={{margin: "10px"}}>
                        Create City
                        </Button>
                    }

                    <TreeItem className="border-2" sx={{ padding: "0.2rem" }} nodeId={`general-${armyId}`} label={`General`}>
                        {/*THIS PART IS A MOCK FOR AMRY GENERALS*/}
                        <div style={{"width": "50%", "display": "inline-block"}}>
                            <img src={(`/images/general_images/general01.png`)} draggable={false}
                         unselectable="on"/>
                        </div>
                        <div>
                            attack: <span style={{"color": "green"}}>+5%</span>
                        </div>
                        <div>
                            city defense: <span style={{"color": "green"}}>+11%</span>
                        </div>


                    </TreeItem>

                    <TreeItem className="border-2" sx={{ padding: "0.2rem" }} nodeId={`stats-${armyId}`} label={`Stats`}>
                        {statsOutput}
                    </TreeItem>

                    <TreeItem className="border-2" sx={{ padding: "0.2rem" }} nodeId={`total-${armyId}`}
                              label={`${totalCount >= 0 ? totalCount : "?"} Units`}>
                        {troopsOutput}
                    </TreeItem>
                </TreeView>
            </div>
        </WindowUI>
    );
}

export default ArmyViewer;