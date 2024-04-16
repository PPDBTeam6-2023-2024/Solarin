import React, {useEffect} from "react";
import './TrainingViewer.css'
import Troops from './../troops.json'
import './TrainingQueueEntry.css'


function TrainingQueueEntry(props) {

    const remainingTimer = React.useRef(null);
    useEffect(() => {

        var d = props.queueData.train_remaining

        remainingTimer.current.innerText = `${Math.floor(d / 3600)}H ${Math.floor((d % 3600) / 60)}M ${d % 60}S`;

        if (props.index !== 0) {
            return
        }
        var timeTillTroopTrained = (props.queueData.troop_size - 1) * props.queueData.unit_training_time;

        var interval = setInterval(() => {
            d -= 1;
            remainingTimer.current.innerText = `${Math.floor(d / 3600)}H ${Math.floor((d % 3600) / 60)}M ${d % 60}S`;
            /*Call the OnTrainedFunction when 1 unit is trained*/
            if (d <= timeTillTroopTrained) {
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
                <img src={(`/images/troop_images/${Troops[props.queueData.troop_type]["icon"]}`)} draggable={false} alt={""}/>
            </div>


            {/*this div makes it possible to do horizontal scrolling among the units*/}
            <div className="TrainingQueueStats">
                <div>
                    <div className="QueueLabel">
                        Type:
                    </div>
                    {props.queueData.troop_type}
                </div>
                <div>
                    <div className="QueueLabel">
                        Rank:
                    </div>
                    {props.queueData.rank}
                </div>

                <div>
                    <div className="QueueLabel">
                        Training Size:
                    </div>
                    {props.queueData.troop_size}
                </div>

                <div>
                    <div className="QueueLabel">
                        Remaining Time:
                    </div>

                    {/*the value of this dict will dynamically display the remaining time*/}
                    <div ref={remainingTimer}/>

                </div>


            </div>

        </div>
    )
}

export default TrainingQueueEntry