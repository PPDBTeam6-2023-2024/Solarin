import datetime
import math
from ..models import *
from ..database import AsyncSession
from .army_access import ArmyAccess
from ....logic.utils.compute_properties import *
from typing import Tuple, List


class ResourceAccess:
    """
    This class will manage the sql access for data related to information of training units
    """
    def __init__(self, session: AsyncSession):
        self.__session = session

    async def has_resources(self, user_id: int, resource_check: List[Tuple[str, int]]):
        """
        Checks if the provided user has enough of the provided resources
        """
        for resource in resource_check:
            get_resources = Select(HasResources.resource_type, HasResources.quantity).where((HasResources.owner_id == user_id) & (HasResources.resource_type == resource[0]))
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
        """
        s = Select(HasResources).where((user_id == HasResources.owner_id) & (HasResources.resource_type == resource_name))
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
        """
        s = Select(HasResources).where((user_id == HasResources.owner_id) & (HasResources.resource_type == resource_name))
        has_resources = await self.__session.execute(s)
        has_resources = has_resources.first()

        has_resources[0].quantity -= amount
        await self.__session.flush()

    async def get_resource_amount(self, user_id: int, resource_name: str):
        """
        returns the amount the user has of this resource
        """
        s = Select(HasResources.quantity).where((user_id == HasResources.owner_id) & (HasResources.resource_type == resource_name))
        has_resources = await self.__session.execute(s)
        has_resources = has_resources.first()

        return has_resources[0]
