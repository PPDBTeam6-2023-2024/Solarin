import './TradingIcon.css'
import {IoMdClose} from "react-icons/io";
import React, {useState} from "react";

import WindowUI from '../WindowUI/WindowUI';
import ChatMenu from "../ChatMenu/ChatMenu";

function TradingIcon() {
    const [chatMenuOpen, setChatMenuOpen] = useState(false);
    const [hideChat, setHideChat] = useState(false)
    return (
        <WindowUI windowName="chatMenu" hideState={hideChat}>
            <>
                <div id={"trading_icon"} className="bottom-0 right-0 fixed transition ease-in-out"
                     onClick={() => setChatMenuOpen(!chatMenuOpen)}>
                    <IoMdClose className='text-7xl' onClick={() => setHideChat(!hideChat)}/>

                    <img src={(`/images/icons/chat_icon.png`)} className="bottom-0 absolute"/>
                </div>
                {chatMenuOpen && <ChatMenu/>}
            </>
        </WindowUI>
    )
}

export default TradingIcon