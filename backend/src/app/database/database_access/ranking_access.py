import datetime

from ..models import *
from ..database import AsyncSession

from .database_acess import DatabaseAccess


class RankingAccess(DatabaseAccess):
    """
    This class will manage the sql access related to ranking information
    """
    def __init__(self, session: AsyncSession):
        super().__init__(session)
        
    async def get_top_ranking(self, limit: int):
        """
        get a list of the top players in the game ranking
        The ranking is based on the amount of SOL a user has

        :param: limit: max amount of ranking entries (top x) we want to retrieve
        """
        get_ranking = Select(User.username, HasResources.quantity).\
            join(HasResources, User.id == HasResources.owner_id).\
            where(HasResources.resource_type == "SOL").order_by(desc(HasResources.quantity)).limit(limit)
        results = await self.session.execute(get_ranking)
        results = results.all()
        return results
