from .data_access_exception import DataAccessException


class InvalidActionException(DataAccessException):
    """
    This exception is a data access Exception, that indicates that an invalid action is done based
    on the parameters
    """

    def __init__(self, message: str):
        super().__init__(message)
