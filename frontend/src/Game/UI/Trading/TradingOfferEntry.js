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
    /*
    * Displays the list of resources on 1 side of the trade offer (gives or receives)
    * */
    return to_map.map((map_element, index) =>
      <div>
          <img key={index} src={(`/images/resources/${resourcesJson[map_element[0]]["icon"]}`)}
                           alt={map_element[0]} draggable={false} style={{"width": "60%"}}/>

          <div style={{"fontSize": "1.2vw", "textAlign": "center", "width": "60%"}}>{map_element[1]}</div>
      </div>

    )
}


function TradingOfferEntry({give_resources, receive_resources, own, offer_id, filter}) {
    /*
    * This component displays a trade Offer
    * */
    const [tradeSocket, setTradeSocket] = useContext(tradeSocketContext);

    /*Changes display depending on whether the user is owner of the trade offer or not*/
    const getKey = (giving) =>{

        if (giving ^ own){
            return "Give"
        }else{
            return "Receive"
        }

    }

    /*
    * Access to the amount of resources the user has
    * */
    const resourceAmount = useSelector((state) => state.resources.resources)

    const hasEnoughResources = (gives) => {
        /*
        * We want to let our display of the accept button depend on whether the user can accept this trade offer
        * For this we will check if the user has enough resources
        * */

        let canPay = true;

        gives.forEach((element) => {
            canPay = canPay && resourceAmount[element[0]] >= element[1];
        })
        return canPay
    }


    {/*Send a trade accept/cancel message depending on whether the user is the trade offer its owner or not*/}
    const handleOffer= () => {
        let trade_type;

        if (own){
            trade_type = "cancel_trade"
        }else{
            trade_type = "accept_trade"
        }

        tradeSocket.send(JSON.stringify(
            {
                "type": trade_type,
                "offer_id": offer_id

        }))
    }

    /*
    * Check if the filter allows this offer to be displayed
    * */
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
            {/*Only display this offer if the filter allows it*/}
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

                {own ?
                    <div className="offer_button" onClick={handleOffer}>
                    <img src={(`/images/icons/reject.png`)} draggable={false}
                         style={{"width": "3vw", "display": "inline-block"}}/>
                    </div>:

                    <>
                    {hasEnoughResources(give_resources) &&
                        <div className="offer_button" onClick={handleOffer}>
                        <img src={(`/images/icons/accept.png`)} draggable={false}
                             style={{"width": "3vw", "display": "inline-block"}}/>
                        </div>
                    }
                    </>


                }

            </div>
            }
        </>


    )
}

export default TradingOfferEntry