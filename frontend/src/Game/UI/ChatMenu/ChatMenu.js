import React, {useContext, useState} from "react";
import "./ChatMenu.css"
import FriendsTab from "./Friends/FriendsTab";
import AllianceTab from "./Alliance/AllianceTab";
import RankingTab from "./Ranking/RankingTab";
import WindowUI from "../WindowUI/WindowUI";
import {PrimaryContext, TextColorContext} from "../../Context/ThemeContext";


const categories = ["Friends", "Alliances", "Ranking"]

const CategoryTab = (props) => {
    /**
     * create the visuals for the categories of the chat
     * */
    const [selectedCategory, setSelectedCategory] = props.selected
    let navBarList = []

    /*
    * make a list of all the categories of the chat menu and give the selected menu a brighter color
    * */

    const [textColor, setTextColor] = useContext(TextColorContext);
    const notSelectedHex = "#868686";

    categories.forEach((elem) => {
        navBarList.push(
            <>
                {selectedCategory === elem ? <li style={{"color": textColor}}>{elem}</li> :
                    <li key={elem} style={{"color": notSelectedHex}}
                        onClick={() => setSelectedCategory(elem)}>{elem}</li>
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
                    {navBarList}
                </ul>
            </nav>
        </>
    );
};


function ChatMenu(props) {

    const [selectedCategory, setSelectedCategory] = useState("Friends");
    return (
        <WindowUI>
            {/*Creates the div that contains the chat menu*/}
            <div className="ChatMenuWidget absolute right-0">
                <CategoryTab selected={[selectedCategory, setSelectedCategory]}/>
                {selectedCategory === "Friends" && <FriendsTab/>}
                {selectedCategory === "Alliances" && <AllianceTab/>}
                {selectedCategory === "Ranking" && <RankingTab/>}
            </div>
        </WindowUI>
    )
}

export default ChatMenu