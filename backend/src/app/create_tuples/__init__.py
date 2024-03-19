import json
from src.app.database.database_access.developer_access import *
from src.logic.utils.compute_properties import *
import os
from src.app.database.database import sessionmanager


class CreateTuples:

    async def create_all_tuples(self):
        async with sessionmanager.session() as session:
            self.__session: AsyncSession = session
            self.__dev = DeveloperAccess(session)
        types_file = open(f"{os.path.dirname(os.path.abspath(__file__))}/types.json").read()
        types = json.loads(types_file)
        await self.create_resource_types(types["resources"])
        await self.create_region_types(types["regions"])
        await self.create_planet_types(types["planets"])
        await self.create_troop_types(types["units"])
        await self.create_barracks_types(types["barracks"])
        await self.create_tower_types(types["towers"])
        await self.create_wall_types(types["walls"])
        await self.create_building_types(types["buildings"])
        await self.__session.commit()

    async def create_barracks_types(self, barracks_types: list[dict[str, Any]]):
        for barracks_type in barracks_types:
            if await self.__session.get(BarracksType, barracks_type["name"]) is None:
                await self.__dev.createBarracksType(barracks_type["name"])

    async def create_tower_types(self, tower_types: list[dict[str, Any]]):
        for tower_type in tower_types:
            if await self.__session.get(TowerType, tower_type["name"]) is None:
                await self.__dev.createTowerType(tower_type["name"], tower_type["attack"])

    async def create_wall_types(self, wall_types: list[dict[str, Any]]):
        for wall_type in wall_types:
            if await self.__session.get(WallType, wall_type["name"]) is None:
                await self.__dev.createWallType(wall_type["name"], wall_type["defense"])

    async def create_planet_types(self, planet_types: list[dict[str, Any]]):
        for planet_type in planet_types:
            if await self.__session.get(PlanetType, planet_type["type-name"]) is None:
                await self.__dev.createPlanetType(planet_type["type-name"], planet_type["description"])

    async def create_region_types(self, region_types: list[dict[str, Any]]):
        for region_type in region_types:
            if await self.__session.get(PlanetRegionType, region_type["type-name"]) is None:
                await self.__dev.createPlanetRegionType(region_type["type-name"], region_type["description"])

    async def create_building_types(self, building_types: list[dict[str, Any]]):
        for building_type in building_types:
            if await self.__session.get(ProductionBuildingType, building_type["name"]) is None:
                # to change
                base_production: int = building_type["products"][0].get("base-production") if \
                building_type["products"][0].get(
                    "base-production", None) is not None else building_type["products"][0]["base-rate"] * 60
                await self.__dev.createProductionBuildingType(building_type["name"], base_production,
                                                              building_type["products"][0]["base-cap"])

                await self.__dev.setUpgradeCost(building_type["name"],
                                                [("TF", PropertyUtility.getGUC(building_type["creation-cost"], 1))])
                for resource_type in building_type["products"]:
                    await self.__dev.setProducesResources(building_type["name"], resource_type["product-name"])

    async def create_resource_types(self, resource_types: list[str]):
        for resource_type in resource_types:
            if await self.__session.get(ResourceType, resource_type) is None:
                await self.__dev.createResourceType(resource_type)

    async def create_troop_types(self, troop_types: list[dict[str, Any]]):
        for troop_type in troop_types:
            if await self.__session.get(TroopType, troop_type["name"]) is None:
                # to change
                attack = troop_type["base-points"]["AP"]
                defense = troop_type["base-points"]["DP"]
                city_attack = troop_type["base-points"]["CAP"]
                city_defense = troop_type["base-points"]["CDP"]
                recovery = troop_type["base-points"]["PBR"]
                speed = troop_type["base-points"]["MS"]
                battle_stats = BattleStats(attack=attack, defense=defense, city_attack=city_attack,
                                           city_defense=city_defense, recovery=recovery, speed=speed)

                # to change
                await self.__dev.createToopType(troop_type["name"], timedelta(minutes=1), battle_stats)
                base_price = 50 if troop_type["spec"] == "land" else 100
                base_cost: int = PropertyUtility.getGPC(base_price,
                                                        [battle_stats.attack, battle_stats.defense,
                                                         battle_stats.city_attack, battle_stats.city_defense,
                                                         battle_stats.recovery, battle_stats.speed])
                await self.__dev.setTroopTypeCost(troop_type["name"], [("SOL", base_cost)])
