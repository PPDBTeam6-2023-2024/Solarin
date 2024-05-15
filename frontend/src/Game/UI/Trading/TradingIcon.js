
import './TradingIcon.css'
import { IoMdClose } from "react-icons/io";

import React, {useState} from "react";
import TradingMenu from "./TradingMenu";

import WindowUI from '../WindowUI/WindowUI';
function TradingIcon() {
    const [tradeMenuOpen, setTradeMenuOpen] = useState(false);
    const [hideMenu, setHideMenu] = useState(false)
    return (
        <WindowUI windowName="tradingMenu" hideState={hideMenu}>
            <>
            <div id={"trading_icon"} className="bottom-0 fixed transition ease-in-out" onClick={() => setTradeMenuOpen(!tradeMenuOpen)}>
                <IoMdClose className='text-5xl' onClick={() => setHideMenu(!hideMenu)}/>

                <img src={(`/images/icons/trade_icon.png`)} className="bottom-0 absolute" draggable={false}
                     unselectable="on"/>
            </div>
            {tradeMenuOpen && <TradingMenu/>}
            </>
        </WindowUI>
    )
}

export default TradingIcon