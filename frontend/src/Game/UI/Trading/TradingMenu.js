import React, {useContext, useEffect, useRef, useState} from "react";
import "./TradingMenu.css"
import WindowUI from "../WindowUI/WindowUI";

import ResourceFilter from "./ResourceFilter";
import {useDispatch, useSelector} from "react-redux";
import TradingOfferEntry from "./TradingOfferEntry";
import {UserInfoContext} from "../../Context/UserInfoContext";
import {openAddTradeContext} from "./openAddTradeContext";
import AddTradeEntry from "./AddTradeEntry";
import {tradeSocketContext} from "./TradeSocketContext";
import {initializeResources} from "../ResourceViewer/ResourceViewer";

function TradingMenu(props) {
    /*THIS MENU (and its components) IS PART OF A MOCK, AND IS NOT YET THE RESULTING REPRESENTATION*/
    const [selectedFilter, setSelectedFilter] = useState("");
    const [userInfo, setUserInfo] = useContext(UserInfoContext);

    const [tradeSocket, setTradeSocket] = useState(null);

    const [trades, setTrades] = useState([]);
    const [ownOffers, setOwnOffers] = useState([]);

    const [openAddTrade, setOpenAddTrade] = useState(false);

    const dispatch = useDispatch();

    const isConnected = useRef(false);
    useEffect(() => {
        if (isConnected.current) return

        isConnected.current = true;

        const webSocket = new WebSocket(`${process.env.REACT_APP_BACKEND_PATH_WEBSOCKET}/trading/ws`,
            `${localStorage.getItem('access-token')}`);

        setTradeSocket(webSocket);
    }, []);

    useEffect(() => {
        if (!tradeSocket) return;

        /*Send the first get_trade event te get the currently available trades*/

        tradeSocket.onopen = () => {
            tradeSocket.send(
                JSON.stringify(
                    {
                        type: "get_trades"
                    })
            )

        }

        tradeSocket.onmessage = (event) => {
            let data = JSON.parse(event.data)

            if (data.action === "show_trades") {
                setTrades(data.trades);
                setOwnOffers(data.own_offers)
                initializeResources(dispatch)
            }

        };

        return () => {
            tradeSocket.close();
        };
    }, [tradeSocket]);



    return (
      <WindowUI>

          {/*Creates the div that contains the chat menu*/}
          <div className="TradingMenuWidget absolute left-0">
              <openAddTradeContext.Provider value={[openAddTrade, setOpenAddTrade]}>
                  <tradeSocketContext.Provider value={[tradeSocket, setTradeSocket]}>
                {userInfo.alliance ?
                    <>
                        <ResourceFilter filter={[selectedFilter, setSelectedFilter]} addTrade={[openAddTrade, setOpenAddTrade]}/>

                        <div className="TradingMenuOffers">
                            {/*Displays the menu to create a new trade*/}
                            {openAddTrade && <AddTradeEntry/>}

                            {ownOffers.map((value, index) =>
                            (<TradingOfferEntry give_resources={value.gives} receive_resources={value.receives}
                                                own={true} offer_id={value.offer_id} filter={selectedFilter}/>))}

                            {trades.map((value, index) =>
                            (<TradingOfferEntry give_resources={value.gives} receive_resources={value.receives}
                                                own={false} offer_id={value.offer_id} filter={selectedFilter}/>))}

                        </div>


                    </>:
                    <>
                        This feature becomes available when you join an alliance
                    </>
                }
                </tradeSocketContext.Provider>
              </openAddTradeContext.Provider>

          </div>



      </WindowUI>
    )
}

export default TradingMenu