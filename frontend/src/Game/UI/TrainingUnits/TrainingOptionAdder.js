import React, {useEffect, useState} from "react";
import './TrainingViewer.css'
import axios from "axios";
import TrainingQueueEntry from "./TrainingQueueEntry";
import './TrainingOptionBar.css'
import TrainingOptionEntry from "./TrainingOptionEntry";
import troopsJson from "./../troops.json"
import './TrainingOptionAdder.css'
function TrainingOptionAdder(props) {
    /*
    * This menu will be used to submit the information about how many and which units we want to train
    * */

    const getTypeCosts = async() => {
    try {
        axios.defaults.headers.common = {'Authorization': `Bearer ${localStorage.getItem('access-token')}`}
        const response = await axios.get(`${process.env.REACT_APP_BACKEND_PATH}/chat/dm_overview`)
        return response.data
    }
    catch(e) {return []}
}

    return (
        <div className="TrainingOptionAdderWidget">lala</div>
    )
}

export default TrainingOptionAdder