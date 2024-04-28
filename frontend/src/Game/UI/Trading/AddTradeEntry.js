import React, {useEffect, useState} from "react";
import resourcesJson from "../ResourceViewer/resources.json"
import "./AddTradeEntry.css"
import {useSelector} from "react-redux";
import {initParticlesEngine} from "@tsparticles/react";
import {loadSlim} from "@tsparticles/slim";
import Tooltip from "@mui/material/Tooltip";
const addTradeResourceList = (onClickAction, skip_list) => {
    return (
        <ul style={{"overflow": "scroll", "maxHeight": "8vw", "width": "30%"}}>
            {Object.entries(resourcesJson).map((resource, index) =>
                <>

                {!skip_list.includes(resource[0]) &&
                    <li key={resource[0]} className="AddTradeEntryResource" onClick={() => onClickAction(resource[0])}>
                    <img src={(`/images/resources/${resourcesJson[resource[0]]["icon"]}`)}
                               alt={resource[0]} draggable={false}/>
                    </li>
                }
                </>

            )}
        </ul>
    )
}

function AddTradeEntry(props) {

    /*This gives corresponds with what the user would receive and the accept-er of the trade offer would give*/
    const [gives, setGives] = useState([]);

    /*This gives corresponds with what the user would giveand the accept-er of the trade offer would receive*/
    const [receives, setReceives] = useState([]);

    const addToGive = (resource) => {
        setGives(g => [...g, [resource, 1]]);
    }

    const addToReceive= (resource) => {
        setReceives(r => [...r, [resource, 1]]);
    }

    const resource_amount = useSelector((state) => state.resources.resources)

    useEffect(() => {
        console.log("rerender")
    }, []);

    return (
        <div className="TradingOfferEntry">

            <div className="TradingOfferEntryResourceSide" style={{"marginLeft": "1vw", "width": "30%", "marginRight": "1vw"}}>
            You Receive:
                {gives.map((resource, index) => <div key={resource[0]+""+index} style={{"width": "100%"}}>

                    <img src={(`/images/resources/${resourcesJson[resource[0]]["icon"]}`)} style={{"width": "30%", "display": "inline-block"}}
                           alt={resource[0]} draggable={false}/>
                    <input type="number" name="resourceAmount" value={resource[1]} min="1" max={`${resource_amount[resource[0]]}`} className="AddResourceAmountInput"
                       onChange={(event) => {

                           const updateGives = [...gives];
                            updateGives[index][1] = event.target.value;

                           setGives(updateGives)
                       }}></input>

                    {/*Remove Trade resource*/}

                      <img src={(`/images/icons/reject.png`)} draggable={false}
                           style={{"width": "15%", "display": "inline-block"}}
                           onClick={() => {setGives(g => g.slice(0, index).concat(g.slice(index+1)))}}/>

                    </div>
                    )}
                {addTradeResourceList(addToGive, receives.map((receive) => receive[0]).concat(gives.map((give) => give[0])))}

          </div>

          {/*Shot the exchange symbol*/}
          <div style={{"display": "inline-block"}}>
              <img src={(`/images/icons/exchange.png`)} draggable={false} style={{"width": "3vw"}}/>
          </div>


          <div className="TradingOfferEntryResourceSide" style={{"width": "30%", "marginLeft": "1vw"}}>
            You Give:
              {receives.map((resource, index) => <div key={resource[0]+""+index} style={{"width": "100%"}}>

                <img src={(`/images/resources/${resourcesJson[resource[0]]["icon"]}`)} style={{"width": "30%", "display": "inline-block"}}
                       alt={resource[0]} draggable={false}/>
                <input type="number" name="resourceAmount" value={resource[1]} min="1" max={`${resource_amount[resource[0]]}`} className="AddResourceAmountInput"
                   onChange={(event) => {

                       const updateReceives = [...receives];
                        updateReceives [index][1] = Math.min(event.target.value, resource_amount[resource[0]]);

                       setReceives(updateReceives)
                   }}></input>

                    {/*Remove Trade resource*/}

                      <img src={(`/images/icons/reject.png`)} draggable={false}
                           style={{"width": "15%", "display": "inline-block"}} 
                           onClick={() => {setReceives(r => r.slice(0, index).concat(r.slice(index+1)))}}/>

                </div>
                )}
              {addTradeResourceList(addToReceive, receives.map((receive) => receive[0]).concat(gives.map((give) => give[0])))}

          </div>
            {/*Trading offer accept button*/}
          <Tooltip title={"Create the Trade Offer"}>
              <div className="offer_button">
                  <img src={(`/images/icons/accept.png`)} draggable={false}
                       style={{"width": "3vw", "display": "inline-block"}}/>
              </div>
           </Tooltip>

        </div>

    )
}

export default AddTradeEntry