import json
from src.app.database.database_access.developer_access import *
from src.logic.formula.compute_properties import *
from sqlalchemy import select
import os


class CreateTuples:
    async def create_all_tuples(self, session):
        self.__session: AsyncSession = session
        self.__dev = DeveloperAccess(session)
        types_file = open(f"{os.path.dirname(os.path.abspath(__file__))}/types.json").read()
        types = json.loads(types_file)
        await self.create_resource_types(types["resources"])
        await self.create_region_types(types["regions"])
        await self.create_planet_types(types["planets"])
        await self.create_production_modifiers(types["production-modifiers"])
        await self.create_city_costs(types["city-costs"])
        await self.create_associations(types["associations"])
        await self.create_stat_types(types["stats"])
        await self.create_troop_types(types["units"])
        await self.create_barracks_types(types["barracks"])
        await self.create_tower_types(types["towers"])
        await self.create_wall_types(types["walls"])
        await self.create_production_building_types(types["production-buildings"])
        await self.create_general_types(types["generals"])
        await self.create_political_stances(types["political-stance"])
        await self.__session.commit()

    async def create_associations(self, associations: list[dict[str, Any]]):
        for association in associations:
            stmt = (
                select(AssociatedWith)
                .where(AssociatedWith.planet_type == association["planet-type"])
                .where(AssociatedWith.region_type == association["region-type"])
            )
            if (await self.__session.execute(stmt)).scalar_one_or_none() is None:
                await self.__dev.create_associated_with(association["planet-type"], association["region-type"])

    async def create_barracks_types(self, barracks_types: list[dict[str, Any]]):
        for barracks_type in barracks_types:
            if await self.__session.get(BarracksType, barracks_type["name"]) is None:
                await self.__dev.create_barracks_type(barracks_type["name"])
                await self.__dev.set_creation_cost(barracks_type["name"],
                                                   [("TF", PropertyUtility.getGUC(barracks_type["creation-cost"], 1))])

                maintenance = [(m["product-name"], m["amount"]) for m in barracks_type["maintenance"]]
                await self.__dev.create_maintenance_building(barracks_type["name"], maintenance)

    async def create_tower_types(self, tower_types: list[dict[str, Any]]):
        for tower_type in tower_types:
            if await self.__session.get(TowerType, tower_type["name"]) is None:
                await self.__dev.create_tower_type(tower_type["name"], tower_type["attack"])
                await self.__dev.set_creation_cost(tower_type["name"],
                                                   [("TF", PropertyUtility.getGUC(tower_type["creation-cost"], 1))])

    async def create_wall_types(self, wall_types: list[dict[str, Any]]):
        for wall_type in wall_types:
            if await self.__session.get(WallType, wall_type["name"]) is None:
                await self.__dev.create_wall_type(wall_type["name"], wall_type["defense"])
                await self.__dev.set_creation_cost(wall_type["name"],
                                                   [("TF", PropertyUtility.getGUC(wall_type["creation-cost"], 1))])

    async def create_planet_types(self, planet_types: list[dict[str, Any]]):
        for planet_type in planet_types:
            if await self.__session.get(PlanetType, planet_type["type-name"]) is None:
                await self.__dev.create_planet_type(planet_type["type-name"], planet_type["description"])

    async def create_region_types(self, region_types: list[dict[str, Any]]):
        for region_type in region_types:
            if await self.__session.get(PlanetRegionType, region_type["type-name"]) is None:
                await self.__dev.create_planet_region_type(region_type["type-name"], region_type["description"])

    async def create_production_building_types(self, building_types: list[dict[str, Any]]):
        for building_type in building_types:
            if await self.__session.get(ProductionBuildingType, building_type["name"]) is None:
                await self.__dev.create_production_building_type(building_type["name"])
                await self.__dev.set_creation_cost(building_type["name"],
                                                   [("TF", PropertyUtility.getGUC(building_type["creation-cost"], 1))])
                for resource_type in building_type["products"]:
                    await self.__dev.set_produces_resources(building_type["name"], resource_type["product-name"], resource_type["base-rate"], resource_type["base-cap"])

                maintenance = [(m["product-name"], m["amount"]) for m in building_type["maintenance"]]
                await self.__dev.create_maintenance_building(building_type["name"], maintenance)



    async def create_resource_types(self, resource_types: list[str]):
        for resource_type in resource_types:
            if await self.__session.get(ResourceType, resource_type) is None:
                await self.__dev.create_resource_type(resource_type)

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
                await self.__dev.create_troop_type(troop_type["name"], timedelta(minutes=1), battle_stats)
                base_price = 50 if troop_type["spec"] == "land" else 100
                base_cost: int = PropertyUtility.getGPC(base_price,
                                                        [battle_stats.attack, battle_stats.defense,
                                                         battle_stats.city_attack, battle_stats.city_defense,
                                                         battle_stats.recovery, battle_stats.speed])
                await self.__dev.set_troop_type_cost(troop_type["name"], [("SOL", base_cost)])

                maintenance = [(m["product-name"], m["amount"]) for m in troop_type["maintenance"]]
                await self.__dev.create_maintenance_troop(troop_type["name"], maintenance)
    async def create_production_modifiers(self, production_modifiers: list[dict[str, Any]]):
        for coefficient in production_modifiers:
            stmt = (
                select(ProductionRegionModifier)
                .where(ProductionRegionModifier.resource_type == coefficient["resource-type"])
                .where(ProductionRegionModifier.region_type == coefficient["region-type"])
            )
            result = await self.__session.execute(stmt)
            if result.scalar_one_or_none() is None:
                resource_type = coefficient["resource-type"]
                region_type = coefficient["region-type"]
                modifier = coefficient["modifier"]

                await self.__dev.set_production_modifier(resource_type=resource_type, region_type=region_type,
                                                         modifier=modifier)

    async def create_city_costs(self, city_costs: list[dict[str,Any]]):
        for city_cost in city_costs:
                await self.__dev.set_city_costs(city_cost["activity"],city_cost["resource-type"], city_cost["amount"], city_cost["time_cost"])


    async def create_general_types(self, general_types: list):
        """
        Add general types to the database
        """
        for general_type in general_types:
            await self.__dev.create_general(general_type["name"])

            for modifier in general_type["modifiers"]:
                await self.__dev.create_general_modifier(general_type["name"], modifier["stat"],
                                                         modifier["amount"], modifier["political_stance"])

    async def create_stat_types(self, stats_types: list[str]):
        """
        Define the types of army stats
        """
        for s in stats_types:
            await self.__dev.create_stat(s)

    async def create_political_stances(self, stances: list[str]):
        """
        Define the types of army stats
        """
        for s in stances:
            await self.__dev.create_political_stance(s)
