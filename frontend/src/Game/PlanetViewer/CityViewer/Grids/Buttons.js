import {
    collectResources,
    getBuildings,
    getResourcesInStorage,
    getUpgradeCost,
    upgradeBuilding,
    upgradeCity
} from "../BuildingManager";
import React, { useState, useEffect } from 'react';

function formatTime(seconds) {
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


export const ResourceButtonComponent = ({data, cityId, refreshResources, resourcesInStorage, setResourcesInStorage}) => {
    const buttonStyle = "wide-button";



    const collectResourcesHelper = async (cityId, buildingId) => {
        try {
            await collectResources(cityId, buildingId);
            refreshResources();
            getResourcesInStorage(cityId).then(resourcesInStorage=> {
            setResourcesInStorage(resourcesInStorage.overview)
            })
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
                setSelectedClick([data.id, "Barracks"]);
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
    setCityUpgradeInfo,
    cityUpgradeBool,
    timerDuration = 0 // Default timer duration in seconds
}) => {
    const [timer, setTimer] = useState(timerDuration);
    const [isButtonDisabled, setIsButtonDisabled] = useState(true);

    useEffect(() => {
        setTimer(timerDuration);
        setIsButtonDisabled(true);

        const countdown = setInterval(() => {
            setTimer(prevTimer => {
                if (prevTimer <= 1) {
                    clearInterval(countdown);
                    setIsButtonDisabled(false);
                    return 0;
                }
                return prevTimer - 1;
            });
        }, 1000);

        return () => clearInterval(countdown);
    }, [timerDuration]);

    const UpgradeBuildingHelper = async () => {
        try {
            let UpgradeSuccessful;
            if (!cityUpgradeBool) {
                UpgradeSuccessful = await upgradeBuilding(cityId, data.id);
            } else {
                UpgradeSuccessful = await upgradeCity(cityId);
            }
            if (UpgradeSuccessful.confirmed === true) {
                const buildings = await getUpgradeCost(cityId);
                const building_costs = buildings[0];
                const costMap = building_costs.reduce((acc, building) => {
                    acc[building.id] = building;
                    return acc;
                }, {});
                setUpgradeCostMap(costMap);
                refreshResources();
                setCityUpgradeInfo(buildings[1]);
                const updatedBuildings = await getBuildings(cityId);
                setBuildings(updatedBuildings[0]);
            }
        } catch (error) {
            console.error("Failed to upgrade building:", error);
        }
    };

    let costData = cityUpgradeBool ? upgradeCost : upgradeCost[data.id];
    const isCostAvailable = costData && costData.costs.length > 0;
    const buttonStyle = isCostAvailable && costData.can_upgrade && !isButtonDisabled
        ? "wide-button"
        : "wide-button disabled";
    const formattedTime = formatTime(timer);
    const buttonText = isButtonDisabled
        ? `Please wait ${formattedTime}`
        : (isCostAvailable ? `Upgrade: ${costData.costs.map(cost => `${cost[1]} ${cost[0]}`).join(', ')}` : 'Loading...');

    return (
        <button className={buttonStyle} onClick={UpgradeBuildingHelper}
                disabled={!isCostAvailable || !costData.can_upgrade || isButtonDisabled}>
            {buttonText}
        </button>
    );
};
