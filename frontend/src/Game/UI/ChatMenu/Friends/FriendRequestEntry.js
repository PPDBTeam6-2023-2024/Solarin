import React, {useEffect, useState} from "react";
import Draggable from "react-draggable";
import axios from "axios";
import RequestEntry from "../Requests/RequestEntry";

function FriendRequestEntry(props) {
    /**
     * This component represent 1 friend request
     * */

    const SendRequestReply = async(friend_id, accepted) => {
        try {
            axios.defaults.headers.common = {'Authorization': `Bearer ${localStorage.getItem('access-token')}`}
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
        }catch (e){}


    }


    return (
      <>

      <RequestEntry text={`Friend request from\n ${props.user}`} onTrue={() => {SendRequestReply(props.user_id, true); props.onEntryChose()}}
        onFalse={() => {SendRequestReply(props.user_id, false); props.onEntryChose()}}/>
    </>
    )
}

export default FriendRequestEntry