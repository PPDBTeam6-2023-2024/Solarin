from sqlalchemy import *

from ..database import Base

from .domains import PositiveInteger

from ..models import *


class HasResources(Base):
    """
    Store resources associated with a user

    owner_id: the id of the user, that is associated with the resource
    resource_type: resource that our user has
    quantity: the amount of this resource that the user has
    """
    __tablename__ = "hasResources"
    owner_id = Column(Integer, ForeignKey("user.id", deferrable=True, initially='DEFERRED', ondelete="cascade"),
                      primary_key=True)

    resource_type = Column(String, ForeignKey("resourceType.name", deferrable=True, initially='DEFERRED',
                                              ondelete="cascade"), primary_key=True)
    quantity = Column(PositiveInteger, nullable=False, default=0)


class ResourceType(Base):
    """
    Types of resources that are in the game
    name: the name of the resource type
    """
    __tablename__ = 'resourceType'
    name = Column(String, primary_key=True)


