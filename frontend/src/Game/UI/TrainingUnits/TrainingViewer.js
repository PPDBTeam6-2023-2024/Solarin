import React, {useEffect, useState} from "react";
import './TrainingViewer.css'
import axios from "axios";
import TrainingQueueEntry from "./TrainingQueueEntry";
import TrainingOptionBar from "./TrainingOptionBar";

const getTrainingQueue = async() => {
    try {
        axios.defaults.headers.common = {'Authorization': `Bearer ${localStorage.getItem('access-token')}`}
        const response = await axios.get(`${process.env.REACT_APP_BACKEND_PATH}/building/training_queue/2`)
        return response.data
    }
    catch(e) {return []}
}

function TrainingViewer(props) {



    const [trainingQueueList, setTrainingQueueList] = useState([])
    const scroll_bar = React.useRef(null);



    useEffect(() => {
        async function makeTrainingQueueOverview() {
            let data = await getTrainingQueue()
            setTrainingQueueList(data);
        }

        makeTrainingQueueOverview()
    }, [])

    /*
    * The effect below makes it possible to horizontally scroll
    * and see the the enter training queue
    * */
    useEffect(() => {
        if (scroll_bar.current === null) {return;}

        //support horizontal scrolling
        scroll_bar.current?.addEventListener("wheel", (evt) => {
            evt.preventDefault();
            scroll_bar.current.scrollLeft += evt.deltaY;
        });


    }, [scroll_bar]);




    return (
        <div className="TrainingViewScreen">
            {/*Displays the list of units that are currently  in the queue*/}
            <div  ref={scroll_bar} className="TrainingViewEntriesList">
                {trainingQueueList.map((queue_entry, index) => <TrainingQueueEntry OnTrainedFunction={
                async() => {
                    /*When a unit should be trained we recalibrate with the backend*/
                    let data = await getTrainingQueue();
                    setTrainingQueueList(data);

                    }
                } key={queue_entry.id+' '+queue_entry.r+' '+queue_entry.train_remaining} queue_data={queue_entry} index={index}/>)}

            </div>
            <TrainingOptionBar/>
        </div>
    )
}

export default TrainingViewer