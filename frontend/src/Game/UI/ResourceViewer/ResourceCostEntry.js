import resourcesJson from "./../ResourceViewer/resources.json"

import './ResourceCostEntry.css'
import Tooltip from "@mui/material/Tooltip";


function ResourceCostEntry(props) {

    let color = "green";
    if (props.cost < 0){
        color = "red"
    }

    return (
        <Tooltip title={`${resourcesJson[props.resource]["description"]}`}>
        <div className="ResourceCostEntry" style={{"display": "inline-block"}}>

            <div style={{"height": "60%", "width": "60%", "margin": "auto"}}>
                <img src={(`/images/resources/${resourcesJson[props.resource]["icon"]}`)} draggable={false} alt={""}/>
            </div>

            <div style={{"fontSize": "100%", "justifyContent": "center", "alignItems": "center", "display": "flex"}}>
                {props.percentage &&
                    <span style={{"color": color}}>
                        {parseFloat(props.cost).toFixed(2)*100}%
                    </span>
                }
                {!props.percentage &&
                    <span>
                        {props.cost}
                    </span>
                }

            </div>

        </div>
        </Tooltip>
    )
}

export default ResourceCostEntry