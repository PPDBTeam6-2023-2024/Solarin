import React from "react";
import './ProfileListEntry.css';

function ProfileListEntry(props) {
    return (
        <div className="ProfileListEntry">
            <div style={{"width": "40%", "display": "inline-block"}}>
                {props.text}
            </div>

            <div style={{"width": "40%", "display": "inline-block"}}>
                Go To {props.type}
            </div>
        </div>

    )
}

export default ProfileListEntry