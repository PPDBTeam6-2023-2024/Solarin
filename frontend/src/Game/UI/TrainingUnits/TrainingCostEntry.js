import resourcesJson from "./../ResourceViewer/resources.json"

import './TrainingCostEntry.css'


function TrainingCostEntry(props) {

    return (
        <div className="TrainingCostEntry">

            <div style={{"height": "60%", "width": "60%", "margin": "auto"}}>
                <img src={(`/src/Game/Images/resources/${resourcesJson[props.resource]["icon"]}`)} draggable={false} alt={""}/>
            </div>

            <div style={{"fontSize": "150%", "justifyContent": "center", "alignItems": "center", "display": "flex"}}>
                {props.cost}
            </div>

        </div>
    )
}

export default TrainingCostEntry