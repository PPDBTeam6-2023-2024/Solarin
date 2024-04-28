import React, {useContext, useEffect, useRef, useState} from "react";
import "./TradingMenu.css"
import WindowUI from "../WindowUI/WindowUI";

import ResourceFilter from "./ResourceFilter";
import {useSelector} from "react-redux";
import TradingOfferEntry from "./TradingOfferEntry";
import {UserInfoContext} from "../../Context/UserInfoContext";
import {openAddTradeContext} from "./openAddTradeContext";
import AddTradeEntry from "./AddTradeEntry";


function TradingMenu(props) {
    /*THIS MENU (and its components) IS PART OF A MOCK, AND IS NOT YET THE RESULTING REPRESENTATION*/
    const [selectedFilter, setSelectedFilter] = useState("");

    const [userInfo, setUserInfo] = useContext(UserInfoContext);

    const [tradeSocket, setTradeSocket] = useState(null);

    const [trades, setTrades] = useState([]);
    const [ownOffers, setOwnOffers] = useState([]);

    const [openAddTrade, setOpenAddTrade] = useState(false);

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
            console.log("d", data)
            if (data.action === "show_trades") {
                console.log("data")
                setTrades(data.trades);
                setOwnOffers(data.own_offers)
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
                {userInfo.alliance ?
                    <>
                        <ResourceFilter filter={[selectedFilter, setSelectedFilter]} addTrade={[openAddTrade, setOpenAddTrade]}/>

                        <div className="TradingMenuOffers">
                            {/*Displays the menu to create a new trade*/}
                            {openAddTrade && <AddTradeEntry/>}

                            {[["SOL", 1], ["TF", 1], ["SOL", 3], ["SOL", 3], ["SOL", 3]].map((value, index) =>
                            (<TradingOfferEntry give_resources={[value, ["SOL", 4]]} receive_resources={[["UR", 2]]}/>))}
                        </div>


                    </>:
                    <>
                        This feature becomes available when you join an alliance
                    </>
                }
              </openAddTradeContext.Provider>

          </div>



      </WindowUI>
    )
}

export default TradingMenu