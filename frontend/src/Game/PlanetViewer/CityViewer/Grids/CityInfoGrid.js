import React, { useMemo, useState } from 'react';
import { AgGridReact } from 'ag-grid-react';
import './NewBuildingGrid.css';
import {getBuildings, getUpgradeCost, upgradeBuilding} from "../BuildingManager";

import {UpgradeButtonComponent} from "./Buttons";
import {getCityImage} from "../GetCityImage";


const CityInfoGrid = ({ cityUpgradeInfo, selectedImage,resourceImage, setBuildings, refreshResources, setCityUpgradeInfo,cityId, cityRank, refresh, setUpgradeCostMap, cityUpgradeTimer ,setCityUpgradeTimer,upgradeCost, selectedBuilding, selectedClick, setSelectedClick }) => {
    const columns = useMemo(() => [
        { headerName: "", field: "label" },
        { headerName: "", field: "value", cellStyle: params => ({
            fontWeight: params.data.label === 'Region buffs' ? 'bold' : 'normal',
            color: params.data.label === 'Region buffs' ? 'red' : 'black'
        }) }
    ], []);

    const rowData = useMemo(() => [
        // { label: "Population size", value: cityInfo.populationSize },
        // { label: "Region type", value: cityInfo.regionType },
        { label: "Population size", value: 1000 },
        { label: "Region type", field: 'rural' },
        {
            label: "Region buffs",
            value: <>
                      <img src={resourceImage} alt="Resource" style={{ width: '20px', height: '20px' }}/>
                      <span style={{ color: 'red', fontWeight: 'bold' }}> +20%</span>
                   </>
        }

    ], [cityUpgradeInfo, resourceImage]);
    return (
        <>

                <div className="ag-theme-alpine-dark" style={{ width: '30%', height: '30vh' }}>
                    <AgGridReact
                        rowData={rowData}
                        columnDefs={columns}
                        domLayout='autoHeight'
                        suppressMovableColumns={true}
                        suppressDragLeaveHidesColumns={true}
                    />
                </div>
                <div className="right-screen">
                    <div className="building_image">
                        <img src={getCityImage(2)} alt="City" className="selected-image"/>
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

                    />
                }
            </div>
        </>
    );
};

export default CityInfoGrid;
