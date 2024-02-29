from .database import db, AsyncSession
from .models import *
from ..schemas import MessageToken
from .user_access import UserAccess
from .alliance_access import AllianceAccess
from .message_access import MessageAccess
from .planet_access import PlanetAccess
from .developer_access import DeveloperAccess
from .city_access import CityAccess


class DataAccess:
    def __init__(self, session):
        self.__session = session
        self.UserAccess = UserAccess(session)
        self.AllianceAccess = AllianceAccess(session)
        self.MessageAccess = MessageAccess(session)
        self.PlanetAccess = PlanetAccess(session)
        self.DeveloperAccess = DeveloperAccess(session)
        self.CityAccess = CityAccess(session)

    async def commit(self):
        await self.__session.commit()
