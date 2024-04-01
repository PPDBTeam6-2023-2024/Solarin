import React, {useContext} from "react";
import './ProfileListEntry.css';
import {ViewModeContext, View} from "../../Context/ViewModeContext";
import Game from "../../Game";

function ProfileListEntry(props) {
    const [viewMode, setViewMode] = useContext(ViewModeContext)

    const handleClick = () => {
        console.log(`planetID of clicked entity: ${props.planet_id}`)
        props.changePlanet(props.planet_id)
        setViewMode(View.PlanetView)
    }

    return (
        <div className="ProfileListEntry">
            <div style={{"width":"70%", "display": "inline-block"}}>
                {props.text}
            </div>

            <div className="goto" style={{"width":"30%", "display": "inline-block"}} onClick={handleClick}>
                Go To {props.type} at ({props.x}, {props.y})
            </div>
        </div>

    )
}

export default ProfileListEntry