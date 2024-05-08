import axios from "axios";
import React from "react";
import "./AllianceMemberEntry.css"

function AllianceMemberEntry(props) {
    /**
     * This component represent 1 request to join your faction
     * */

    const sendKickUser = async (user_id) => {
        /*
        * when we accept or reject an alliance join request we need to communicate that to the backend
        * */
        try {
            await axios.post(`${process.env.REACT_APP_BACKEND_PATH}/chat/kick_user`,
                JSON.stringify({
                    "user_id": user_id
                }),
                {
                    headers: {
                        'content-type': 'application/json',
                        'accept': 'application/json',
                    },
                }
            )
            props.onEntryChose();
        } catch (e) {
        }

    }

    return (
        <>
            <div className="AllianceMemberEntry">
                <div style={{"paddingLeft": "10%", "paddingRight": "10%"}}>{props.user}</div>

                <button style={{"marginLeft": "10%"}} onClick={() => {sendKickUser(props.user_id)}}>Kick User</button>

            </div>
        </>
    )
}

export default AllianceMemberEntry