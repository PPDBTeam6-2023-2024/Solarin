import React, {useState} from 'react';
import troopsJson from "./../troops.json"
import "./ArmyViewTroopEntry.css"
import Tooltip from "@mui/material/Tooltip";
import "./GeneralView.css"
import SelectGeneralView from "./SelectGeneralView";
import generalsJson from "./generals.json"
import axios from "axios";

const addGenerals = async (armyId, generalName) => {
        /*Add a general to the army*/
        const response = await axios.post(`${process.env.REACT_APP_BACKEND_PATH}/general/add_general`,
                JSON.stringify({
                    "army_id": armyId,
                    "general_name": generalName
                }),
                {
                    headers: {
                        'content-type': 'application/json',
                        'accept': 'application/json',
                    },
                }
            )
    }


function GeneralListEntry({generalInfo, armyId}) {
    /*Display the general that is part of the army*/

    console.log("info", generalInfo)
    console.log("2", generalsJson[generalInfo.name], generalInfo.name, generalsJson)
    return (
        <div style={{"width": "50%"}} onClick={() => {addGenerals(armyId, generalInfo.name)}}>
            <img src={(`/images/general_images/${generalsJson[generalInfo.name]["icon"]}`)} draggable={false}
                     unselectable="on"/>
        </div>

    );
}

export default GeneralListEntry;