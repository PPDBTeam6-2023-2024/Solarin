from .data_access_exception import DataAccessException


class NotFoundException(DataAccessException):
    """
    This exception is a data access Exception, that data corresponding to a parameter is not found
    """

    def __init__(self, not_found_param: int | str, action_message: str):
        super().__init__(f"{not_found_param} does not exist during execution of {action_message}")
