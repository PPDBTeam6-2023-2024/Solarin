from .data_access_exception import DataAccessException


class PermissionException(DataAccessException):
    """
    This exception is a data access Exception, that indicates that the user_id does not have
    the permission to do this data access Action
    """

    def __init__(self, user_id: int, action_message: str):
        super().__init__(f"{user_id} does not have the permissions to {action_message}")
