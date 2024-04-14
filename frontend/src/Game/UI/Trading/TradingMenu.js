import React, {useState} from "react";
import "./TradingMenu.css"
import WindowUI from "../WindowUI/WindowUI";

import ResourceFilter from "./ResourceFilter";
import {useSelector} from "react-redux";


function TradingMenu(props) {
    /*THIS MENU (and its components) IS PART OF A MOCK, AND IS NOT YET THE RESULTING REPRESENTATION*/
    const [selectedFilter, setSelectedFilter] = useState("");
    return (
      <WindowUI>
          {/*Creates the div that contains the chat menu*/}
      <div className="TradingMenuWidget absolute left-0">
            <ResourceFilter filter={[selectedFilter, setSelectedFilter]}/>
            he
      </div>
      </WindowUI>
    )
}

export default TradingMenu