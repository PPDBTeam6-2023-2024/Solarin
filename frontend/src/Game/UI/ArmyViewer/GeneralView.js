import React, {useState} from 'react';
import troopsJson from "./../troops.json"
import "./ArmyViewTroopEntry.css"
import Tooltip from "@mui/material/Tooltip";
import "./GeneralView.css"
import SelectGeneralView from "./SelectGeneralView";
import generalsJson from "./generals.json"
import axios from "axios";
import GeneralViewStatEntry from "./GeneralViewStats";

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
                    {generalInfo !== null &&
                        <img src={(`/images/general_images/${generalsJson[generalInfo.general_data.name]["icon"]}`)}
                             draggable={false}
                             unselectable="on"/>
                    }
                    {generalInfo === null &&
                        <div>
                            Click here to add a General
                        </div>
                    }

                    </div>
                    {generalInfo.modifiers.map((modifier, index) =>
                        <div>
                            <GeneralViewStatEntry key={index} stat_name={modifier.stat} stat_value={modifier.modifier}
                            political_stat_name={modifier.political_stance}
                            political_stat_value={modifier.political_stance_modifier}/>
                        </div>
                    )}

                </div>
            }

            {generalSelectorMenu &&
                <SelectGeneralView armyId={armyId} onChangeGeneral={addGenerals}/>
            }

        </>

    );
}

export default GeneralView;