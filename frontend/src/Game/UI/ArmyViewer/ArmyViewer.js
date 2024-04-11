import React, {useState, useEffect, useContext} from 'react';
import axios from 'axios';
import { TreeView, TreeItem } from '@mui/x-tree-view';
import WindowUI from '../WindowUI/WindowUI';
import {Button} from "@mui/material";
import {PlanetIdContext} from "../../Context/PlanetIdContext";
import ArmyViewTroopEntry from "./ArmyViewTroopEntry";

function ArmyViewer({armyId, onCityCreated}) {
    const [troops, setTroops] = useState([]);
    const [stats, setStats] = useState([]);

    useEffect(() => {
        const fetchTroops = async () => {
            try {
                const response = await axios.get(`${process.env.REACT_APP_BACKEND_PATH}/army/troops?armyid=${armyId}`);
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
        try {
        const cityData = {
            army_id: armyId
        };
            await axios.post(`${process.env.REACT_APP_BACKEND_PATH}/cityManager/create_city`, cityData);
            onCityCreated()
        } catch (error) {
            console.error("Failed creating city", error);
        }
    };

    let troopsOutput = troops.map((troop, index) => (
        <>
            <ArmyViewTroopEntry key={index} troop_type={troop.troop_type} troop_size={troop.size} rank={troop.rank}/>
        </>

    ));

    /*displays the stats*/
    let statsOutput = Object.entries(stats).map(([key, value], index) => (
        <TreeItem key={index} nodeId={`${index}`} label={`${key}: ${value}`} />
    ));

    let totalCount = troops.reduce((acc, troop) => acc + troop.size, 0);

    return (
        <WindowUI>
            <div className="bg-gray-600 border-4" style={{ padding: "1rem", zIndex: 1, position: 'absolute', top: '10%', left: '10%', width: '15vw', minWidth:"300px", height: 'auto' }}>
                <TreeView aria-label="file system navigator">
                    <h1 className="text-2xl my-1">Army {armyId}</h1>
                    <Button variant="contained" onClick={createCity} sx={{margin: "10px"}}>
                        Create City
                    </Button>
                    <TreeItem className="border-2" sx={{ padding: "0.2rem" }} nodeId={`stats-${armyId}`} label={`Stats`}>
                        {statsOutput}
                    </TreeItem>

                    <TreeItem className="border-2" sx={{ padding: "0.2rem" }} nodeId={`total-${armyId}`} label={`${totalCount} Units`}>
                        {troopsOutput}
                    </TreeItem>
                </TreeView>
            </div>
        </WindowUI>
    );
}

export default ArmyViewer;