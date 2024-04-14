import React, {useState} from "react";
import "./TradingMenu.css"
import WindowUI from "../WindowUI/WindowUI";

import ResourceFilter from "./ResourceFilter";
import {useSelector} from "react-redux";
import "./TradingOfferEntry.css"
import resourcesJson from "../ResourceViewer/resources.json"
function TradingOfferEntry(props) {
    return (
      <div className="TradingOfferEntry">
          <div className="TradingOfferEntryResourceSide" style={{"marginLeft": "3vw", "width": "15%"}}>
            Give:
              <img src={(`/images/resources/${resourcesJson[props.give_resource]["icon"]}`)}
                                       alt={props.give_resource} draggable={false} style={{"width": "60%"}}/>

          </div>
          <img src={(`/images/icons/exchange.png`)} draggable={false} style={{"width": "3vw", "display": "inline-block"}}/>

          <div className="TradingOfferEntryResourceSide" style={{"width": "15%", "marginLeft": "1vw"}}>
            Receive:
              <img src={(`/images/resources/${resourcesJson[props.receive_resource]["icon"]}`)}
                                       alt={props.receive_resource} draggable={false} style={{"width": "60%"}}/>
          </div>

          {/*Trading offer accept button*/}
          <div className="offer_button">
              <img src={(`/images/icons/accept.png`)} draggable={false} style={{"width": "3vw", "display": "inline-block"}}/>
          </div>

          {/*Trading offer reject button*/}
          <div className="offer_button">
              <img src={(`/images/icons/reject.png`)} draggable={false} style={{"width": "3vw", "display": "inline-block"}}/>
          </div>
      </div>
    )
}

export default TradingOfferEntry