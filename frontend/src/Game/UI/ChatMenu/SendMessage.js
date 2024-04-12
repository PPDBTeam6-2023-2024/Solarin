import React, {useState} from "react";
import './SendMessage.css'

function SendMessage(props) {
    /**
     * making it possible for a user to send new messages
     * */

    const [pendingMessage, setPendingMessage] = useState("");

    const sendMessage = () => {
        /**
         * send a message to the server
         * */
        props.socket.send(
            JSON.stringify(
                {
                    type: "new message",
                    body: `${pendingMessage}`
                })
        )
        setPendingMessage("")
    }

    return (
        <div className="SendMessageTab">
                  <textarea name="message_body" value={pendingMessage}
                            onChange={(event) => {
                                setPendingMessage(event.target.value)
                            }}
                            className="bg-gray-900" required/>

            <button onClick={sendMessage}>Send</button>
        </div>

    )
}

export default SendMessage