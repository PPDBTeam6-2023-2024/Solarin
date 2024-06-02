import resourcesJson from "./../ResourceViewer/resources.json"

import './TrainingCostEntry.css'



function TrainingCostEntry(props) {

    return (
        <div className="TrainingCostEntry">

            <div style={{"height": "50%", "width": "50%", "margin": "auto"}}>
                <img src={(`/images/resources/${resourcesJson[props.resource]["icon"]}`)} draggable={false} alt={""}/>
            </div>

            <div style={{"fontSize": "1.8vw", "justifyContent": "center", "alignItems": "center", "display": "flex", "paddingTop": "0.5vw"}}>
                {props.cost}
            </div>

        </div>
    )
}

export default TrainingCostEntry