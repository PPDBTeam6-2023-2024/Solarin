import React, {useState} from 'react';
import troopsJson from "./../troops.json"
import "./ArmyViewTroopEntry.css"
import Tooltip from "@mui/material/Tooltip";
import "./GeneralView.css"
import SelectGeneralView from "./SelectGeneralView";
import generalsJson from "./generals.json"
import axios from "axios";



function GeneralListEntry({generalInfo, armyId, onChangeGeneral}) {
    /*Display the general that is part of the army*/

    return (
        <div style={{"width": "50%"}} onClick={() => {onChangeGeneral(armyId, generalInfo.name)}}>
            <img src={(`/images/general_images/${generalsJson[generalInfo.name]["icon"]}`)} draggable={false}
                     unselectable="on"/>
        </div>

    );
}

export default GeneralListEntry;