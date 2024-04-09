import React, {useEffect, useState} from "react";
import './TrainingViewer.css'
import axios from "axios";
import TrainingQueueEntry from "./TrainingQueueEntry";
import TrainingOptionBar from "./TrainingOptionBar";
import {cos} from "three/examples/jsm/nodes/math/MathNode";

const getTrainingQueue = async(building_id) => {
    try {
        axios.defaults.headers.common = {'Authorization': `Bearer ${localStorage.getItem('access-token')}`}
        const response = await axios.get(`${process.env.REACT_APP_BACKEND_PATH}/building/training_queue/${building_id}`)
        return response.data
    }
    catch(e) {return []}
}

const addTrainingQueue = async(building_id, train_json) => {
    try {
        axios.defaults.headers.common = {'Authorization': `Bearer ${localStorage.getItem('access-token')}`}
        const response = await axios.post(`${process.env.REACT_APP_BACKEND_PATH}/unit/train/${building_id}`, train_json, {
              headers: {
                'content-type': 'application/json',
                'accept': 'application/json',
              },
            })

        return response.data
    }
    catch(e) {return []}
}

function TrainingViewer({building_id, onClose}) {

    const [trainingQueueList, setTrainingQueueList] = useState([])
    const scroll_bar = React.useRef(null);
    const [errorMessage, setErrorMessage] = useState("");

    async function addTrainingData(train_json) {
        let data = await addTrainingQueue(building_id, train_json)
        setTrainingQueueList(data["queue"]);
        if (!data["success"]){
            setErrorMessage(data["message"]);
        }else{
            setErrorMessage("");
        }
    }

    useEffect(() => {
        async function makeTrainingQueueOverview() {
            let data = await getTrainingQueue(building_id)
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


        const handleClickOutside = (event) => {
            if ((scroll_bar.current && !scroll_bar.current.contains(event.target)) && !event.target.closest('.TrainingOptionList')) {
                onClose();
            }
        };

        // Add and remove the event listener
        document.addEventListener('mousedown', handleClickOutside);
        return () => {
            document.removeEventListener('mousedown', handleClickOutside);
        };


    }, [scroll_bar]);


    return (
        <div className="TrainingViewScreen">
            {/*Displays the list of units that are currently  in the queue*/}
            <div  ref={scroll_bar} className="TrainingViewEntriesList">
                {trainingQueueList.map((queue_entry, index) => <TrainingQueueEntry OnTrainedFunction={
                async() => {
                    /*When a unit should be trained we recalibrate with the backend*/
                    let data = await getTrainingQueue(building_id);
                    setTrainingQueueList(data);

                    }
                } key={queue_entry.id+' '+queue_entry.r+' '+queue_entry.train_remaining} queue_data={queue_entry} index={index}/>)}

            </div>

            <TrainingOptionBar onTrain={(train_json) => addTrainingData(train_json)}/>
            {errorMessage}
        </div>
    )
}

export default TrainingViewer