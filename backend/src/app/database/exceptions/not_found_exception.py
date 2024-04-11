from .data_access_exception import DataAccessException


class NotFoundException(DataAccessException):
    """
    This exception is a data access Exception, that data corresponding to a parameter is not found
    """

    def __init__(self, not_found_param: int | str, table_name: str):
        super().__init__(f"{table_name} does not have an entry for {not_found_param}")
