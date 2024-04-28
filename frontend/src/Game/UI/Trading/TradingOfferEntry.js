import React, {useState} from "react";
import "./TradingMenu.css"
import WindowUI from "../WindowUI/WindowUI";

import ResourceFilter from "./ResourceFilter";
import {useSelector} from "react-redux";
import "./TradingOfferEntry.css"
import resourcesJson from "../ResourceViewer/resources.json"

const getOfferResourceSide = (to_map) => {
    return to_map.map((map_element, index) =>
      <div>
          <img key={index} src={(`/images/resources/${resourcesJson[map_element[0]]["icon"]}`)}
                           alt={map_element[0]} draggable={false} style={{"width": "60%"}}/>

          <div style={{"fontSize": "1.2vw", "textAlign": "center", "width": "60%"}}>{map_element[1]}</div>
      </div>

    )
}


function TradingOfferEntry({give_resources, receive_resources}) {
    return (
      <div className="TradingOfferEntry">
          <div className="TradingOfferEntryResourceSide" style={{"marginLeft": "3vw", "width": "20%"}}>
            Give:
              {/*Displays the resources the offer accept-er needs to give */}
              {getOfferResourceSide(give_resources)}
          </div>

          {/*Shot the exchange symbol*/}
          <div style={{"display": "inline-block"}}>
              <img src={(`/images/icons/exchange.png`)} draggable={false} style={{"width": "3vw"}}/>
          </div>


          <div className="TradingOfferEntryResourceSide" style={{"width": "20%", "marginLeft": "1vw"}}>
            Receive:
              {/*Displays the resources the offer accept-er receives */}
              {getOfferResourceSide(receive_resources)}

          </div>

          {/*Trading offer accept button*/}
          <div className="offer_button">
              <img src={(`/images/icons/accept.png`)} draggable={false}
                   style={{"width": "3vw", "display": "inline-block"}}/>
          </div>

          {/*Trading offer reject button*/}
          <div className="offer_button">
              <img src={(`/images/icons/reject.png`)} draggable={false}
                   style={{"width": "3vw", "display": "inline-block"}}/>
          </div>
      </div>
    )
}

export default TradingOfferEntry