import {
    collectResources,
    getCityData,
    getResourcesInStorage,
    getUpgradeCost,
    upgradeBuilding,
    upgradeCity
} from "../BuildingManager";
import React, { useState, useEffect } from 'react';


function formatTime(seconds) {
    /*
    * Gives time a good format
    * */
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const remainingSeconds = seconds % 60;

    const parts = [
        hours ? String(hours).padStart(2, '0') : null,
        (hours || minutes) ? String(minutes).padStart(2, '0') : null,
        String(remainingSeconds).padStart(2, '0')
    ].filter(Boolean);

    return parts.join(':');
}

export const ResourceButtonComponent = ({data, cityId, refreshResources, setResourcesInStorage}) => {
    const buttonStyle = "wide-button";

    const collectResourcesHelper = async (cityId, buildingId) => {
        try {
            await collectResources(cityId, buildingId);
            refreshResources();
            getResourcesInStorage(cityId).then(resourcesInStorage => {
                setResourcesInStorage(resourcesInStorage.overview);
            });
        } catch (error) {
            console.error("Failed to collect resources:", error);
        }
    };

    if (data.type === "productionBuilding") {
        return (
            <button className={buttonStyle} onClick={() => collectResourcesHelper(cityId, data.id)}>
                Collect Resources
            </button>
        );
    }
    return null;
};

export const TrainButtonComponent = ({data, setSelectedClick}) => {
    return (
        <button
            className="wide-button"
            onClick={(event) => {
                event.stopPropagation();
                setSelectedClick([data.id, "Barracks", data.building_type]);
            }}
        >
            Train Troops
        </button>
    );
};

export const UpgradeButtonComponent = ({
    data,
    cityId,
    setUpgradeCostMap,
    setBuildings,
    upgradeCost,
    refreshResources,
    cityUpgradeBool,
    setCityInfo,
    totalTimePassed,
    setTotalTimePassed
}) => {
    /**
     * Component to create an upgrade button
     * */

    /*
    * A button appears disabled when not clickable (during upgrade, or when not enough resources)
    * */
    const [isButtonDisabled, setIsButtonDisabled] = useState(true);
    const [timer, setTimer] = useState(0)

    /* Effect to handle remaining time and button disabling logic*/
    useEffect(() => {
        const upgradeBuildingEvent = async () => {
            await refreshData();
        };
        /*
        * When waiting time is over, update the data
        * */
        const updateTimerAndCheckForExpiration = () => {
            const newTimerValue = Math.max(data.remaining_update_time - totalTimePassed, 0);
            setTimer(newTimerValue);
            if(data.remaining_update_time > 0 && newTimerValue <= 0){
                /*after a delay of 1 seconds upgradeBuildingEvent is called*/
                setTimeout(upgradeBuildingEvent, 1000)
            }
            setIsButtonDisabled(newTimerValue > 0);
        };

        updateTimerAndCheckForExpiration();

        /*
        * Visualize count down
        * */
        const countdown = setInterval(() => {
            setTimer(prevTimer => {
                const newTimer = Math.max(prevTimer - 1, 0);
                if (newTimer <= 0) {
                    clearInterval(countdown);
                    setIsButtonDisabled(false);
                }
                return newTimer;
            });
        }, 1000);
        return () => clearInterval(countdown);
    }, [data.remaining_update_time, totalTimePassed]);

    const refreshData = async () => {
        /*
        * Resync data with the backend
        * */
        try {
            const cityData = await getCityData(cityId);
            setBuildings(cityData?.buildings);
            setCityInfo(cityData?.city);
            const buildings = await getUpgradeCost(cityId);
            const building_costs = buildings?.[0];
            const costMap = building_costs?.reduce((acc, building) => {
                acc[building?.id] = building;
                return acc;
            }, {});
            setUpgradeCostMap(costMap);
            refreshResources();
            setTotalTimePassed(0)

            if (cityUpgradeBool){
                setTimer(buildings[1]?.time_cost);
                setIsButtonDisabled(true);
            }
        } catch (error) {
            console.error("Error refreshing building and city data:", error);
        }
    };


    const UpgradeBuildingHelper = async () => {
        /*
        * Execute the upgrade action
        * */
        try {
            let UpgradeSuccessful;
            if (!cityUpgradeBool) {
                UpgradeSuccessful = await upgradeBuilding(cityId, data.id);
            } else {
                UpgradeSuccessful = await upgradeCity(cityId);
            }
            if (UpgradeSuccessful.confirmed === true) {
                await refreshData()
            }
        } catch (error) {
            console.error("Failed to upgrade building:", error);
        }
    };


    let costData = cityUpgradeBool ? upgradeCost : upgradeCost[data.id];
    const isCostAvailable = costData && costData.costs.length > 0;
    const buttonStyle = isCostAvailable && costData.can_upgrade && !isButtonDisabled && !(cityUpgradeBool && (data.rank === 5))
        ? "wide-button"
        : "wide-button disabled";
    const formattedTime = formatTime(timer);

    /*Display the upgrade button text*/
    const buttonText = isButtonDisabled
        ? `Please wait ${formattedTime}`
        : (cityUpgradeBool && (data.rank === 5))
            ? 'Max City Rank: 5'
            : isCostAvailable
                ? `Upgrade: ${costData.costs.map(cost => `${cost[1]} ${cost[0]}`).join(', ')}`
                : 'Loading...';

    return (
        <button style={{"fontSize": "1.4vw"}} className={buttonStyle} onClick={UpgradeBuildingHelper}
                disabled={!isCostAvailable || !costData.can_upgrade || isButtonDisabled}>
            {buttonText}
        </button>
    );
};
