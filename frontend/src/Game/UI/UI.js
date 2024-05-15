import {useContext, useState} from "react"
import SideMenu from "./SideMenu/SideMenu";
import ProfileButton from "./ProfileViewer/ProfileButton";
import "./UI.css"
import ChatIcon from "./ChatMenu/ChatIcon";
import HiddenWindowsViewer from "./HiddenWIndowsViewer/HIddenWIndowsViewer";
import TradingIcon from "./Trading/TradingIcon";
import Settings from "./Settings/Settings";
//component that contains all the UI components
import {PrimaryContext, SecondaryContext, TertiaryContext} from "../Context/ThemeContext";
const getColorString = (r, g, b, a) => {
    /**
     * Convert rgba to its corresponding hex
     * */
    return `#${r.toString(16)}${g.toString(16)}${b.toString(16)}${a.toString(16)}`;

}

function UI() {

    /**
     * these 2 states exist to be able to change the UI colors
     * */
    const [primaryColor, setPrimaryColor] = useContext(PrimaryContext);
    const [secondaryColor, setSecondaryColor] = useContext(SecondaryContext);
    const [tertiaryColor, setTertiaryColor] = useContext(TertiaryContext);
    return (

        <div className="UI" style={
            {
                '--primaryColor': primaryColor,
                '--secundaryColor': secondaryColor,
                "--tertiaryColor": tertiaryColor
            }}>

            {/*load hidden windows viewer */}
            <HiddenWindowsViewer/>

            {/*Load the side menu */}
            <SideMenu/>

            {/*Load Profile button with resource TAB*/}
            <ProfileButton/>

            {/*display chatIcon which can be clicked to open the chat menu*/}
            <ChatIcon/>

            {/*display tradingIcon which can be clicked to open the trading menu*/}
            <TradingIcon/>


        </div>

    )


}

export default UI