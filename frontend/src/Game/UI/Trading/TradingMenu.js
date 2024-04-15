import React, {useState} from "react";
import "./TradingMenu.css"
import WindowUI from "../WindowUI/WindowUI";

import ResourceFilter from "./ResourceFilter";
import {useSelector} from "react-redux";
import TradingOfferEntry from "./TradingOfferEntry";

function TradingMenu(props) {
    /*THIS MENU (and its components) IS PART OF A MOCK, AND IS NOT YET THE RESULTING REPRESENTATION*/
    const [selectedFilter, setSelectedFilter] = useState("");
    return (
      <WindowUI>
          {/*Creates the div that contains the chat menu*/}
          <div className="TradingMenuWidget absolute left-0">
                <ResourceFilter filter={[selectedFilter, setSelectedFilter]}/>
                {[["SOL", 1], ["TF", 1], ["SOL", 3]].map((value, index) => (<TradingOfferEntry give_resource={value[0]} receive_resource={"UR"}/>))}
          </div>
      </WindowUI>
    )
}

export default TradingMenu