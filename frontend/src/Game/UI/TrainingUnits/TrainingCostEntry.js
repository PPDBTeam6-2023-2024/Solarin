import resourcesJson from "./../ResourceViewer/resources.json"
import { useMemo } from "react";
import Tooltip from '@mui/material/Tooltip';
import WindowUI from "../WindowUI/WindowUI";

import './TrainingCostEntry.css'


function TrainingCostEntry(props) {

    return (
        <div className="TrainingCostEntry">

            <div style={{"height": "60%", "width": "60%", "margin":"auto"}}>
                <img src={(`/images/resources/${resourcesJson[props.resource]["icon"]}`)} draggable={false}/>
            </div>

            <div style={{"fontSize": "150%", "justifyContent": "center", "alignItems": "center", "display":"flex"}}>
                {props.cost}
            </div>

        </div>
    )
}
export default TrainingCostEntry