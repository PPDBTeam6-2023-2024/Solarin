import React from "react";
import './TrainingOptionEntry.css'

function TrainingOptionEntry(props) {
    /*
    * In the training menu we can choose new units we want to train
    * This component will have the list of units we can train
    * */

    let styleAtt = {};
    if (props.select) {
        styleAtt = {"transform": "scale(110%)", "backgroundColor": "gold"}
    }

    return (
        <div className="TrainingOptionEntry" onClick={props.onSelect} style={styleAtt}>
            <img src={(`/images/troop_images/${props.image}`)} draggable={false} unselectable="on" alt={""}/>

        </div>
    )
}

export default TrainingOptionEntry