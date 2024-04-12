import React from "react";
import axios from "axios";
import './RequestEntry.css'

function RequestEntry(props) {
    /**
     * a template component for things like friend requests, alliance requests,...
     * */
    return (
        <>
            {/*Creates the div that contains the chat menu*/}
            <div className="transition ease-in-out" id={"RequestEntryVisual"}>
                <div style={{"width": "45%"}}>
                    {props.text}
                </div>

                <button style={{"backgroundColor": "green"}} onClick={props.onTrue}>
                    accept
                </button>
                <button style={{"backgroundColor": "red"}} onClick={props.onFalse}>
                    reject
                </button>

            </div>
        </>
    )
}

export default RequestEntry