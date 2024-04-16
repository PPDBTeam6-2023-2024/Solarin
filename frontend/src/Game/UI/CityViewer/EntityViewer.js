import BuildingRecords from "../buildingImages.json";
import TroopRecords from "../troops.json";

export const getImageForBuildingType = (buildingType) => {
    if (BuildingRecords && BuildingRecords[buildingType]) {
        return `/images/building_images/${BuildingRecords[buildingType].icon}`;
    }
    return null;
}

export const getImageForTroopType = (TroopType) => {
    if (TroopRecords && TroopRecords[TroopType]) {
        return `/images/troop_images/${TroopRecords[TroopType].icon}`;
    }
    return null;
}