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
import {PrimaryContext, SecondaryContext, TertiaryContext, TextColorContext} from "../../Context/ThemeContext";
import "./ArmyViewer.css"
import {SplitArmy} from "../../PlanetViewer/CityViewer/BuildingManager"


function ArmyViewer({armyId, is_owner, onCityCreated, in_space}) {
    /**
     * This component visualizes the details menu of an army, containing
     * information about its General, Stats, and troops
     * */

    const [troops, setTroops] = useState([]);
    const [stats, setStats] = useState([]);
    const [general, setGeneral] = useState({});
    const [socket, setSocket] = useContext(SocketContext);
    const [maintenance, setMaintenance] = useState([]);
    const [selectedTroopIndexes, setSelectedTroopIndexes] = useState([]);


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
        onCityCreated()

    };

    // handle clicks on troops
    const handleTroopClick = (index) => {
        if (selectedTroopIndexes.includes(index)) {
            // If already selected, remove from the array
            setSelectedTroopIndexes(selectedTroopIndexes.filter(i => i !== index));
        } else {
            // If not selected, add to the array
            setSelectedTroopIndexes([...selectedTroopIndexes, index]);
        }
    };
    /*Get the selected troops*/
    const handleSplitArmy = async () => {
        /* when all troops are selected, disable splitting army */
        if (troops.length === selectedTroopIndexes.length){
            return
        }
        const selectedTroops = selectedTroopIndexes.map(index => troops[index]);
        await SplitArmy(armyId, selectedTroops).then(
            await new Promise((resolve) => setTimeout(resolve, 50)),
            await socket.send(JSON.stringify({ type: "get_armies" })),
            await fetchTroops(),
            setSelectedTroopIndexes([])
        );
    };



    /*
    * for every troop type in the army create a TroopEntry
    * These troops can be selected, to be able to let them split off from the current army
    * */
    let troopsOutput = troops.map((troop, index) => (
        <div key={index}
             className={`troopEntry ${selectedTroopIndexes.includes(index) ? 'troopEntrySelected' : ''}`}
             onClick={() => handleTroopClick(index)}>
            <ArmyViewTroopEntry troop_type={troop.troop_type} troop_size={troop.size} rank={troop.rank}/>
        </div>
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

    /*
    * Calculate the total amount of troops inside this army
    * */
    let totalCount = troops.reduce((acc, troop) => acc + troop.size, 0);

    /*
    * Visualize the army viewer using the theme colors
    * */
    const [primaryColor, setPrimaryColor] = useContext(PrimaryContext);
    const [secondaryColor, setSecondaryColor] = useContext(SecondaryContext);
    const [tertiaryColor, setTertiaryColor] = useContext(TertiaryContext);
    const [textColor, setTextColor] = useContext(TextColorContext);

    return (
        <WindowUI>
            <div className={"UI"}
                 style={{
                 padding: "1rem", zIndex: 1, position: 'absolute', top: '10%', left: '10%', width: '15vw', minWidth:"300px", height: 'auto',
                 maxHeight: "70vh", "overflow": "scroll",
                 '--primaryColor': primaryColor,
                 '--secundaryColor': secondaryColor,
                 "--tertiaryColor": tertiaryColor,
                 "--textColor": textColor,
                 "border": "0.4vw solid var(--tertiaryColor)"}}>
                <TreeView aria-label="file system navigator">

                    <h1 className="text-2xl my-1">Army {armyId}</h1>

                    {/*Only display the create city button when the user is the owner of that army*/}
                    {is_owner && !in_space &&
                        <Button variant="contained" onClick={createCity} sx={{margin: "10px",
                            backgroundColor: primaryColor, '&:hover': {
                            backgroundColor: secondaryColor,
                            boxShadow: 'none',
                          }}}>
                        Create City
                        </Button>
                    }
                    {selectedTroopIndexes.length > 0 && is_owner && (
                      <Button variant="contained"
                        onClick={handleSplitArmy} sx={{margin: "10px",
                            backgroundColor: primaryColor, '&:hover': {
                            backgroundColor: secondaryColor,
                            boxShadow: 'none',
                          }}}>
                        Split Army
                      </Button>
                    )}


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

                    {/*Only display maintenance option when it contains information*/}
                    {maintenance.length > 0 &&
                        <TreeItem className="border-2" sx={{ padding: "0.2rem" }} nodeId={`maintenance-${armyId}`}
                              label={`Maintenance Cost /hour`}>
                        {maintenanceOutput}

                        </TreeItem>
                    }

                </TreeView>

            </div>
        </WindowUI>
    );
}

export default ArmyViewer;