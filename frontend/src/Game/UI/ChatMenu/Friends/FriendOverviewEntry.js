import React, {useEffect, useState} from "react";
import Draggable from "react-draggable";
import "./FriendOverviewEntry.css"
function FriendOverviewEntry(props) {
    /**
     * This component is 1 entry in the friend overview list
     * This component contains the username of the friend and the last message send between them
     * */

    return (
      <>
          {/*Creates the div that contains the chat menu*/}
      <div className="transition ease-in-out" id={"FriendOverviewEntryVisual"}>
          <div style={{"width": "40%", "marginBottom": "5%"}}>
              {props.user}
          </div>

          <div id={"FriendOverviewEntryMessage"} className="bg-gray-900" style={{"width": "60%", "height": "100%"}}>
              {props.message.body}

          </div>


      </div>
    </>
    )
}

export default FriendOverviewEntry