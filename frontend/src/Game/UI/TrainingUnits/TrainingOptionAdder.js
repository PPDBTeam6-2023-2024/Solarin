import React, {useEffect, useRef, useState} from "react";
import './TrainingViewer.css'
import axios from "axios";
import './TrainingOptionBar.css'
import './TrainingOptionAdder.css'
import TrainingCostEntry from "./TrainingCostEntry";
import statJson from "../stats.json"

function TrainingOptionAdder(props) {
    /*
    * This menu will be used to submit the information about how many and which units we want to train
    * */

    /*This state takes the typecost into account so, it can display the cost before the user starts training*/
    const [typeCost, setTypeCost] = useState([]);
    const [troopStats, setTroopStats] = useState([])

    const getTypeCosts = async () => {
        try {
            const response = await axios.get(`${process.env.REACT_APP_BACKEND_PATH}/unit/train_cost/${props.type}/${props.buildingId}`)
            return response.data
        } catch (e) {
            return []
        }

    }
    useEffect(() => {
        const getTroopStats = async () => {
            try {
                const response = await axios.get(`${process.env.REACT_APP_BACKEND_PATH}/army/get_troop_stats/`);
                setTroopStats(response.data);
            } catch (e) {
                return []
            }
        }
        getTroopStats();
    }, []);

    useEffect(() => {
        async function getTrainingCost() {
            let data = await getTypeCosts()
            setTypeCost(data);
        }

        getTrainingCost()
    }, [props.type]);

    /*reference to the div that displays the resources needed for the upgrade*/
    const resourceBar = React.useRef(null);

    /*slider related states*/
    const [unitAmount, setUnitAmount] = useState(1);

    const onSliderChange = (e) => {
        setUnitAmount(e.target.value);
    };

    /*Put value in scrollbar*/
    useEffect(() => {
        sliderPos.current.style.left = (unitAmount * 78.5 / 100) + 5 + "%";
    }, [unitAmount]);

    /*
    * We want our number to follow the scrollbar, To do this we will move our text corresponding to the value
    * */
    const sliderRef = useRef(null);
    const sliderPos = useRef(null);

    const trainJson = () => {
        return JSON.stringify({
            "type": props.type,
            "amount": unitAmount
        })
    }

    return (
        <div className="TrainingOptionAdderWidget">
            <div ref={resourceBar} style={{
                "height": "40%",
                "display": "flex",
                "marginTop": "3%",
                "justifyContent": "center",
                "alignItems": "center"
            }}>
                {typeCost.map((value, index) => <TrainingCostEntry key={index} resource={value[0]}
                                                                   cost={value[1] * unitAmount}/>)}

            </div>

            <div style={{"position": "relative"}}>
                {troopStats[props.type] &&
                <div className={"troop-stats"}>
                    {troopStats[props.type].map(stat => (
                        <div key={stat.stat} className="stat-entry">
                            <img src={`/images/stats_icons/${statJson[stat.stat].icon}`}
                                 alt={stat}/>
                            {stat.stat !== "speed" ? <div>{stat.value*unitAmount}</div> :
                            <div>{stat.value}</div>}

                        </div>
                    ))}
                </div>
                }

            </div>


            <div style={{"position": "relative", "marginTop": "5%"}}>
                {/*This makes sure that our number follows the scroll bar*/}
                <span ref={sliderPos} style={{
                    "position": "absolute",
                    "left": "5%",
                    "fontSize": "1.3vw",
                    "userSelect": "none",
                    "pointerEvents": "none"
                }}>{unitAmount}</span>

                <input ref={sliderRef} className="TroopAmountSlider" type="range" min="1" max="100" value={unitAmount}
                       onInput={onSliderChange}/>

            </div>

            {/*button to train units*/}
            <div style={{"display": "flex", "justifyContent": "center", "alignItems": "center"}}>
                <button className="TrainButton" onClick={() => props.onTrain(trainJson())}> Train Units</button>
            </div>


        </div>
    )
}

export default TrainingOptionAdder