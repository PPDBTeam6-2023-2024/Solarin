import React from "react";
import axios from "axios";
import RequestEntry from "../Requests/RequestEntry";

function FriendRequestEntry(props) {
    /**
     * This component represent 1 friend request
     * */

    const sendRequestReply = async (friend_id, accepted) => {
        /*
        * communicate to the server whether we accepted or rejected this friend request
        * */
        try {
            const response = await axios.post(`${process.env.REACT_APP_BACKEND_PATH}/chat/friend_requests`,
                JSON.stringify({
                    "friend_id": friend_id,
                    "accepted": accepted,
                    "type": "review"
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

            <RequestEntry text={`Friend request from\n ${props.user}`} onTrue={() => {
                sendRequestReply(props.user_id, true);
                props.onEntryChose()
            }}
                          onFalse={() => {
                              sendRequestReply(props.user_id, false);
                              props.onEntryChose()
                          }}/>
        </>
    )
}

export default FriendRequestEntry