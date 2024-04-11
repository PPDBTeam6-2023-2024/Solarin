import datetime

from ..models import *
from ..database import AsyncSession


class RankingAccess:
    """
    This class will manage the sql access related to ranking information
    """
    def __init__(self, session: AsyncSession):
        self.__session = session

    async def get_top_ranking(self, limit: int):
        """
        get a list of the top players in the game ranking
        """
        get_ranking = Select(User.username, HasResources.quantity).join(HasResources, User.id == HasResources.owner_id).where(HasResources.resource_type == "SOL").order_by(desc(HasResources.resource_type)).limit(limit)
        results = await self.__session.execute(get_ranking)
        results = results.all()
        return results
