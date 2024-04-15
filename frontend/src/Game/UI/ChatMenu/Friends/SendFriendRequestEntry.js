import React, {useState} from "react";
import axios from "axios";
import '../Requests/RequestEntry.css'
import "../Requests/RequestButtons.css"

function SendFriendRequestEntry(props) {
    /**
     * a component for sending a simple 1 input friend request and expecting a response message
     * */
    /*friend request name*/
    const [friendRequestName, setFriendRequestName] = useState("");
    const [anwserMessage, setAnwserMessage] = useState("");


    const sendFriendRequest = async (username) => {
        try {
            /*send a post request to try and create or join the alliance*/
            axios.defaults.headers.common = {'Authorization': `Bearer ${localStorage.getItem('access-token')}`}
            const response = await axios.post(`${process.env.REACT_APP_BACKEND_PATH}/chat/friend_requests`,
                JSON.stringify({
                    type: "add",
                    username: username
                }),
                {
                    headers: {
                        'content-type': 'application/json',
                        'accept': 'application/json',
                    },
                }
            )
            setAnwserMessage(response.data.message)
        } catch (e) {
            return ""
        }
    }


    return (
        <>

            <div>
                Send Friend request:
                <input name="friend_name" value={friendRequestName}
                       onChange={(event) => {
                           setFriendRequestName(event.target.value)
                       }}
                       className="bg-gray-900" required/>

                <button className="RequestButton" onClick={() => sendFriendRequest(friendRequestName)}> Send</button>

                {/*Display the message that is received after sending the friend request*/}
                {anwserMessage}
            </div>
        </>
    )
}

export default SendFriendRequestEntry