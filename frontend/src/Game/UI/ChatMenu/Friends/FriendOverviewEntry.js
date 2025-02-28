import React from "react";
import "./FriendOverviewEntry.css"


function FriendOverviewEntry(props) {
    /**
     * This component is 1 entry in the friend overview list
     * This component contains the username of the friend and the last message send between them
     * */

    return (
        <>
            {/*Creates the div that contains the chat menu*/}
            <div className="transition ease-in-out" id={"FriendOverviewEntryVisual"} onClick={props.onEntryClick}>
                <div style={{"width": "35%", "marginLeft": "5%"}}>
                    {props.user}
                </div>

                <div id={"FriendOverviewEntryMessage"} className="bg-gray-900"
                     style={{"width": "60%", "height": "100%"}}>
                    {props.message.body}

                </div>


            </div>
        </>
    )
}

export default FriendOverviewEntry