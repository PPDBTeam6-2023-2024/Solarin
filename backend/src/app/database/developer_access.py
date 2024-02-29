from .models import *
from .database import db, AsyncSession


class DeveloperAccess:
    """
    This class will manage the sql access for data related to information of planets
    """
    def __init__(self, session):
        self.__session = session

    async def createPlanetType(self, type_name: str, description: str = None):
        """
        creates a new type of planet
        """
        self.__session.add(PlanetType(type=type_name, description=description))

    async def createPlanetRegionType(self, type_name: str, description: str = None):
        """
        creates a new type of planet region
        """
        self.__session.add(PlanetRegionType(type=type_name, description=description))
