import React, {useEffect, useState} from "react";
import './TrainingViewer.css'
import axios from "axios";
import TrainingQueueEntry from "./TrainingQueueEntry";
import TrainingOptionBar from "./TrainingOptionBar";
import {cos} from "three/examples/jsm/nodes/math/MathNode";

const getTrainingQueue = async (building_id) => {
    try {
        axios.defaults.headers.common = {'Authorization': `Bearer ${localStorage.getItem('access-token')}`}
        const response = await axios.get(`${process.env.REACT_APP_BACKEND_PATH}/building/training_queue/${building_id}`)
        return response.data
    }
    catch(e) {return []}
}

const addTrainingQueue = async (buildingId, trainJson) => {
    try {
        axios.defaults.headers.common = {'Authorization': `Bearer ${localStorage.getItem('access-token')}`}
        const response = await axios.post(`${process.env.REACT_APP_BACKEND_PATH}/unit/train/${buildingId}`, trainJson, {
            headers: {
                'content-type': 'application/json',
                'accept': 'application/json',
            },
        })

        return response.data
    }
    catch(e) {return []}
}

function TrainingViewer({buildingId, onClose, refreshResources}) {
    const [trainingQueueList, setTrainingQueueList] = useState([])
    const scrollBar = React.useRef(null);
    const [errorMessage, setErrorMessage] = useState("");

    async function addTrainingData(train_json) {
        let data = await addTrainingQueue(buildingId, train_json)
        setTrainingQueueList(data["queue"]);
        refreshResources()
        if (!data["success"]) {
            setErrorMessage(data["message"]);
        } else {
            setErrorMessage("");
        }
    }

    useEffect(() => {
        async function makeTrainingQueueOverview() {
            let data = await getTrainingQueue(buildingId)
            setTrainingQueueList(data);
        }

        makeTrainingQueueOverview()
    }, [])

    /*
    * The effect below makes it possible to horizontally scroll
    * and see the enter training queue
    * */
    useEffect(() => {
        if (scrollBar.current === null) {
            return;
        }

        //support horizontal scrolling
        scrollBar.current?.addEventListener("wheel", (evt) => {
            evt.preventDefault();
            scrollBar.current.scrollLeft += evt.deltaY;
        });

        /* Calls onClose() when user clicks outside TrainingViewScreen */
        const handleClickOutside = (event) => {
            if (!event.target.closest('.TrainingViewScreen')) {
                onClose();
            }
        };

        // Add and remove the event listener
        document.addEventListener('mousedown', handleClickOutside);
        return () => {
            document.removeEventListener('mousedown', handleClickOutside);
        };


    }, [scrollBar]);


    return (
        <div className="TrainingViewScreen">
            {/*Displays the list of units that are currently  in the queue*/}
            <div ref={scrollBar} className="TrainingViewEntriesList">
                {trainingQueueList.map((queueEntry, index) => <TrainingQueueEntry OnTrainedFunction={
                async() => {
                    /*When a unit should be trained we recalibrate with the backend*/
                    let data = await getTrainingQueue(buildingId);
                    setTrainingQueueList(data);

                    }
                } key={queueEntry.id + ' ' + queueEntry.r + ' ' + queueEntry.train_remaining}
                                                                                   queueData={queueEntry}
                                                                                   index={index}/>)}

            </div>

            <TrainingOptionBar onTrain={(trainJson) => addTrainingData(trainJson)}/>
            {errorMessage}
        </div>
    )
}

export default TrainingViewer