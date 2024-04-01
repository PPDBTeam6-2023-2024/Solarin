import React, {useEffect, useState} from "react";
import './TrainingViewer.css'
import axios from "axios";
import Message from "../ChatMenu/Message";
import Troops from './../troops.json'
import './TrainingQueueEntry.css'


function TrainingQueueEntry(props) {

    const remaining_timer = React.useRef(null);
    useEffect(() => {
        /*
        * We make sure that their is a
        * */
        var d = new Date(props.queue_data.train_remaining*1000);

        remaining_timer.current.innerText = d.toLocaleTimeString();

        if (props.index !== 0){
            return
        }
        var time_till_troop_trained = (props.queue_data.troop_size-1)*props.queue_data.unit_training_time;

        var interval = setInterval(() => {
            d.setSeconds(d.getSeconds() - 1);
            remaining_timer.current.innerText = d.toLocaleTimeString();

            /*Call the OnTrainedFunction when 1 unit is trained*/
            if (d.getTime() / 1000 <= time_till_troop_trained){
                props.OnTrainedFunction()

            }

        }, 1000)

        return () => {
            clearInterval(interval);
        };
    }, []);

    return (
        <div className="TrainingQueueEntry">
            <div className="TrainingQueueImageWrapper">
                <img src={(`/images/troop_images/${Troops[props.queue_data.troop_type]["icon"]}`)} draggable={false}/>
            </div>


            {/*this div makes it possible to do horizontal scrolling among the units*/}
            <div className="TrainingQueueStats">
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
                        Training Size:
                    </div>
                     {props.queue_data.troop_size}
                </div>

                <div>
                    <div  className="QueueLabel">
                        Remaining Time:
                    </div>

                    {/*this dict its value will be dynamically display the remaining time*/}
                    <div ref={remaining_timer}/>

                </div>


            </div>

        </div>
    )
}

export default TrainingQueueEntry