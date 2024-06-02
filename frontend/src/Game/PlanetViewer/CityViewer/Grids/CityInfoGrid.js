import React, {useEffect, useContext, useMemo, useState} from 'react';
import {AgGridReact} from 'ag-grid-react';
import './NewBuildingGrid.css';
import {UpgradeButtonComponent} from "./Buttons";
import {getCityImage} from "../GetCityImage";
import axios from "axios";
import statsJson from "../../../UI/stats.json";
import ResourceCostEntry from "../../../UI/ResourceViewer/ResourceCostEntry";
import {TertiaryContext, TextColorContext} from "../../../Context/ThemeContext";
const CityInfoGrid = ({setBuildings, refreshResources, cityId, setUpgradeCostMap, upgradeCost, cityInfo, setCityInfo, timer, setTimer}) => {
    /**
     * This component visualizes the city manager menu when you select the 'City' tab
     * */
    const [cityStats, setCityStats] = useState(null)

    /*
    * Load the city combat stats
    * */
    const fetchStats = async () => {
        try {
            const response = await axios.get(`${process.env.REACT_APP_BACKEND_PATH}/cityManager/get_stats/${cityId}`);
            setCityStats(response.data);
        } catch (error) {
            console.error('Error while fetching city combat stats:', error);
        }
    };

    useEffect(() => {
        fetchStats();
    }, [])

    /*
    * Make textcolor depend on theme
    * */
    const [textColor, setTextColor] = useContext(TextColorContext);

    return (
        <>
            <div className={"FontSizer"} style={{"width": "50%", "display": "inline-block"}}>
                <div>
                    Region type: <span style={{"color": textColor}}>{cityInfo.region_type}</span>
                </div>

                <div>
                    City Population: <span style={{"color": textColor}}>{cityInfo.population}</span>
                </div>

                {/*Div to display the Region buffs*/}
                <div>
                    <h2>Region Buffs</h2>
                    <div style={{"display": "flex", "flexDirection": "row", "alignItems": "center",
                        "justifyContent": "center", "overflow": "scroll"}}>
                        {cityInfo.region_buffs.map((element) => <ResourceCostEntry resource={element[0]}
                                                                               cost={element[1]-1}
                                                                               percentage={true}/>)}
                    </div>

                </div>

                {/*Div to display the City Maintenance*/}
                <div>
                    <h2>City Maintenance Cost /hour</h2>
                    <div style={{"display": "flex", "flexDirection": "row", "alignItems": "center",
                        "justifyContent": "center", "overflow": "scroll"}}>
                        {cityInfo.maintenance_cost.map((element, index) => <ResourceCostEntry resource={element[0]}
                                                                                          cost={element[1]}
                                                                                          percentage={false}/>)}
                    </div>

                </div>


            </div>

            <div className="right-screen-city-info">
                {cityStats &&
                    <div style={{"display": "flex", "flexDirection": "row", "marginTop": "0.5vw", "rowGap": "0.5vw"}}>
                        {/*Display the combat stats of a city*/}
                        <div className={"building-stats"}>
                            <img src={`/images/stats_icons/${statsJson.attack.icon}`} alt={"attack"}/>
                            <div>{Math.round(cityStats["attack"])}</div>
                        </div>
                        <div className={"building-stats"}>
                            <img src={`/images/stats_icons/${statsJson.defense.icon}`} alt={"defense"}/>
                            <div>{Math.round(cityStats["defense"])}</div>
                        </div>
                    </div>
                }
                <div className="building_image" style={{"marginBottom": "5vw"}}>
                    {/*Display an image of the city*/}
                    <img src={getCityImage(cityInfo?.rank)} alt="City" className="selected-image shadow-2xl"/>
                </div>

                { <UpgradeButtonComponent
                                            data = {cityInfo}
                                            cityId={cityId}
                                            upgradeCost={upgradeCost}
                                            setUpgradeCostMap={setUpgradeCostMap}
                                            refreshResources={refreshResources}
                                            setBuildings={setBuildings}
                                            cityUpgradeBool={true}
                                            setCityInfo={setCityInfo}
                                            totalTimePassed={timer}
                                            setTotalTimePassed={setTimer}

                    />
                }
            </div>
        </>
    );
};

export default CityInfoGrid;
