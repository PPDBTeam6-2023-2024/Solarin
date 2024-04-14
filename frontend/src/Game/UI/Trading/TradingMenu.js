import React, {useState} from "react";
import "./TradingMenu.css"
import WindowUI from "../WindowUI/WindowUI";

import ResourceFilter from "./ResourceFilter";


function TradingMenu(props) {

    const [selectedFilter, setSelectedFilter] = useState("");
    return (
      <WindowUI>
          {/*Creates the div that contains the chat menu*/}
      <div className="TradingMenuWidget absolute left-0">
            <ResourceFilter setSelectedFilter={setSelectedFilter}/>
            he
      </div>
      </WindowUI>
    )
}

export default TradingMenu