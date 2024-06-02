from typing import Type
from sqlalchemy import *
from ..exceptions.domain_exception import DomainException

"""
This file contains the classes of the postgresSQL domains we use
"""


class Decimal(TypeDecorator):

    """
    This class is a domain for values that are in the range of [0,1]
    """

    impl = Float(precision=53)
    cache_ok = True

    @property
    def python_type(self) -> Type[Any]:
        return FLOAT

    def process_literal_param(self, value, dialect: Dialect) -> str:
        return value

    def process_bind_param(self, value, dialect):

        return value

    def process_result_value(self, value, dialect):
        return value


class Percentage(TypeDecorator):

    """
    This class is a domain for values that are in the range of [0,1]
    """

    impl = Float(precision=53)
    cache_ok = True

    @property
    def python_type(self) -> Type[Any]:
        return FLOAT

    def process_literal_param(self, value, dialect: Dialect) -> str:
        return value

    def process_bind_param(self, value, dialect):
        """
        SQL Alchemy has no native support for adding checks to Domains, so
        we check manually if the value is between 0 and 1.
        """
        if not (-1 <= value <= 1):
            raise DomainException("Percentage", "value in range [-1, 1]")

        return value

    def process_result_value(self, value, dialect):
        return value


class Coordinate(Decimal):
    """
    This class is a domain for values that are in the range of [0,1]
    """
    def process_bind_param(self, value, dialect):

        if value is not None:
            value = min(value, (2 ** 31) - 1)

        return value


class PositiveInteger(TypeDecorator):
    """
    This class is a domain for positive integers
    """

    impl = Integer
    cache_ok = True
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
        if value is not None:
            value = min(value, (2 ** 31) - 1)

        if value is not None and not (0 <= value):
            raise DomainException("PositiveInteger", "value is negative")

        return value

    def process_result_value(self, value, dialect):
        return value


class HexColor(TypeDecorator):
    """
    This class is a domain for colors encoded as hexadecimal
    """

    impl = String
    cache_ok = True

    @property
    def python_type(self) -> Type[Any]:
        return int

    def process_literal_param(self, value, dialect: Dialect) -> str:
        return value

    def process_bind_param(self, value, dialect):
        """
        SQL Alchemy has no native support for adding checks to Domains, so
        we check manually that it is a valid hex code
        """

        if value is not None:
            if not isinstance(value, str):
                raise DomainException("HexColor", "not a string type")

            if len(value) != 7:
                raise DomainException("HexColor", "wrong amount of characters")

            if value[0] != "#":
                raise DomainException("HexColor", "HexColor needs to start with a '#'")

        return value

    def process_result_value(self, value, dialect):
        return value
