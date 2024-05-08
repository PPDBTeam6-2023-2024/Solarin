import React from 'react';
import statsJson from "./../stats.json"
import Tooltip from "@mui/material/Tooltip";

function GeneralViewStatEntry(props) {

    /*This component represents a stat entry in the details of an army*/

    const value = Math.round(props.stat_value*100)
    let color = "white";
    if (value > 0){
        color = "green";
    }else if (value < 0){
        color = "red";
    }

    const political_value = Math.round(props.political_stat_value*100)
    let political_color = "white";
    if (political_value > 0){
        political_color = "green";
    }else if (political_value < 0){
        political_color = "red";
    }

    return (
        <div style={{"width": "100%", "marginTop": "0.3vw"}}>
            <div style={{"width": "20%", "display": "inline-block"}}>
                <Tooltip title={`${props.stat_name}`}>
                    <img src={(`/images/stats_icons/${statsJson[props.stat_name]["icon"]}`)} draggable={false}
                         unselectable="on"
                         alt=""
                    />
                </Tooltip>
            </div>

            <Tooltip title={`${value}% ${props.stat_name} bonus`}>
            <div style={{"width": "30%", "display": "inline-block", "textAlign": "right",
                "fontSize": "150%", "color": color}}>
                {value}%
            </div>
            </Tooltip>

            <Tooltip title={`${political_value}% ${props.political_stat_name} bonus`}>
            <div style={{"width": "30%", "display": "inline-block", "textAlign": "right",
                "fontSize": "150%", "color": political_color}}>
                {political_value}%
            </div>
            </Tooltip>
        </div>
    );
}

export default GeneralViewStatEntry;