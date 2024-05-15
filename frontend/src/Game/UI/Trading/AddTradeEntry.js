import React, {useContext, useEffect, useState} from "react";
import resourcesJson from "../ResourceViewer/resources.json"
import "./AddTradeEntry.css"
import {useSelector} from "react-redux";
import {initParticlesEngine} from "@tsparticles/react";
import {loadSlim} from "@tsparticles/slim";
import Tooltip from "@mui/material/Tooltip";
import {tradeSocketContext} from "./TradeSocketContext";
import {openAddTradeContext} from "./openAddTradeContext";
import {TextColorContext} from "../../Context/ThemeContext";


const addTradeResourceList = (onClickAction, skip_list) => {
    /*
    * We will show a list of all the resources a user can select to trade
    * This function will return this list.
    * OnClickAction will be triggered when the user selects a certain resource
    * skip_list is a list of resources that are not allowed to be displayed anymore,
    * for example when it is already used in a trade
    * */
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
    /*
    * This component will show the component used to create new trade offers
    * In this component a user can choose which resources he/she wants to give/receive and how much of each
    * */

    const [textColor, setTextColor] = useContext(TextColorContext);

    const [tradeSocket, setTradeSocket] = useContext(tradeSocketContext);
    const [openAddTrade, setOpenAddTrade] = useContext(openAddTradeContext);

    /*This gives corresponds with what the user would receive and the accept-er of the trade offer would give*/
    const [gives, setGives] = useState([]);

    /*This gives corresponds with what the user would give and the accept-er of the trade offer would receive*/
    const [receives, setReceives] = useState([]);

    /*
    * Add a resource to the list of resources we want to give
    * */
    const addToGive = (resource) => {
        setGives(g => [...g, [resource, 1]]);
    }

    /*
    * Add a resource to the list of resources we want to receive
    * */
    const addToReceive= (resource) => {
        setReceives(r => [...r, [resource, 0]]);
    }

    /*
    * Send the creation request of the trade to the backend
    * */
    const addTradeOffer = () => {
        tradeSocket.send(

            JSON.stringify(
            {
                "type": "create_trade",
                "gives": gives,
                "receives": receives

            })

        )
        setOpenAddTrade(false);

    }

    /*
    * Access to the amount of resources the user has
    * */
    const resourceAmount = useSelector((state) => state.resources.resources)

    const getResourceSide = (title, resourceList, setResourceList, addToResourceList, onChange) => {
        /*
        * The AddTrade Entry has 2 sides a receive and a give side.
        * Most of the script is the same, so this function will make it possible to reduce the amount
        * of duplicated code
        * */


        return (
            <div className="TradingOfferEntryResourceSide"
                 style={{"marginLeft": "1vw", "width": "30%", "marginRight": "1vw"}}>
                {title}:
                {resourceList.map((resource, index) =>
                    <div key={resource[0]+""+index} style={{"width": "100%"}}>
                        {/*For each resource display the resource image*/}
                        <img src={(`/images/resources/${resourcesJson[resource[0]]["icon"]}`)}
                             style={{"width": "30%", "display": "inline-block"}}
                               alt={resource[0]} draggable={false}/>
                        {/*For each resource display an input place to modify the amount of this resource for
                        this trade*/}
                        <input type="number" name="resourceAmount" value={resource[1]}
                               min="0"
                               max={`${resourceAmount[resource[0]]}`}
                               className="AddResourceAmountInput" style={{"color": textColor}}
                           onChange={(event) => { onChange(event, index, resource) }}></input>

                        {/*Remove Trade resource button*/}
                        <img src={(`/images/icons/reject.png`)} draggable={false}
                           style={{"width": "15%", "display": "inline-block"}}
                           onClick={() => {setResourceList(g => g.slice(0, index).concat(g.slice(index+1)))}}/>

                    </div>
                    )}
                {/*Displays a list of all the resources that are not a part of this trade*/}
                {addTradeResourceList(addToResourceList,
                    receives.map((receive) => receive[0]).concat(gives.map((give) => give[0])))}

            </div>

        )
    }

    /*
    * Update the trade number
    * */
    const onChangeGive = (event, index, resource) => {
        const updateGives = [...gives];
        updateGives[index][1] = Number(event.target.value);

        setGives(updateGives)
    }

    /*
    * A user cannot offer more resources than it has, so in that case when the provided number
    * is higher than the amount of resources the user has, we will automatically reduce it to the amount
    * of resources the user has
    */
    const onChangeReceive = (event, index, resource) => {
        const updateReceives = [...receives];
        updateReceives [index][1] = Math.min(event.target.value, resourceAmount[resource[0]]);
        setReceives(updateReceives)
    }

    return (
        <div className="TradingOfferEntry">
            {/*Visualize the resources the trade offer creator would receive on accept*/}
            {getResourceSide("You Receive", gives, setGives, addToGive, onChangeGive)}

            {/*Shot the exchange symbol*/}
            <div style={{"display": "inline-block"}}>
                <img src={(`/images/icons/exchange.png`)} draggable={false} style={{"width": "3vw"}}/>
            </div>

            {/*Visualize the resources the trade offer creator would give on accept*/}
            {getResourceSide("You Give", receives, setReceives, addToReceive, onChangeReceive)}

            {/*Trading offer accept button*/}
            <Tooltip title={"Create the Trade Offer"}>
                <div className="offer_button" onClick={addTradeOffer}>
                    <img src={(`/images/icons/accept.png`)} draggable={false}
                         style={{"width": "3vw", "display": "inline-block"}}/>
                </div>
           </Tooltip>

        </div>

    )
}

export default AddTradeEntry