import React, { useMemo } from 'react';
import { AgGridReact } from 'ag-grid-react';
import './NewBuildingGrid.css';
import {UpgradeButtonComponent} from "./Buttons";
import {getCityImage} from "../GetCityImage";
import ResourceCostEntry from "../../../UI/ResourceViewer/ResourceCostEntry";


const CityInfoGrid = ({ setBuildings, refreshResources,cityId, setUpgradeCostMap,upgradeCost, cityInfo, setCityInfo }) => {

    const RegionBuffsCellRenderer = ({ value }) => {
          return (
            <>{value.map((buff, index) => (
              <span key={index} style={{ color: buff.modifier >= 0 ? 'green' : 'red' }}>
                {buff.percentage} {buff.type}
              </span>
            )).reduce((prev, curr) => [prev, ', ', curr])}</> // This handles the comma separation properly in JSX
          );
        };


     const columns = useMemo(() => [
        { headerName: "Category", field: "category" },
        {
            headerName: "Information",
            field: "info",
            cellRenderer: (params) => {
                if (params.data.category === "Region buffs") {
                    return <RegionBuffsCellRenderer value={params.value} />;
                } else {
                    return <span>{params.value}</span>;
                }
            }
        }
    ], []);

    const rowData = useMemo(() => [
        // Example data preparation (similar to previous transformations)
        { category: "Region type", info: cityInfo.region_type , autoHeight: true},
        { category: "Region buffs", info: cityInfo.region_buffs.map(buff => ({
            type: buff[0],
            modifier: parseFloat(buff[1]) - 1,
            percentage: `${(parseFloat(buff[1]) - 1) >= 0 ? '+' : ''}${((parseFloat(buff[1]) - 1) * 100).toFixed(0)}%`
        })) , autoHeight: true, autoWidth: true},
        { category: "Population size", info: cityInfo.population , autoHeight: true},
    ], [cityInfo]);

    const onGridReady = (params) => {
        params.api.sizeColumnsToFit();
    };

    return (
        <>
            <div className={"FontSizer"} style={{"width": "50%", "display": "inline-block"}}>
                <div>
                    Region type: <span style={{"color": "gold"}}>{cityInfo.region_type}</span>
                </div>

                <div>
                    City Population: <span style={{"color": "gold"}}>{cityInfo.population}</span>
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
                <div className="building_image">
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

                    />
                }
            </div>
        </>
    );
};

export default CityInfoGrid;
