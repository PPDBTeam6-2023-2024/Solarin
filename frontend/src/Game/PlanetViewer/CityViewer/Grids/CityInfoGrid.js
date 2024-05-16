import React, {useEffect, useMemo, useState} from 'react';
import {AgGridReact} from 'ag-grid-react';
import './NewBuildingGrid.css';
import {getCityData, getUpgradeCost, upgradeBuilding} from "../BuildingManager";

import {UpgradeButtonComponent} from "./Buttons";
import {getCityImage} from "../GetCityImage";
import axios from "axios";
import statsJson from "../../../UI/stats.json";


const CityInfoGrid = ({
                          cityUpgradeInfo,
                          selectedImage,
                          resourceImage,
                          setBuildings,
                          refreshResources,
                          setCityUpgradeInfo,
                          cityId,
                          refresh,
                          setUpgradeCostMap,
                          cityUpgradeTimer,
                          setCityUpgradeTimer,
                          upgradeCost,
                          cityInfo,
                          setCityInfo
                      }) => {
    // const columns = useMemo(() => [
    //     { headerName: "", field: "label" },
    //     { headerName: "", field: "value", cellStyle: params => ({
    //         fontWeight: params.data.label === 'Region buffs' ? 'bold' : 'normal',
    //         color: params.data.label === 'Region buffs' ? 'red' : 'black'
    //     }) }
    // ], []);
    const [cityStats, setCityStats] = useState(null)


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

    const RegionBuffsCellRenderer = ({value}) => {
        return (
            <>{value.map((buff, index) => (
                <span key={index} style={{color: buff.modifier >= 0 ? 'green' : 'red'}}>
                {buff.percentage} {buff.type}
              </span>
            )).reduce((prev, curr) => [prev, ', ', curr])}</> // This handles the comma separation properly in JSX
        );
    };


    const columns = useMemo(() => [
        {headerName: "Category", field: "category"},
        {
            headerName: "Information",
            field: "info",
            cellRenderer: (params) => {
                if (params.data.category === "Region buffs") {
                    return <RegionBuffsCellRenderer value={params.value}/>;
                } else {
                    return <span>{params.value}</span>;
                }
            }
        }
    ], []);

    const rowData = useMemo(() => [
        // Example data preparation (similar to previous transformations)
        {category: "Region type", info: cityInfo.region_type, autoHeight: true},
        {
            category: "Region buffs", info: cityInfo.region_buffs.map(buff => ({
                type: buff[0],
                modifier: parseFloat(buff[1]) - 1,
                percentage: `${(parseFloat(buff[1]) - 1) >= 0 ? '+' : ''}${((parseFloat(buff[1]) - 1) * 100).toFixed(0)}%`
            })), autoHeight: true, autoWidth: true
        },
        {category: "Population size", info: cityInfo.population, autoHeight: true},
    ], [cityInfo]);

    const onGridReady = (params) => {
        params.api.sizeColumnsToFit();
    };

    return (
        <>

            <div className="ag-theme-alpine-dark city_info_grid">
                <AgGridReact
                    rowData={rowData}
                    columnDefs={columns}
                    domLayout='autoHeight'
                    suppressMovableColumns={true}
                    suppressDragLeaveHidesColumns={true}
                    onGridReady={onGridReady}
                />
            </div>
            <div className="right-screen-city-info">
                {cityStats &&
                    <>
                        <div className={"building-stats"}>
                            <img src={`/images/stats_icons/${statsJson.defense.icon}`} alt={"defense"}/>
                            <div>{cityStats["defense"] + cityStats["city_defense"]}</div>
                        </div>
                        <div className={"building-stats"}>
                            <img src={`/images/stats_icons/${statsJson.attack.icon}`} alt={"attack"}/>
                            <div>{cityStats["attack"] + cityStats["city_attack"]}</div>
                        </div>
                    </>
                }
                <div className="building_image">
                    <img src={getCityImage(cityInfo.rank)} alt="City" className="selected-image shadow-2xl"/>
                </div>
                {cityUpgradeInfo &&
                    <UpgradeButtonComponent
                        cityId={cityId}
                        upgradeCost={upgradeCost}
                        setUpgradeCostMap={setUpgradeCostMap}
                        refreshResources={refreshResources}
                        setBuildings={setBuildings}
                        setCityUpgradeInfo={setCityUpgradeInfo}
                        cityUpgradeBool={true}
                        timerDuration={cityUpgradeTimer}
                        setTimeDuration={setCityUpgradeTimer}
                        setCityInfo={setCityInfo}

                    />
                }
            </div>
        </>
    );
};

export default CityInfoGrid;
