import React, {useContext} from "react";
import './ProfileListEntry.css';
import {ViewModeContext, View} from "../../Context/ViewModeContext";

function ProfileListEntry(props) {
    const [viewMode, setViewMode] = useContext(ViewModeContext)

    return (
        <div className="ProfileListEntry">
            <div style={{"width": "40%", "display": "inline-block"}}>
                {props.text}
            </div>

            <div className={"goto"} style={{"width": "40%", "display": "inline-block"}} onClick={() => setViewMode(View.PlanetView)}>
                Go To {props.type}
            </div>
        </div>

    )
}

export default ProfileListEntry