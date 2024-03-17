import React, {useEffect, useState} from "react";
import Draggable from "react-draggable";
import axios from "axios";
import './FriendRequestEntry.css'

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
              "accepted": accepted
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
          {/*Creates the div that contains the chat menu*/}
      <div className="transition ease-in-out" id={"FriendRequestEntryVisual"} >
          <div style={{"width": "45%"}}>
              Friend request from
              '{props.user}'
          </div>

          <button style={{"backgroundColor": "green"}} onClick={() => {SendRequestReply(props.user_id, true); props.onEntryChose()}}>
              accept
          </button>
          <button style={{"backgroundColor": "red"}} onClick={() => {SendRequestReply(props.user_id, false); props.onEntryChose()}}>
              reject
          </button>

      </div>
    </>
    )
}

export default FriendRequestEntry