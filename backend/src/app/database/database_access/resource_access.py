import datetime
import math
from ..models import *
from ..database import AsyncSession
from ....logic.formula.compute_properties import *
from typing import Tuple, List
from .database_acess import DatabaseAccess


class ResourceAccess(DatabaseAccess):
    """
    This class will manage the sql access for data related to information of resources
    """
    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def set_starting_resources(self, user_id: int) -> None:
        """
        Set the starting resources for a user and remove all the resources the user had before

        :param: user_id: id of the user whose resources will be set
        """
        resources = await self.session.execute(select(ResourceType))
        resources = resources.scalars().all()
        for resource in resources:
            """
            Remove all the resources the user had before
            """
            d = delete(HasResources).where(HasResources.owner_id == user_id)
            await self.session.execute(d)
            """
            Set the starting resources for the user
            """
            self.session.add(HasResources(resource_type=resource.name, quantity=resource.starting_amount, owner_id=user_id))
        await self.session.flush()

    async def has_resources(self, user_id: int, resource_check: List[Tuple[str, int]]) -> bool:
        """
        Checks if the provided user has enough of the provided resources

        :param: user_id: id of the user whose resources will be checked
        :param: resource_check: list of tuples (resource_name, amount), that will be checked
        """
        for resource in resource_check:
            """
            This costs None of this resource, so we don't have to check this
            """
            if resource[1] == 0:
                continue

            get_resources = Select(HasResources.resource_type, HasResources.quantity).\
                where((HasResources.owner_id == user_id) & (HasResources.resource_type == resource[0]))
            results = await self.session.execute(get_resources)
            resource_real = results.first()

            if resource_real is None:
                return False

            """
            When not enough resources
            """
            if resource[1] > resource_real[1]:
                return False

        return True

    async def add_resource(self, user_id: int, resource_name: str, amount: int):
        """
        Add a resource value to the user

        :param: user_id: id of the user who will receive the added resources
        :param: resource_name: name of the resource that will be added
        :param: amount: amount of the provide resource that will be added
        """
        s = Select(HasResources).\
            where((user_id == HasResources.owner_id) & (HasResources.resource_type == resource_name))
        has_resources = await self.session.execute(s)
        has_resources = has_resources.scalar_one_or_none()

        if has_resources is None:
            self.session.add(HasResources(resource_type=resource_name, quantity=amount, owner_id=user_id))
        else:
            has_resources.quantity += amount

        await self.session.flush()

    async def remove_resource(self, user_id: int, resource_name: str, amount: int):
        """
        Remove a resource value to the user

        :param: user_id: id of the user who will lose the removed resources
        :param: resource_name: name of the resource that will be removed
        :param: amount: amount of the provide resource that will be removed
        """

        s = Select(HasResources).\
            where((user_id == HasResources.owner_id) & (HasResources.resource_type == resource_name))
        has_resources = await self.session.execute(s)
        has_resources = has_resources.scalar_one_or_none()

        if has_resources is None:
            self.session.add(HasResources(resource_type=resource_name, quantity=0, owner_id=user_id))
        else:
            has_resources.quantity -= amount

        await self.session.flush()

    async def get_resource_amount(self, user_id: int, resource_name: str) -> int:
        """
        returns the amount the user has of this resource

        :param: user_id: id of the user whose resources we want
        :param: resource_name: name of the resource

        :return: amount of this resource
        """
        s = Select(HasResources.quantity).\
            where((user_id == HasResources.owner_id) & (HasResources.resource_type == resource_name))
        has_resources = await self.session.execute(s)
        has_resources = has_resources.scalar_one_or_none()

        if has_resources is None:
            has_resources = 0

        return has_resources

    async def get_resources(self, user_id: int):
        """
        Get all the resources of a specific user

        :param: user_id: id of the user whose resources we want
        return: dict, with resource names as keys and resource amount as values
        """

        """
        Retrieve the resources of the user
        """
        user_resources = await self.session.execute(select(HasResources).where(HasResources.owner_id == user_id).\
            order_by(asc(HasResources.resource_type)))
        resources = await self.session.execute(select(ResourceType))
        result: dict[str, int] = {}

        """
        Put resources inside a dictionary
        """
        for user_resource in user_resources.scalars().all():
            result[user_resource.resource_type] = user_resource.quantity

        """
        All the resources that do not have an entry, will receive value 0
        """
        for resource in resources.scalars().all():
            result[resource.name] = 0 if not result.get(resource.name, False) else result[resource.name]

        return result

    async def get_maintenance_city(self, city_id: int):
        """
        Get the maintenance cost for a specific city

        :param: city_id: id corresponding to the city
        """

        get_costs = Select(MaintenanceBuilding, BuildingInstance.rank).\
            join(BuildingType, BuildingType.name == MaintenanceBuilding.building_type).\
            join(BuildingInstance, BuildingInstance.building_type == BuildingType.name).\
            where(BuildingInstance.city_id == city_id)

        maintenance_costs = await self.session.execute(get_costs)
        maintenance_costs = maintenance_costs.all()

        cost_dict = {}
        for m, rank in maintenance_costs:
            """
            Calculate maintenance cost for the city, taking into account the rank of the buildings
            """
            cost_dict[m.resource_type] = cost_dict.get(m.resource_type, 0)+PropertyUtility.getGPR(1.0, m.amount,
                                                                                                  rank, False)

        """
        Let city population also affect the maintenance
        """
        get_city_population = Select(City.population).where(City.id == city_id)
        population = await self.session.execute(get_city_population)
        population = population.scalar_one_or_none()

        cost_dict["RA"] = cost_dict.get("RA", 1)+floor(population/10)
        return cost_dict

    async def check_maintenance_city(self, user_id: int, city_id: int, delta_time: int = None):
        """
        Check the maintenance of a city
        :param: user_id: id corresponding to the user that is being checked
        :param: city_id: id corresponding to the city
        :return: boolean if true, maintenance has removed a city
        """

        if delta_time is None:
            delta_time = await self.maintenance_delta_time(user_id)

        maintenance = await self.get_maintenance_city(city_id)
        m_list = []

        min_time = 1
        for k, m in maintenance.items():
            remaining_resources = await self.get_resource_amount(user_id, k)
            min_time = min(math.floor(remaining_resources/m), min_time)

            m_list.append((k, math.floor(m*delta_time/3600)))

            if remaining_resources < math.floor(m*delta_time/3600):
                """
                When not enough resources set the resource amount to 0
                """
                await self.remove_resource(user_id, k, await self.get_resource_amount(user_id, k))

        """
        We Will now check whether we have sufficient resources
        """

        has_enough = await self.has_resources(user_id, m_list)
        if has_enough:
            """
            Remove the resources
            """
            for r in m_list:
                await self.remove_resource(user_id, r[0], r[1])

            return False

        """
        In case a user does not have enough resources, the user will, lose some buildings in the city
        """

        hours_passed = math.floor(max(delta_time/3600-min_time, 0))

        get_deleted_buildings = Select(BuildingInstance, MaintenanceBuilding).\
            join(City, City.id == BuildingInstance.city_id).\
            join(MaintenanceBuilding, MaintenanceBuilding.building_type == BuildingInstance.building_type).\
            where(City.id == city_id).\
            order_by(func.random()).limit(hours_passed)

        deleted_buildings = await self.session.execute(get_deleted_buildings)
        deleted_buildings = deleted_buildings.all()

        for del_b, maintenance in deleted_buildings:

            r_amount = await self.get_resource_amount(user_id, maintenance.resource_type)
            if r_amount > 0:
                continue

            d = delete(BuildingInstance).where(BuildingInstance.id == del_b.id)
            await self.session.execute(d)

        await self.session.flush()

        return True

    async def maintenance_delta_time(self, user_id):
        """
        Get the time between now and the last maintenance check
        """

        get_last_checked = Select(User.last_maintenance_check).where(User.id == user_id)
        last_time = await self.session.execute(get_last_checked)
        last_time = last_time.scalar_one()

        delta_time = datetime.utcnow()-last_time

        return delta_time.total_seconds()

    async def maintenance_checked(self, user_id: int):
        """
        Set the last checked maintenance timer to now
        """
        delta_time = await self.maintenance_delta_time(user_id)
        """
        We only want to remove 1 hour, because some checks work every hour
        """

        u = Update(User).values({"last_maintenance_check": datetime.utcnow()}).where(User.id == user_id)
        await self.session.execute(u)
        await self.session.flush()

    async def get_maintenance_army(self, army_id: int):
        """
        Get the maintenance cost for a specific army

        :param: army_id: id corresponding to the army

        :return: boolean if true, maintenance has removed some troops
        """

        get_costs = Select(MaintenanceTroop, ArmyConsistsOf.rank, ArmyConsistsOf.size).\
            join(TroopType, MaintenanceTroop.troop_type == TroopType.type).\
            join(ArmyConsistsOf, ArmyConsistsOf.troop_type == TroopType.type).\
            where(ArmyConsistsOf.army_id == army_id)

        maintenance_costs = await self.session.execute(get_costs)
        maintenance_costs = maintenance_costs.all()

        cost_dict = {}
        for m, rank, size in maintenance_costs:
            """
            Calculate maintenance cost for the city, taking into account the rank of the buildings
            """
            cost_dict[m.resource_type] = floor(cost_dict.get(m.resource_type, 0) \
                                         + PropertyUtility.getUnitTrainCost(1.0, rank)*m.amount*size)

        return cost_dict

    async def check_maintenance_army(self, user_id: int, army_id: int, delta_time: int = None):
        """
        Check the maintenance of an army
        :param: user_id: id corresponding to the user that is being checked
        :param: city_id: id corresponding to the city
        """

        if delta_time is None:
            delta_time = await self.maintenance_delta_time(user_id)

        maintenance = await self.get_maintenance_army(army_id)
        m_list = []

        min_time = 1
        for k, m in maintenance.items():
            if m == 0:
                continue

            remaining_resources = await self.get_resource_amount(user_id, k)
            min_time = min(math.floor(remaining_resources / m), min_time)
            m_list.append((k, math.floor(m*delta_time/3600)))

        """
        In case a user does not have enough resources,  we lose part of its troops
        We will do the following formula: we set the resource to 0, and every hour we kill 20% of the remaining army 
        that uses this resource.
        """
        hours_passed = max(delta_time/3600-min_time, 0)
        army_remaining = 0.9**hours_passed

        changed = False
        for r in m_list:
            """
            We Will now check whether we have sufficient resources
            """
            has_enough = await self.has_resources(user_id, [r])
            if has_enough:
                await self.remove_resource(user_id, r[0], r[1])
                continue

            """
            Set remaining resources to 0
            """
            await self.remove_resource(user_id, r[0], await self.get_resource_amount(user_id, r[0]))

            """
            Retrieve troops that use the resources that are in shortage
            """

            get_losing_troops = Select(ArmyConsistsOf).\
                join(TroopType, ArmyConsistsOf.troop_type == TroopType.type).\
                join(MaintenanceTroop, TroopType.type == MaintenanceTroop.troop_type).\
                where(MaintenanceTroop.resource_type == r[0])

            losing_troops = await self.session.execute(get_losing_troops)
            losing_troops = losing_troops.scalars().all()
            for t in losing_troops:
                t.size = math.ceil(t.size*army_remaining)
                if t.size == 0:
                    t.size = 1

            changed = True

        await self.session.flush()
        return changed


