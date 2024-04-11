import React, {useState, useEffect, useContext} from 'react';
import troopsJson from "./../troops.json"
import "./ArmyViewTroopEntry.css"
import Tooltip from "@mui/material/Tooltip";
function ArmyViewTroopEntry(props) {

    return (
        <div className="ArmyViewTroopEntry">

            <div style={{"width": "20%", height:"auto", "display": "inline-block"}}>
                <img src={(`/images/troop_images/${troopsJson[props.troop_type]["icon"]}`)} draggable={false} unselectable="on"/>
            </div>

            <div className={"ArmyViewTroopEntryInfo"}>

                <div>
                    {props.troop_type}
                </div>

                <div>
                    <span style={{"color": "gold"}}> {props.troop_size} </span> units
                </div>


            </div>





            {/*Display an icon for the rank of a unit (max 11, because we only have images till rank 11)*/}
            <div style={{"width": "20%", height:"auto", "display": "inline-block"}}>
                <Tooltip title={`rank ${props.rank}`}>
                <img src={(`/images/ranks/Rank${Math.min(props.rank, 11)}.png`)} draggable={false} unselectable="on"/>
                </Tooltip>
            </div>

        </div>
    );
}

export default ArmyViewTroopEntry;