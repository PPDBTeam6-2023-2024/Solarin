import axios from "axios";
import RequestEntry from "../Requests/RequestEntry";
import React from "react";

function AllianceRequestEntry(props) {
    /**
     * This component represent 1 request to join your faction
     * */

    const SendRequestReply = async (user_id, accepted) => {
        /*
        * when we accept or reject an alliance join request we need to communicate that to the backend
        * */
        try {
            axios.defaults.headers.common = {'Authorization': `Bearer ${localStorage.getItem('access-token')}`}
            const response = await axios.post(`${process.env.REACT_APP_BACKEND_PATH}/chat/alliance_requests`,
                JSON.stringify({
                    "user_id": user_id,
                    "accepted": accepted
                }),
                {
                    headers: {
                        'content-type': 'application/json',
                        'accept': 'application/json',
                    },
                }
            )
        } catch (e) {
        }


    }


    return (
        <>
            <RequestEntry text={`join request\n '${props.user}'`} onTrue={() => {
                SendRequestReply(props.user_id, true);
                props.onEntryChose()
            }}
                          onFalse={() => {
                              SendRequestReply(props.user_id, false);
                              props.onEntryChose()
                          }}/>
        </>
    )
}

export default AllianceRequestEntry