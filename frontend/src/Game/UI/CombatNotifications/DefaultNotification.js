import {useContext, useState} from "react"

import "../UI.css"
import "./Notification.css"
import WindowUI from "../WindowUI/WindowUI";


function DefaultNotification({text}) {
    /**
    * Display a short notification message
    * */
    return (
        <WindowUI>
            <div className="Notification">
                {text}

            </div>

        </WindowUI>


    )


}

export default DefaultNotification