import React, {useEffect, useState} from "react";
import Draggable from "react-draggable";
import './TrainingViewer.css'
import axios from "axios";
import Message from "../ChatMenu/Message";
import Troops from './../troops.json'
import './TrainingQueueEntry.css'


function TrainingQueueEntry(props) {

    const [remainingTime, setRemainingTime] = useState(new Date());

    useEffect(() => {
        var d = new Date()
        d.setSeconds(props.queue_data.train_remaining);
        setRemainingTime(d);

        setInterval(()=> {remainingTime.setSeconds(remainingTime.getSeconds()-2); setRemainingTime(remainingTime)}, 1000)
        }
    );

    return (
        <div className="TrainingQueueEntry">
            <img src={(`/images/troop_images/${Troops[props.queue_data.troop_type]["icon"]}`)} draggable={false}/>
            <div>
                <div  className="QueueLabel">
                    Type:
                </div>
                 {props.queue_data.troop_type}
            </div>
            <div>
                <div  className="QueueLabel">
                    Rank:
                </div>
                 {props.queue_data.rank}
            </div>
            <div>
                <div  className="QueueLabel">
                    Remaining Time:
                </div>
                {remainingTime.toLocaleTimeString()}
            </div>
        </div>
    )
}

export default TrainingQueueEntry