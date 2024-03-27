import React, {useEffect, useState} from "react";
import Draggable from "react-draggable";
import './TrainingViewer.css'
import axios from "axios";


const getTrainingQueue = async() => {
    try {
        axios.defaults.headers.common = {'Authorization': `Bearer ${localStorage.getItem('access-token')}`}
        const response = await axios.get(`${process.env.REACT_APP_BACKEND_PATH}/building/training_queue/2`)
        return response.data
    }
    catch(e) {return []}
}

function TrainingViewer(props) {

    useEffect(() => {
        async function makeTrainingQueueOverview() {
            let data = await getTrainingQueue()
            setDmData(data)

            data = await getFriendRequests()
            setFriendRequests(data)
        }
        makeOverviewEntries()
    }, [])



    return (
        <div className="TrainingViewScreen">

        </div>
    )
}

export default TrainingViewer