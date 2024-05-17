import React, { useMemo } from 'react';
import { AgGridReact } from 'ag-grid-react';
import './NewBuildingGrid.css';
import {UpgradeButtonComponent} from "./Buttons";
import {getCityImage} from "../GetCityImage";


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
        { category: "Region type", info: cityInfo?.region_type , autoHeight: true},
        { category: "Region buffs", info: cityInfo?.region_buffs.map(buff => ({
            type: buff[0],
            modifier: parseFloat(buff[1]) - 1,
            percentage: `${(parseFloat(buff[1]) - 1) >= 0 ? '+' : ''}${((parseFloat(buff[1]) - 1) * 100).toFixed(0)}%`
        })) , autoHeight: true, autoWidth: true},
        { category: "Population size", info: cityInfo?.population , autoHeight: true},
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
