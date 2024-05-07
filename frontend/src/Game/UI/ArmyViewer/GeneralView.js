import React, {useState} from 'react';
import troopsJson from "./../troops.json"
import "./ArmyViewTroopEntry.css"
import Tooltip from "@mui/material/Tooltip";
import "./GeneralView.css"
import SelectGeneralView from "./SelectGeneralView";
import generalsJson from "./generals.json"
import axios from "axios";

function GeneralView({armyId, generalInfo, onChangeGeneral}) {
    /*Display the general that is part of the army*/

    const [generalSelectorMenu, setGeneralSelectorMenu] = useState(false);

    const addGenerals = async (armyId, generalName) => {
        /*Add a general to the army*/
        const response = await axios.post(`${process.env.REACT_APP_BACKEND_PATH}/general/add_general`,
            JSON.stringify({
                "army_id": armyId,
                "general_name": generalName
            }),
            {
                headers: {
                    'content-type': 'application/json',
                    'accept': 'application/json',
                },
            }
        )

        /*Close the select general menu*/
        setGeneralSelectorMenu(false);

        /*Propagate change of general to parent*/
        onChangeGeneral();
    }

    return (
        <>
            {!generalSelectorMenu &&
                <div className="GeneralWindow" onClick={() => {setGeneralSelectorMenu(true)}}>
                    <div style={{"width": "50%", "display": "inline-block"}}>
                    {/*Display the general*/}
                    <img src={(`/images/general_images/${generalsJson[generalInfo.name]["icon"]}`)} draggable={false}
                     unselectable="on"/>
                    </div>
                    <div>
                        attack: <span style={{"color": "green"}}>+5%</span>
                    </div>
                    <div>
                        city defense: <span style={{"color": "green"}}>+11%</span>
                    </div>
                </div>
            }

            {generalSelectorMenu &&
                <SelectGeneralView armyId={armyId} onChangeGeneral={addGenerals}/>
            }

        </>

    );
}

export default GeneralView;