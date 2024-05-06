import React, {useState} from 'react';
import troopsJson from "./../troops.json"
import "./ArmyViewTroopEntry.css"
import Tooltip from "@mui/material/Tooltip";
import "./GeneralView.css"
import SelectGeneralView from "./SelectGeneralView";


function GeneralView(props) {
    /*Display the general that is part of the army*/

    const [generalSelectorMenu, setGeneralSelectorMenu] = useState(false);

    return (
        <>
            {!generalSelectorMenu &&
                <div className="GeneralWindow" onClick={() => {setGeneralSelectorMenu(true)}}>
                    <div style={{"width": "50%", "display": "inline-block"}}>
                    {/*Display the general*/}
                    <img src={(`/images/general_images/general01.png`)} draggable={false}
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
                <SelectGeneralView/>
            }

        </>

    );
}

export default GeneralView;