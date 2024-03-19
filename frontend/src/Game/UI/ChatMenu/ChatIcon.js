
import './ChatIcon.css'

import chat_icon from "../../Images/icons/chat_icon.png";
import React, {useState} from "react";
import ChatMenu from "./ChatMenu";
function ChatIcon() {
    const [chatMenuOpen, setChatMenuOpen] = useState(false);
    return (
        <>
            <div id={"chat_icon"} className="bottom-0 right-0 fixed transition ease-in-out" onClick={() => setChatMenuOpen(!chatMenuOpen)}>
                <img src={chat_icon} className="bottom-0 absolute" draggable="false"/>
            </div>

            {chatMenuOpen && <ChatMenu/>}
        </>


    )
}

export default ChatIcon