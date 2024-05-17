import WindowUI from "../WindowUI/WindowUI"
import {useState} from "react";
import "./Settings.css"

function Settings(props) {
    return (
        <>
            {props.viewSettings &&
                <WindowUI>
                    <div className="SettingsMenu">
                        Settings Window
                    </div>
                </WindowUI>
            }
        </>
    )
}

export default Settings