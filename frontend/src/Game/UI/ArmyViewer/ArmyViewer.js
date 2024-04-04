import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { TreeView, TreeItem } from '@mui/x-tree-view';
import WindowUI from '../WindowUI/WindowUI';

function ArmyViewer({ armyId, onUpdatePosition }) {
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

    let troopsOutput = troops.map((troop, index) => (
        <TreeItem key={index} nodeId={`${index}`} label={`${troop.size}x Troop ${troop.troop_type}`} />
    ));

    /*displays the stats*/
    let statsOutput = Object.entries(stats).map(([key, value], index) => (
        <TreeItem key={index} nodeId={`${index}`} label={`${key}: ${value}`} />
    ));

    let totalCount = troops.reduce((acc, troop) => acc + troop.size, 0);

    return (
        <WindowUI>
            <div className="bg-gray-600 border-4" style={{ padding: "1rem", zIndex: 1, position: 'absolute', top: '10%', left: '10%', width: 'auto', minWidth: '300px', height: 'auto' }}>
                <TreeView aria-label="file system navigator">
                    <h1 className="text-2xl my-1">Army {armyId}</h1>
                    <TreeItem className="border-2" sx={{ padding: "0.25rem" }} nodeId={`stats-${armyId}`} label={`Stats`}>
                        {statsOutput}
                    </TreeItem>

                    <TreeItem className="border-2" sx={{ padding: "0.25rem" }} nodeId={`total-${armyId}`} label={`${totalCount} Units`}>
                        {troopsOutput}
                    </TreeItem>
                </TreeView>
            </div>
        </WindowUI>
    );
}

export default ArmyViewer;
