from typing import Type
from sqlalchemy import *
from ..exceptions.domain_exception import DomainException

"""
This file contains the classes of the postgresSQL domains we use
"""


class Coordinate(TypeDecorator):

    """
    This class is a domain for coordinates (that are in the range of [0,1])
    """

    impl = Float(precision=53)

    @property
    def python_type(self) -> Type[Any]:
        return FLOAT

    def process_literal_param(self, value, dialect: Dialect) -> str:
        return value

    def process_bind_param(self, value, dialect):
        """
        SQL Alchemy has no native support for adding checks to Domains, so
        we check manually if the value of a coordinate is between 0 and 1.
        """
        if not (0 <= value <= 1):
            raise DomainException("Coordinate", "value in range [0, 1]")

        return value

    def process_result_value(self, value, dialect):
        return value


class PositiveInteger(TypeDecorator):
    """
    This class is a domain for positive integers
    """

    impl = Integer

    @property
    def python_type(self) -> Type[Any]:
        return int

    def process_literal_param(self, value, dialect: Dialect) -> str:
        return value

    def process_bind_param(self, value, dialect):
        """
        SQL Alchemy has no native support for adding checks to Domains, so
        we check manually if the value of the Integer is greater or equal to 0
        """
        if value is not None and not (0 <= value):
            raise DomainException("PositiveInteger", "value is negative")

        return value

    def process_result_value(self, value, dialect):
        return value
