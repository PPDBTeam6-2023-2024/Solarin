import React, {useContext, useState} from "react";
import "./TradingMenu.css"
import WindowUI from "../WindowUI/WindowUI";

import ResourceFilter from "./ResourceFilter";
import {useSelector} from "react-redux";
import TradingOfferEntry from "./TradingOfferEntry";
import {UserInfoContext} from "../../Context/UserInfoContext";

function TradingMenu(props) {
    /*THIS MENU (and its components) IS PART OF A MOCK, AND IS NOT YET THE RESULTING REPRESENTATION*/
    const [selectedFilter, setSelectedFilter] = useState("");

    const [userInfo, setUserInfo] = useContext(UserInfoContext);
    console.log(userInfo)
    return (
      <WindowUI>

          {/*Creates the div that contains the chat menu*/}
          <div className="TradingMenuWidget absolute left-0">
                {userInfo.alliance ?
                    <>
                        <ResourceFilter filter={[selectedFilter, setSelectedFilter]}/>
                        {[["SOL", 1], ["TF", 1], ["SOL", 3]].map((value, index) =>
                            (<TradingOfferEntry give_resource={value[0]} receive_resource={"UR"}/>))}
                    </>:
                    <>
                        This feature becomes available when you join an alliance
                    </>
                }

          </div>



      </WindowUI>
    )
}

export default TradingMenu