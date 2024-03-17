import React, {useEffect, useState} from "react";
import Draggable from "react-draggable";
import axios from "axios";
import './RequestEntry.css'

function RequestEntry(props) {
    /**
     * a template component for things like friend requests, alliance requests,...
     * */
    return (
      <>
          {/*Creates the div that contains the chat menu*/}
      <div className="transition ease-in-out" id={"RequestEntryVisual"} >
          <div style={{"width": "45%"}}>
              {props.text}
          </div>

          <button style={{"backgroundColor": "green"}} onClick={() => {props.on_true(); props.onEntryChose()}}>
              accept
          </button>
          <button style={{"backgroundColor": "red"}} onClick={() => {props.on_false(); props.onEntryChose()}}>
              reject
          </button>

      </div>
    </>
    )
}

export default FriendRequestEntry