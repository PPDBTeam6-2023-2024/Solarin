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
    /*This menu is the trading menu, when a user opens the trading menu this component will appear*/

    /*Select Filter keeps track if and which item filter is set*/
    const [selectedFilter, setSelectedFilter] = useState("");

    /*Get access to user information*/
    const [userInfo, setUserInfo] = useContext(UserInfoContext);

    /*This state stores the websocket used for trading*/
    const [tradeSocket, setTradeSocket] = useState(null);

    /*Trades lists a list of trades offered by other users*/
    const [trades, setTrades] = useState([]);

    /*OwnOffers list the offers offered by the user itself*/
    const [ownOffers, setOwnOffers] = useState([]);

    /*Players can also create new trade offers. To keep track if the add trade menu is open or not, we use this state*/
    const [openAddTrade, setOpenAddTrade] = useState(false);

    const dispatch = useDispatch();

    /*
    * Connect the trading websocket to the backend
    * */
    const isConnected = useRef(false);
    useEffect(() => {
        if (isConnected.current) return

        isConnected.current = true;

        const webSocket = new WebSocket(`${process.env.REACT_APP_BACKEND_PATH_WEBSOCKET}/trading/ws`,
            `${localStorage.getItem('access-token')}`);

        setTradeSocket(webSocket);
    }, []);

    /*Receive trade events from the websocket*/
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

        /*Receive trade messages containing the trade data*/
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
              {/*Use of context for clean access in child components*/}
              <openAddTradeContext.Provider value={[openAddTrade, setOpenAddTrade]}>
              <tradeSocketContext.Provider value={[tradeSocket, setTradeSocket]}>

                  {/*Users that are not in an alliance will not be able to see the trading menu*/}
                  {userInfo.alliance ?
                      <>
                          {/*Displays the resource filter part a the top of the window*/}
                          <ResourceFilter filter={[selectedFilter, setSelectedFilter]}
                                          addTrade={[openAddTrade, setOpenAddTrade]}/>

                          <div className="TradingMenuOffers">
                              {/*Displays the menu to create a new trade*/}
                              {openAddTrade && <AddTradeEntry/>}

                              {/*Display the own trade offers*/}
                              {ownOffers.map((value, index) =>
                              (<TradingOfferEntry give_resources={value.gives} receive_resources={value.receives}
                                                own={true} offer_id={value.offer_id} filter={selectedFilter}/>))}

                              {/*Display others their trade offers*/}
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