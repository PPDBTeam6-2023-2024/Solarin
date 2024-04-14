import {useState} from "react"
import SideMenu from "./SideMenu/SideMenu";
import ProfileButton from "./MainUI/ProfileButton";
import "./UI.css"
import ChatIcon from "./ChatMenu/ChatIcon";
import HiddenWindowsViewer from "./HiddenWIndowsViewer/HIddenWIndowsViewer";
import TradingIcon from "./Trading/TradingIcon";
//component that contains all the UI components

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
    const [primaryColor, setPrimaryColor] = useState("#ce1c75")
    const [secondaryColor, setSecondaryColor] = useState("#d57d11")
    const [tertiaryColor, setTertiaryColor] = useState("#e1b812")
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