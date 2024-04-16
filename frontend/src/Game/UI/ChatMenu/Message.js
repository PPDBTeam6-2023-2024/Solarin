import React from "react";
import './Message.css'

function Message(props) {
    return (
        <>

            <div className="MessageBody" style={{"width": "95%"}}>
                <div className="MessageSender" style={{"width": "100%"}}>
                    {props.message.sender_name} at {props.message.created_at}
                </div>

                {props.message.body}
            </div>
        </>

    )
}

export default Message