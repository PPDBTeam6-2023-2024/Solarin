import React, {useEffect, useState} from "react";
import Draggable from "react-draggable";
import './TrainingViewer.css'
import axios from "axios";
import TrainingQueueEntry from "./TrainingQueueEntry";


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

    useEffect(() => {
        async function makeTrainingQueueOverview() {
            let data = await getTrainingQueue()
            setTrainingQueueList(data);
        }
        makeTrainingQueueOverview()
    }, [])



    return (
        <div className="TrainingViewScreen">
            {trainingQueueList.map((queue_entry, index) => <TrainingQueueEntry key={index} queue_data={queue_entry}/>)}
        </div>
    )
}

export default TrainingViewer