from abc import ABC, abstractmethod
from ...database.database_access.data_access import DataAccess


class RequestHandler:
    """
    handles a complex request
    """

    def __init__(self, data, db):
        """
        stores the data of the request

        """
        self.data = data
        self.data_access: DataAccess = DataAccess(db)
        self.__verify_data()

    @abstractmethod
    def __verify_data(self):
        """
        an abstract method to verify the integrity of the data
        """
        pass

    @abstractmethod
    async def handle(self, user_id):
        """
        do the required action
        """
        pass
