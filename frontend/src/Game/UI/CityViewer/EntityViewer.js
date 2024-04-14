import BuildingRecords from "../buildingImages.json";
import TroopRecords from "../troops.json";

export const getImageForBuildingType = (buildingType) => {
    if (BuildingRecords && BuildingRecords[buildingType]) {
        return `/src/Game/Images/building_images/${BuildingRecords[buildingType].icon}`;
    }
    return null;
}

export const getImageForTroopType = (TroopType) => {
    if (TroopRecords && TroopRecords[TroopType]) {
        return `/src/Game/Images/troop_images/${TroopRecords[TroopType].icon}`;
    }
    return null;
}