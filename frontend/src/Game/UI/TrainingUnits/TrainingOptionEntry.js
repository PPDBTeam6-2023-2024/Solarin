import React, {useEffect, useState} from "react";
import './TrainingOptionEntry.css'

function TrainingOptionEntry(props) {
    /*
    * In the training menu we can choose new units we want to train
    * This component will have the list of units we can train
    * */

    return (
        <div className="TrainingOptionEntry" onClick={props.onSelect}>
            <img src={(`/images/troop_images/${props.image}`)} draggable={false}/>

        </div>
    )
}

export default TrainingOptionEntry