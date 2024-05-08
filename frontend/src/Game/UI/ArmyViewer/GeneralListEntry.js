import React, {useState} from 'react';
import troopsJson from "./../troops.json"
import "./ArmyViewTroopEntry.css"
import Tooltip from "@mui/material/Tooltip";
import "./GeneralView.css"
import SelectGeneralView from "./SelectGeneralView";
import generalsJson from "./generals.json"
import axios from "axios";
import GeneralViewStatEntry from "./GeneralViewStats";
import "./GenerallistEntry.css"

function GeneralListEntry({generalInfo, armyId, onChangeGeneral}) {
    /*Display the general that is part of the army*/
    return (
        <div className="GeneralListEntry" onClick={() => {onChangeGeneral(armyId, generalInfo.name)}}>
            <span style={{"fontSize": "150%", "color": "gold"}}>General {generalInfo.name}</span>
            <img src={(`/images/general_images/${generalsJson[generalInfo.name]["icon"]}`)} style={{"width": "40%"}}
                 draggable={false}
                     unselectable="on"/>

            {generalInfo.modifiers.map((modifier, index) =>
                <div>
                    <GeneralViewStatEntry key={index} stat_name={modifier.stat} stat_value={modifier.modifier}
                    political_stat_name={modifier.political_stance}
                    political_stat_value={modifier.political_stance_modifier}/>
                </div>
            )}
        </div>

    );
}

export default GeneralListEntry;