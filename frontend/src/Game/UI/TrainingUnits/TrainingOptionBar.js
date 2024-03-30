import React, {useEffect, useState} from "react";
import './TrainingViewer.css'
import axios from "axios";
import TrainingQueueEntry from "./TrainingQueueEntry";
import './TrainingOptionBar.css'
import TrainingOptionEntry from "./TrainingOptionEntry";
import troopsJson from "./../troops.json"
import TrainingOptionAdder from "./TrainingOptionAdder";
function TrainingOptionBar(props) {
    /*
    * In the training menu we can choose new units we want to train
    * This component will have the list of units we can train
    * */

    const [selected, setSelected] = useState(-1);

    return (
        <>
            <div className="TrainingOptionList">
            {Object.keys(troopsJson).map((key, index) => <TrainingOptionEntry key={index} type={key} image={troopsJson[key]["icon"]} onSelect={() => setSelected(index)}/>)}
            </div>
            {selected !== -1 && <TrainingOptionAdder/>}
        </>
    )
}

export default TrainingOptionBar