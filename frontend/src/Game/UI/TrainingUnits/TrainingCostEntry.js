import resourcesJson from "./../ResourceViewer/resources.json"

import './TrainingCostEntry.css'
import {useSelector} from "react-redux";


function TrainingCostEntry(props) {
    const resources = useSelector((state) => state.resources.resources)

    return (
        <div className="TrainingCostEntry">

            <div style={{"height": "50%", "width": "50%", "margin": "auto"}}>
                <img src={(`/images/resources/${resourcesJson[props.resource]["icon"]}`)} draggable={false} alt={""}/>
            </div>

            <div style={{"fontSize": "1.8vw", "justifyContent": "center", "alignItems": "center", "display": "flex", "paddingTop": "0.5vw"}}>
                {Math.min(props.cost, resources[props.resource])}
            </div>

        </div>
    )
}

export default TrainingCostEntry