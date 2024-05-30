import React, {useContext} from "react";
import './ProfileListEntry.css';
import {ViewModeContext, View} from "../../Context/ViewModeContext";
import generalsJson from "./../ArmyViewer/generals.json"
import Tooltip from "@mui/material/Tooltip";
function ProfileListEntry(props) {
    const [viewMode, setViewMode] = useContext(ViewModeContext)

    const handleClick = () => {
        props.changePlanet(props.planet_id)
        setViewMode(View.PlanetView)
    }

    return (
        <div className="ProfileListEntry">
            <div style={{"width": "20%", "display": "inline-block"}}>
                {props.text}
            </div>


            <div style={{"width": "50%", "display": "inline-block"}}>
                {props.popups.map((elem) => <span style={{"display": "inline-block"}} key={props.text}>{elem}</span>)}
            </div>

            <div className="goto" style={{"width": "30%", "display": "inline-block"}} onClick={handleClick}>
                {/*Display a go to location button with rounded cords so we don't have a too ling integer*/}
                Go To {props.type} at ({props.x.toFixed(4)}, {props.y.toFixed(4)})
            </div>


        </div>

    )
}

export default ProfileListEntry