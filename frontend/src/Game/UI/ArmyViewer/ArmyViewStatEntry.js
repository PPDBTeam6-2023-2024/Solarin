import React, {useState, useEffect, useContext} from 'react';
import statsJson from "./../stats.json"
import troopsJson from "../troops.json";
import Tooltip from "@mui/material/Tooltip";

function ArmyViewStatEntry(props) {

    /*This component represents a stat entry in the details of an army*/
    return (
        <div style={{"width": "100%", "marginTop": "0.3vw"}}>
            <div style={{"width": "20%", "display": "inline-block"}}>
                <Tooltip title={`${props.stat_name}`}>
                <img src={(`/images/stats_icons/${statsJson[props.stat_name]["icon"]}`)} draggable={false} unselectable="on"/>
                </Tooltip>
            </div>

            <div style={{"width": "65%", "display": "inline-block", "textAlign": "right"}}>
                {Math.round(props.stat_value)}
            </div>
        </div>
    );
}

export default ArmyViewStatEntry;