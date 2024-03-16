import React from "react";
import {Button} from "@mui/material";
import './SendMessage.css'
function SendMessage(props) {
    /**
     * making it possible for a user to send new messages
     * */
    return (
        <div className="SendMessageTab">
                  <textarea name="message_body" className="bg-gray-900" required/>
                  <button onClick=onClick={() => props.socket.send(
                      JSON.stringify({
                          type: "new message",
                          body: ""
                      })
                  )}>Send</button>
        </div>

    )
}

export default SendMessage