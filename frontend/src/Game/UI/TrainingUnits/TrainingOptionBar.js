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

    const [selected, setSelected] = useState("");

    const changeSelected = (key) => {if (selected === key){setSelected(-1)}else{setSelected(key)}}

    return (
        <>
            <div className="TrainingOptionList">
            {Object.keys(troopsJson).map((key, index) =>


                <>
                  {selected === key?
                    <TrainingOptionEntry key={index} type={key} image={troopsJson[key]["icon"]} selected={true} onSelect={() => changeSelected(key)}/>:
                    <TrainingOptionEntry key={index} type={key} image={troopsJson[key]["icon"]} selected={false} onSelect={() => changeSelected(key)}/>
                    }
                </>

                )
            }
            </div>
            {selected !== "" && <TrainingOptionAdder/>}
        </>
    )
}

export default TrainingOptionBar