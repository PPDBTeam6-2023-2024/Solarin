import React, {useEffect, useState, useContext} from "react";
import "../Alliance/AllianceTab.css"
import "../Requests/RequestButtons.css"
import axios from "axios";
import './RankingEntry.css'

const RankingEntry = (props) => {


    return (
        <div className="RankingEntry">
            <div style={{"width": "20%"}}>
                {props.index}
            </div>

            <div style={{"width": "50%"}}>
                {props.user}
            </div>

            <div style={{"width": "30%"}}>
                {props.quantity}
            </div>

        </div>
    )
}

export default RankingEntry