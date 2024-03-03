from ..database import AsyncSession

from .user_access import UserAccess
from .alliance_access import AllianceAccess
from .message_access import MessageAccess
from .planet_access import PlanetAccess
from .developer_access import DeveloperAccess
from .city_access import CityAccess
from .building_access import BuildingAccess
from .army_access import ArmyAccess
from .training_access import TrainingAccess


class DataAccess:
    """
    Common interface to access data from the Database
    The access methods are divided into categories so it is more easy to navigate for developers
    """
    def __init__(self, session: AsyncSession):
        self.__session = session
        self.UserAccess = UserAccess(session)
        self.AllianceAccess = AllianceAccess(session)
        self.MessageAccess = MessageAccess(session)
        self.PlanetAccess = PlanetAccess(session)
        self.DeveloperAccess = DeveloperAccess(session)
        self.CityAccess = CityAccess(session)
        self.BuildingAccess = BuildingAccess(session)
        self.ArmyAccess = ArmyAccess(session)
        self.TrainingAccess = TrainingAccess(session)

    async def commit(self):
        """
        Make sure you can call commit without having access to the session directly
        """
        await self.__session.commit()
