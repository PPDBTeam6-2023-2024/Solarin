from sqlalchemy.ext.asyncio import AsyncSession
from .database_acess import DatabaseAccess
from ..models import *
from ..exceptions.permission_exception import PermissionException
from .army_access import ArmyAccess


class GeneralAccess(DatabaseAccess):
    """
    This class will manage the sql access for data related to information of generals
    """
    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def get_available_generals(self, user_id: int):
        """
        Get the generals that are still available (not assigned) to an army of the user

        :param: user_id: the id of the user whose available generals we want to retrieve
        :return: list of General Model objects
        """

        """
        Retrieve All generals that are not assigned to a user its army
        """
        get_generals = Select(Generals).join(ArmyHasGeneral, ArmyHasGeneral.general_name == Generals.name).\
            join(Army, Army.id == ArmyHasGeneral.army_id).where(Army.user_id == user_id)

        generals_army = await self.session.execute(get_generals)
        generals_army = generals_army.scalars().all()

        get_generals = Select(Generals)

        generals_all = await self.session.execute(get_generals)
        generals_all = generals_all.scalars().all()

        remaining_generals = list(set(generals_all)-set(generals_army))

        return remaining_generals

    async def assign_general(self, user_id: int, army_id: int, general_name: str):
        """
        Assign a general to a provided army

        :param: user_id: the id of the user who does this action
        :param: army_id: the id of the army who get a general assigned
        :param: general_name: name of the general that will be assigned to this army
        """

        """
        Remove general in case a general is already assigned
        """
        await self.remove_general(user_id, army_id)

        ac = ArmyAccess(self.session)
        army_owner = await ac.get_army_owner(army_id)

        if army_owner.id != user_id:
            raise PermissionException(user_id, "change the assignment of generals of another user its armies")

        army_has = ArmyHasGeneral(army_id=army_id, general_name=general_name)
        self.session.add(army_has)

        await self.session.flush()

    async def get_general(self, army_id: int):
        """
        Retrieve the general that is part of the provided army

        :param: army_id: the id of the army whose general we want to retrieve
        :return: general object, or None when no general assigned to this army
        """

        get_general = Select(Generals).join(ArmyHasGeneral, ArmyHasGeneral.general_name == Generals.name).\
            where(ArmyHasGeneral.army_id == army_id)

        general = await self.session.execute(get_general)
        general = general.scalar_one_or_none()

        return general

    async def remove_general(self, user_id: int, army_id: int):
        """
        unassign a general form an army

        :param: army_id: the id of the army whose general we want to unassign
        """

        ac = ArmyAccess(self.session)
        army_owner = await ac.get_army_owner(army_id)

        if army_owner.id != user_id:
            raise PermissionException(user_id, "change the assignment of generals of another user its armies")

        delete_general_assignment = delete(ArmyHasGeneral).where(ArmyHasGeneral.army_id==army_id)
        await self.session.execute(delete_general_assignment)
        await self.session.flush()

    async def get_modifiers(self, user_id: int, general_name: str):
        """
        Get the modifiers corresponding to a specific general
        :param: general_name: name of the general whose modifiers we want

        :return: List of tuple objects of ('GeneralModifier', polital stance value) object
        """

        get_modifiers = Select(GeneralModifier, HasPoliticalStance.value).\
            join(HasPoliticalStance, (GeneralModifier.political_stance == HasPoliticalStance.stance_name)). \
            where((GeneralModifier.general_name == general_name) & (user_id == HasPoliticalStance.user_id))
        modifiers = await self.session.execute(get_modifiers)
        modifiers = modifiers.all()

        return modifiers


