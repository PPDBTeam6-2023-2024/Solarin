import datetime
import math
from ..models import *
from ..database import AsyncSession
from .army_access import ArmyAccess
from ....logic.formula.compute_properties import *
from typing import Tuple, List


class ResourceAccess:
    """
    This class will manage the sql access for data related to information of training units
    """
    def __init__(self, session: AsyncSession):
        self.__session = session

    async def has_resources(self, user_id: int, resource_check: List[Tuple[str, int]]) -> bool:
        """
        Checks if the provided user has enough of the provided resources

        :param: user_id: id of the user whose resources will be checked
        :param: resource_check: list of tuples (resource_name, amount), that will be checked
        """
        for resource in resource_check:
            """
            This costs None of this resoruce, so we don't have to check this
            """
            if resource[1] == 0:
                continue

            get_resources = Select(HasResources.resource_type, HasResources.quantity).\
                where((HasResources.owner_id == user_id) & (HasResources.resource_type == resource[0]))
            results = await self.__session.execute(get_resources)
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
        has_resources = await self.__session.execute(s)
        has_resources = has_resources.scalar_one_or_none()

        if has_resources is None:
            self.__session.add(HasResources(resource_type=resource_name, quantity=amount, owner_id=user_id))
        else:
            has_resources.quantity += amount

        await self.__session.flush()

    async def remove_resource(self, user_id: int, resource_name: str, amount: int):
        """
        Remove a resource value to the user

        :param: user_id: id of the user who will lose the removed resources
        :param: resource_name: name of the resource that will be removed
        :param: amount: amount of the provide resource that will be removed
        """

        s = Select(HasResources).\
            where((user_id == HasResources.owner_id) & (HasResources.resource_type == resource_name))
        has_resources = await self.__session.execute(s)
        has_resources = has_resources.scalar_one_or_none()

        if has_resources is None:
            self.__session.add(HasResources(resource_type=resource_name, quantity=0, owner_id=user_id))
        else:
            has_resources.quantity -= amount

        await self.__session.flush()

    async def get_resource_amount(self, user_id: int, resource_name: str) -> int:
        """
        returns the amount the user has of this resource

        :param: user_id: id of the user whose resources we want
        :param: resource_name: name of the resource

        :return: amount of this resource
        """
        s = Select(HasResources.quantity).\
            where((user_id == HasResources.owner_id) & (HasResources.resource_type == resource_name))
        has_resources = await self.__session.execute(s)
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
        user_resources = await self.__session.execute(select(HasResources).where(HasResources.owner_id == user_id))
        resources = await self.__session.execute(select(ResourceType))
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
