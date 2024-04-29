import React, {useContext, useEffect, useState} from "react";
import "./TradingMenu.css"
import WindowUI from "../WindowUI/WindowUI";

import ResourceFilter from "./ResourceFilter";
import {useSelector} from "react-redux";
import "./TradingOfferEntry.css"
import resourcesJson from "../ResourceViewer/resources.json"
import {tradeSocketContext} from "./TradeSocketContext";
import {initializeResources} from "../ResourceViewer/ResourceViewer";

const getOfferResourceSide = (to_map) => {
    return to_map.map((map_element, index) =>
      <div>
          <img key={index} src={(`/images/resources/${resourcesJson[map_element[0]]["icon"]}`)}
                           alt={map_element[0]} draggable={false} style={{"width": "60%"}}/>

          <div style={{"fontSize": "1.2vw", "textAlign": "center", "width": "60%"}}>{map_element[1]}</div>
      </div>

    )
}


function TradingOfferEntry({give_resources, receive_resources, own, offer_id, filter}) {

    const [tradeSocket, setTradeSocket] = useContext(tradeSocketContext);

    /*Changes display depending on whether the user is owner of the trade offer or not*/
    const getKey = (giving) =>{

        if (giving ^ own){
            return "Give"
        }else{
            return "Receive"
        }

    }

    const handleOffer= () => {
        let packet;


        if (own){
            packet = JSON.stringify(
            {
                "type": "cancel_trade",
                "offer_id": offer_id

            })
        }else{
            packet = JSON.stringify(
            {
                "type": "accept_trade",
                "offer_id": offer_id

            })

        }

        tradeSocket.send(packet)
    }

    const inFilter = () => {
        if (filter === ""){
            return true
        }

        let check_list = receive_resources
        if (own){
            check_list = give_resources
        }

        let mapped = check_list.map((value) => value[0])
        return mapped.includes(filter)
    }
    return (
        <>
            {inFilter() &&
            <div className="TradingOfferEntry">
          <div className="TradingOfferEntryResourceSide" style={{"marginLeft": "3vw", "width": "20%"}}>

              {getKey(true)}:
              {/*Displays the resources the offer accept-er needs to give */}
              {getOfferResourceSide(give_resources)}
          </div>

          {/*Shot the exchange symbol*/}
          <div style={{"display": "inline-block"}}>
              <img src={(`/images/icons/exchange.png`)} draggable={false} style={{"width": "3vw"}}/>
          </div>


          <div className="TradingOfferEntryResourceSide" style={{"width": "20%", "marginLeft": "1vw"}}>
            {getKey(false)}:
              {/*Displays the resources the offer accept-er receives */}
              {getOfferResourceSide(receive_resources)}

          </div>

          {/*Trading offer accept/reject button*/}
          <div className="offer_button" onClick={handleOffer}>
              {own ?
                  <img src={(`/images/icons/reject.png`)} draggable={false}
                   style={{"width": "3vw", "display": "inline-block"}}/>:
                  <img src={(`/images/icons/accept.png`)} draggable={false}
                       style={{"width": "3vw", "display": "inline-block"}}/>
              }

          </div>

        </div>}
        </>


    )
}

export default TradingOfferEntry