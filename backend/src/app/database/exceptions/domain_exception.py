from .data_access_exception import DataAccessException


class DomainException(DataAccessException):
    """
    This exception is a data access Exception, that indicates that some error occurred
    with a check of a SQL domain
    """

    def __init__(self, domain_name: str, failed_constraint: str):
        super().__init__(f"{domain_name} failed constraint: {failed_constraint}")
