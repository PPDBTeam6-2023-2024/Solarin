import {useState} from "react"
import SideMenu from "./SideMenu/SideMenu";
import ProfileButton from "./MainUI/ProfileButton";
import "./UI.css"
import ChatIcon from "./ChatMenu/ChatIcon";
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
    const [primaryColor, setPrimaryColor] = useState("#07cb61")
    const [secondaryColor, setSecondaryColor] = useState("#7715c7")

    console.log(getColorString(182, 179, 171, 255));
    return(

        <div className="UI" style={{'--primaryColor': primaryColor, '--secundaryColor': secondaryColor}}>

            {/*Load the side menu */}
            <SideMenu/>

            {/*Load Profile button with resource TAB*/}
            <ProfileButton/>

            {/*display chatIcon which can be clicked to open the chat menu*/}
            <ChatIcon/>

        </div>

    )


}

export default UI