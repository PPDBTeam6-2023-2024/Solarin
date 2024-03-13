import json
from src.app.database.database_access.developer_access import *
from src.logic.utils.compute_properties import *
def create_planet_types(dev: DeveloperAccess, planet_types: list[dict[str,Any]]):
    for planet_type in planet_types:
        dev.createPlanetType(planet_type["type-name"], planet_type["description"])


def create_region_types(dev: DeveloperAccess, region_types: list[dict[str,Any]]):
    for region_type in region_types:
        dev.createPlanetRegionType(region_type["type-name"], region_type["description"])

def create_building_types(dev: DeveloperAccess, building_types: list[dict[str,Any]]):
    for building_type in building_types:
        if building_type["is-barrack"]:
            dev.createBarracksType(building_type["name"])

        # to change
        base_production: int = building_type["products"][0]["base-production"] if building_type["products"][0]["base-production"] is not None else building_type["products"][0]["base-rate"]*60
        dev.createProductionBuildingType(building_type["name"], base_production, building_type["base-cap"])

        dev.setUpgradeCost(building_type["name"], [("TF", PropertyUtility.getGUC(building_type["creation-cost"], 1))])
        for resource_type in building_type["products"]:
            dev.setProducesResources(building_type["name"], resource_type["product-name"])

def create_resource_types(dev: DeveloperAccess, resource_types: list[str]):
    for resource_type in resource_types:
        dev.createResourceType(resource_type)

def create_troop_types(dev: DeveloperAccess, troop_types: list[dict[str, Any]]):
    for troop_type in troop_types:
        # to change
        battle_stats = BattleStats()
        battle_stats.attack = troop_type["base_points"]["AP"]
        battle_stats.defense = troop_type["base_points"]["DP"]
        battle_stats.city_attack = troop_type["base_points"]["CAP"]
        battle_stats.city_defense = troop_type["base_points"]["CDP"]
        battle_stats.recovery = troop_type["base_points"]["PBR"]
        battle_stats.speed = troop_type["base_points"]["MS"]


        # to change
        dev.createToopType(troop_type["name"], timedelta(minutes=1), battle_stats, None)
        base_price = 50 if troop_type["spec"] == "land" else 100
        base_cost: int = PropertyUtility.getGPC(base_price,
               [battle_stats.attack, battle_stats.defense,
                battle_stats.city_attack, battle_stats.city_defense,
                battle_stats.recovery, battle_stats.speed])
        dev.setTroopTypeCost(troop_type["name"], [("SOL", base_cost)])



def create_tuples(dev: DeveloperAccess):
    types_file = open("./types.json").read()
    types = json.loads(types_file)
    create_resource_types(dev, types["resources"])
    create_region_types(dev, types["regions"])
    create_planet_types(dev, types["planets"])
    create_troop_types(dev, types["units"])
    create_building_types(dev, types["buildings"])

