
class DataAccessException(Exception):
    """
    This class will be the base class for all the exceptions thrown, with regard to data access
    """

    def __init__(self, message: str):
        """
        We add a prefix to our exception to make it clear that it is a DataAccessException
        """
        super().__init__(f"data access Exception: {message}")
