import React from 'react';
import decisionsData from '../decisions.json';  // Importing the decisions JSON
import resourcesJson from "../ResourceViewer/resources.json";

function PoliticsDecision({ updateStance }) {
    return (
        <div style={{"border": "0.4vw solid white", "width": "80%", "display": "block"}}>
            {decisionsData.decisions.map((decision, index) => (
                <div key={index} style={{"marginBottom": "2vw", "display": "inline-block", "width": "100%"}}>
                    <div style={{"width": "50%", "display": "inline-block"}}>
                        <span style={{"color": "gold"}}>{decision.title}</span>
                        <ul>
                            {Object.entries(decision.impacts).map(([govType, impact], idx) => (
                                <li key={idx}>{govType.replace(/_/g, '').replace(/([A-Z])/g, ' $1').trim()}: {impact}</li>
                            ))}
                        </ul>
                    </div>
                    <div style={{"width": "30%", "display": "inline-block"}}>
                        {Object.entries(decision.cost).map(([resource, amount], idx) => (
                            <span key={idx} style={{"display": "flex", "alignItems": "center", "marginBottom": "5px"}}>
                                <img src={`/images/resources/${resourcesJson[resource].icon}`} alt={resource} style={{"width": "40px", "marginRight": "10px"}}/>
                                {amount}
                            </span>
                        ))}
                        <button
                            onClick={() => updateStance(decision.impacts, decision.cost)}
                            style={{"border": "0.2vw solid white", "borderRadius": "1vw 1vw 1vw 1vw"}}>
                            Do Decision
                        </button>
                    </div>
                </div>
            ))}
        </div>
    );
}

export default PoliticsDecision;
