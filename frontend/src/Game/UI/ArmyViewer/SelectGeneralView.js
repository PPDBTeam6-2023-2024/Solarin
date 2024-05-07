import React, {useEffect, useState} from 'react';
import troopsJson from "./../troops.json"
import "./ArmyViewTroopEntry.css"
import Tooltip from "@mui/material/Tooltip";
import "./GeneralView.css"
import axios from "axios";
import GeneralListEntry from "./GeneralListEntry";


function SelectGeneralView({armyId, onChangeGeneral}) {
    /*Display the list of generals that can be assigned to this army*/

    const [generals, setGenerals] = useState([]);


    const getAvailableGenerals = async () => {
        /*get the generals available to be assigned to this army*/
        try {
            const response = await axios.get(`${process.env.REACT_APP_BACKEND_PATH}/general/available_generals`)
            setGenerals(response.data);
        } catch (e) {
            setGenerals([]);
        }
    }

    useEffect(() => {
        getAvailableGenerals()
    }, [])

    console.log(generals)
    return (
        <>
            {generals.map((general, index) => <GeneralListEntry key={general.name} generalInfo={general} armyId={armyId} onChangeGeneral={onChangeGeneral}/>)}

        </>

    );
}

export default SelectGeneralView;