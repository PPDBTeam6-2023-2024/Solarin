import {useContext, useState} from "react"

import "../UI.css"
import "./Notification.css"
import WindowUI from "../WindowUI/WindowUI";


function Notification({own_target, other_target, won}) {
    /*
    * Display a short notification message
    * */
    console.log(own_target)
    return (
        <WindowUI>
            <div className="Notification">
                Combat Result
                <div>
                    {won ?
                    <span style={{"color": "green"}}>Victory</span >:
                    <span style={{"color": "red"}}>Defeat</span>
                    }

                </div>
                <div>
                    own <span>{own_target}</span> vs other <span>{other_target}</span>
                </div>

            </div>

        </WindowUI>


    )


}

export default Notification