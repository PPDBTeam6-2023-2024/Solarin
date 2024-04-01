import React, {useState, useEffect} from 'react';
import axios from 'axios';
import { TreeView, TreeItem } from '@mui/x-tree-view';
import WindowUI from '../WindowUI/WindowUI';
import {Button} from "@mui/material";

function ArmyViewer({armyId, onUpdatePosition, onCityCreated}) {
    const [troops, setTroops] = useState([]);
    const [showInputFields, setShowInputFields] = useState(false);
    const [coordinates, setCoordinates] = useState({x: '', y: ''});

    useEffect(() => {
        const fetchTroops = async () => {
            try {
                const response = await axios.get(`${process.env.REACT_APP_BACKEND_PATH}/army/troops?armyid=${armyId}`);
                if (response.status === 200 && Array.isArray(response.data)) {
                    setTroops(response.data);
                }
            } catch (error) {
                console.error("Failed to fetch troops", error);
            }
        };
        fetchTroops();
    }, [armyId]);

    const handleInputChange = (e) => {
        const {name, value} = e.target;
        setCoordinates(prev => ({...prev, [name]: value}));
    };

    const createCity = async () => {
        try {
            // get the planetID and coordinates from the army using the armyID
            const army = await axios.get(`${process.env.REACT_APP_BACKEND_PATH}/army/getarmy?army_id=${armyId}`)
        const armyData = army.data;
        let planet_id = armyData.planet_id
        const cityData = {
            x: armyData.x,
            y: armyData.y
        };
            await axios.post(`${process.env.REACT_APP_BACKEND_PATH}/cityManager/create_city?planet_id=${planet_id}`, cityData);
            onCityCreated()
        } catch (error) {
            console.error("Failed creating city", error);
        }
    };

    const submitCoordinates = async () => {
        const {x, y} = coordinates;
        try {
            const newX = parseFloat(x);
            const newY = parseFloat(y);
            await axios.post(`${process.env.REACT_APP_BACKEND_PATH}/army/armies/${armyId}/update-coordinates`, { x: newX, y: newY });
            console.log("Army moved successfully");
            onUpdatePosition(armyId, newX, newY); // Use the callback to update the position in the PlanetViewer
            setShowInputFields(false);
            setCoordinates({x: '', y: ''});
        } catch (error) {
            console.error("Failed to move army", error);
        }
    };

    let troopsOutput = troops.map((troop, index) => (
        <TreeItem key={index} nodeId={`${index}`} label={`${troop.size}x Troop ${troop.troop_type}`}/>
    ));

    let totalCount = troops.reduce((acc, troop) => acc + troop.size, 0);

    return (
        <WindowUI>
            <div className="bg-gray-600 border-4" style={{ padding: "1rem", zIndex: 1, position: 'absolute', top: '10%', left: '10%', width: 'auto', minWidth: '300px', height: 'auto' }}>
                <TreeView aria-label="file system navigator">
                    <h1 className="text-2xl my-1">Army {armyId}</h1>
                    <Button variant="contained" onClick={createCity} sx={{margin: "10px"}}>
                        Create City
                    </Button>
                    <TreeItem className="border-2" sx={{ padding: "0.25rem" }} nodeId={`stats-${armyId}`} label={`Stats`}></TreeItem>
                    <TreeItem className="border-2" sx={{ padding: "0.25rem" }} nodeId={`total-${armyId}`} label={`${totalCount} Units`}>
                        {troopsOutput}
                    </TreeItem>
                </TreeView>
            </div>
        </WindowUI>
    );
}

export default ArmyViewer;
