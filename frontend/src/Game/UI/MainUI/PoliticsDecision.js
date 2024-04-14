import resourcesJson from "../ResourceViewer/resources.json"
import React from "react";

function PoliticsDecision() {
    /*THIS PAGE IS A MOCK PAGE AND NOT A FINISHED RESULT*/

    return (
        <div style={{"border": "0.4vw solid white", "width": "80%", "display": "inline-block"}}>
            <div style={{"width": "50%", "display": "inline-block"}}>
                <span style={{"color": "gold"}}>Offer citizens more food</span>

                <ul>
                    <li>Democratic: +3%</li>
                    <li>Religious: +8%</li>
                    <li>Authoritarian: -3%</li>
                    <li>Corporatism: -6%</li>
                </ul>

            </div>

            <div style={{"width": "30%", "display": "inline-block"}}>
                Costs 10
                <span style={{"width": "25%", "display": "inline-block"}}>
                    <img src={(`/images/resources/${resourcesJson["INF"]["icon"]}`)}
                                       alt={"INF"} draggable={false}/>
                </span>

                <button style={{"border": "0.2vw solid white", "borderRadius": "1vw 1vw 1vw 1vw"}}>Do Decision</button>
            </div>





        </div>


    )


}

export default PoliticsDecision;