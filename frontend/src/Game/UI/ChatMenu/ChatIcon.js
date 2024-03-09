
import './ChatIcon.css'

import chat_icon from "../../Images/icons/chat_icon.png";
import React from "react";

function ChatIcon() {
    return (
        <div id={"chat_icon"} className="bottom-0 right-0 absolute">
            <img src={chat_icon} className="bottom-0 absolute" draggable="false"/>
        </div>
    )
}

export default ChatIcon