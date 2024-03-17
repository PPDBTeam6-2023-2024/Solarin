import React, {useEffect, useState} from "react";
import chat_icon from "../../Images/icons/chat_icon.png";
import {TreeItem, TreeView} from "@mui/x-tree-view";
import Draggable from "react-draggable";
import "./ChatMenu.css"
import profile from "../../Images/profile_images/profile_1.png";
import axios from "axios";
import FriendOverviewEntry from "./Friends/FriendOverviewEntry";
import MessageBoard from "./MessageBoard";
import DmTab from "./DmTab";
const categories = ["Friends", "Alliances", "Ranking"]




const CategoryTab = (props) => {
    /**
     * create the visuals for the categories of the chat
     * */
    const [selectedCategory, setSelectedCategory] = props.selected
    let nav_bar_list = []

    /*
    * make a list of all the categories of the chat menu and give the selected menu a brighter color
    * */
    const selected_hex = "#FFFFFF";
    const not_selected_hex = "#868686";

    categories.forEach((elem) => {
      nav_bar_list.push(
          <>
              {selectedCategory === elem ? <li style={{"color": selected_hex}}>{elem}</li>:
                  <li style={{"color": not_selected_hex}} onClick={() => setSelectedCategory(elem)}>{elem}</li>
              }
          </>
      )
    })
    /**
     * return the small category bar at the top of the chat Menu
    * */
      return (
      <>
          <div className="ChatMenuWidgetBackground"></div>
        <nav className="ChatNavBar">
            <ul>
                {nav_bar_list}
            </ul>
        </nav>
      </>
      );
};




function ChatMenu(props) {

    const [selectedCategory, setSelectedCategory] = useState("Friends");
    return (
      <Draggable>
          {/*Creates the div that contains the chat menu*/}
      <div className="ChatMenuWidget absolute right-0">
          <CategoryTab selected={[selectedCategory, setSelectedCategory]}/>
          {selectedCategory === "Friends" && <DmTab></DmTab>}

      </div>
    </Draggable>
    )
}

export default ChatMenu