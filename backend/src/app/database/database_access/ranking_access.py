import datetime

from ..models.models import *
from ..database import AsyncSession


class RankingAccess:
    """
    This class will manage the sql access related to ranking information
    """
    def __init__(self, session: AsyncSession):
        self.__session = session

    def getTopRanking(self, limit: int):
        """
        get a list of the top players in the game ranking
        """
        get_ranking = Select(User.username)
