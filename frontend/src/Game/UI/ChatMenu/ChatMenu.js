import React, {useEffect, useState} from "react";
import chat_icon from "../../Images/icons/chat_icon.png";
import {TreeItem, TreeView} from "@mui/x-tree-view";
import Draggable from "react-draggable";
import "./ChatMenu.css"
import profile from "../../Images/profile_images/profile_1.png";
import axios from "axios";
import FriendOverviewEntry from "./Friends/FriendOverviewEntry";
import MessageBoard from "./MessageBoard";

const categories = ["Friends", "Alliances", "Ranking"]


const getDMOverview = async() => {
    try {
        //const socket = new WebSocket(`ws://${process.env.REACT_APP_BACKEND_PATH}/chat/dm_overview`)

        axios.defaults.headers.common = {'Authorization': `Bearer ${localStorage.getItem('access-token')}`}
        const response = await axios.get(`${process.env.REACT_APP_BACKEND_PATH}/chat/dm_overview`)
        return response.data
    }
    catch(e) {return false}
}

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


const DmTab = (props) => {
    const [dmData, setDmData] = useState([])
    const [dmIndex, setDmIndex] = useState(-1)

    //syntax is not great, but apparently the proper way to retrieve async information from a sync function
    //This function reads the data from the RESTAPI request, and will use its data to amek  the DMOverview


    useEffect(() => {
        async function makeOverviewEntries() {
            let data = await getDMOverview()
            setDmData(data)
        }
        makeOverviewEntries()
    }, [])


    return (
        <>
            {dmIndex === -1 && <div style={{"overflow-y": "scroll", "height":"85%", "scrollbar-width:": "none"}}>
                <div>{
                    /*display al the friend overview entries we jsut retrieved*/
                    dmData.map((elem, index) => <FriendOverviewEntry user={elem[0]} message={elem[1]} key={index} onEntryClick={() => setDmIndex(index)}></FriendOverviewEntry>)
                }</div>

            </div>}
            {/*Open a component for the dm between the 2 users that were just selected*/}
            {dmIndex !== -1 && <MessageBoard message_board={dmData.slice(dmIndex , dmIndex+1)[0][2]}/>}
        </>


    )
}

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