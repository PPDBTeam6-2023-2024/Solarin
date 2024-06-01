import React, {useContext, useState} from 'react';
import troopsJson from "./../troops.json"
import "./ArmyViewTroopEntry.css"
import Tooltip from "@mui/material/Tooltip";
import "./GeneralView.css"
import SelectGeneralView from "./SelectGeneralView";
import generalsJson from "./generals.json"
import axios from "axios";
import GeneralViewStatEntry from "./GeneralViewStats";
import "./GenerallistEntry.css"
import {TextColorContext} from "../../Context/ThemeContext";

function GeneralListEntry({generalInfo, armyId, onChangeGeneral}) {
    /**
     * Display the general that is part of the army
     * */
    const [textColor, setTextColor] = useContext(TextColorContext)
    return (
        <div className="GeneralListEntry" onClick={() => {onChangeGeneral(armyId, generalInfo.name)}}>
            <span style={{"fontSize": "150%", "color": textColor}}>General {generalInfo.name}</span>
            {/*Show the image of the general*/}
            <img src={(`/images/general_images/${generalsJson[generalInfo.name]["icon"]}`)} style={{"width": "40%"}}
                 draggable={false}
                     unselectable="on"/>

            {generalInfo.modifiers.map((modifier, index) =>
                <div>
                    {/*Displays the stats of the general*/}
                    <GeneralViewStatEntry key={index} stat_name={modifier.stat} stat_value={modifier.modifier}
                    political_stat_name={modifier.political_stance}
                    political_stat_value={modifier.political_stance_modifier}/>
                </div>
            )}
        </div>

    );
}

export default GeneralListEntry;