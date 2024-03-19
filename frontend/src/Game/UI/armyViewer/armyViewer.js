import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { TreeView, TreeItem } from '@mui/x-tree-view';
import Draggable from 'react-draggable';

function ArmyViewer(props) {
    const [troops, setTroops] = useState([]);

    useEffect(() => {
        const fetchTroops = async () => {
            try {
                const response = await axios.get(`${process.env.REACT_APP_BACKEND_PATH}/army/troops?armyid=${props.armyId}`);
                if (response.status === 200 && Array.isArray(response.data)) {
                    setTroops(response.data);
                }
            } catch (error) {
                console.error("Failed to fetch troops", error);
            }
        };

        fetchTroops();
    }, [props.armyId]);

    let troopsOutput = troops.map((troop, index) => {
        return (
            <TreeItem
                key={index}
                nodeId={`${index}`}
                label={`${troop.size}x Troop ${troop.troop_type}`}
            />
        );
    });

    let totalCount = troops.reduce((acc, troop) => acc + troop.size, 0);

    return (
        <Draggable>
            <TreeView
                className="bg-gray-600 fixed border-4"
                aria-label="file system navigator"
                sx={{zIndex: 1, flexGrow: 1, overflowY: 'auto', padding: "1rem"}}
            >
                <h1 className="text-2xl my-1">Army {props.armyId}</h1>
                <TreeItem className="border-2" sx={{padding: "0.25rem"}} nodeId={`stats-${props.armyId}`} label={`stats`}></TreeItem>
                <TreeItem className="border-2" sx={{padding: "0.25rem"}} nodeId={`total-${props.armyId}`} label={`${totalCount} troops`}>
                    {troopsOutput}
                </TreeItem>
            </TreeView>
        </Draggable>
    );
}

export default ArmyViewer;
