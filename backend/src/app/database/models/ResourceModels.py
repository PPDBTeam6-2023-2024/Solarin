from sqlalchemy import *

from ..database import Base

from .domains import PositiveInteger
from datetime import datetime
from ..models import *
from sqlalchemy.orm import relationship
from ...routers.trading.schemas import TradeOfferSchema


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
    starting_amount = Column(PositiveInteger, nullable=False)


class ProductionRegionModifier(Base):
    """
    Stores the modifiers applied to resource production based on the planet's region type.

    resource_type: Identifier for the type of resource.
    region_type: Type of the planetary region affecting production.
    production_modifier: Multiplier for base production rates, indicating boosts or reductions.
    """
    __tablename__ = 'ProductionRegionModifier'
    resource_type = Column(String, ForeignKey("resourceType.name"), primary_key=True)
    region_type = Column(String, ForeignKey('planetRegionType.region_type'), primary_key=True)
    modifier = Column(Float(precision=53))


class TradeOffer(Base):
    """
    Trading Offers need to be stored, for storing the offer, we use the Trade Offer Table
    alliance_name: name of the alliance that has access to the offer
    offer_owner: id of the user who placed the offer, and whose is able to cancel the offer
    id: id to uniquely identify the offer
    """
    __tablename__ = 'tradeOffer'
    alliance_name = Column(String, nullable=False)
    offer_owner = Column(Integer, ForeignKey("user.id", deferrable=True, initially='DEFERRED', ondelete="cascade"),
                         nullable=False)
    id = Column(Integer, Sequence('tradeOffer_id_seq'), primary_key=True, index=True)

    """
    Relations with trade Gives and Receives is joined, because in every situation with regards to this trade we are 
    interested in the other information on the other side of this relationship
    """
    gives = relationship("TradeGives", back_populates="offer", lazy='joined')
    receives = relationship("TradeReceives", back_populates="offer", lazy='joined')

    def toSchema(self):
        return TradeOfferSchema(user_id=self.offer_owner, offer_id=self.id,
                                gives=[(g.resource_type, g.amount) for g in self.gives],
                                receives=[(r.resource_type, r.amount) for r in self.receives])


class TradeGives(Base):
    """
    Each trade offer has 2 parts, 'gives' and 'receives' resources.
    This table stores which resources a user will give to the trade offer setter when he/she accepts the trade offer.
    offer_id: id of the offer the give resource belongs to
    resource_type: the type of resource we would give
    amount: the amount of this resource we would give
    """

    __tablename__ = 'tradeGives'
    offer_id = Column(Integer, ForeignKey("tradeOffer.id", deferrable=True, initially='DEFERRED',
                                          ondelete="cascade"), primary_key=True)

    resource_type = Column(String, ForeignKey("resourceType.name", deferrable=True, initially='DEFERRED',
                                              ondelete="cascade"), primary_key=True)

    amount = Column(PositiveInteger, nullable=False)

    """
    Relations with trade Gives and Receives is joined, because in every situation with regards to this trade we are 
    interested in the other information on the other side of this relationship
    """
    offer = relationship("TradeOffer", back_populates="gives", lazy='joined')


class TradeReceives(Base):
    """
    Each trade offer has 2 parts, 'gives' and 'receives' resources.
    This table stores which resources a user will receive from the trade offer setter when he/she accepts the trade
    offer.
    offer_id: id of the offer the give resource belongs to
    resource_type: the type of resource we would receive
    amount: the amount of this resource we would receive
    """

    __tablename__ = 'tradeReceives'
    offer_id = Column(Integer, ForeignKey("tradeOffer.id", deferrable=True, initially='DEFERRED',
                                          ondelete="cascade"), primary_key=True)

    resource_type = Column(String, ForeignKey("resourceType.name", deferrable=True, initially='DEFERRED',
                                              ondelete="cascade"), primary_key=True)

    amount = Column(PositiveInteger, nullable=False)

    """
    Relations with trade Gives and Receives is joined, because in every situation with regards to this trade we are 
    interested in the other information on the other side of this relationship
    """
    offer = relationship("TradeOffer", back_populates="receives", lazy='joined')


class MaintenanceTroop(Base):
    """
    This table stores maintenance costs for each troop type
    """

    __tablename__ = 'maintenanceTroop'

    troop_type = Column(TEXT, ForeignKey("troopType.type", deferrable=True, initially='DEFERRED', ondelete="cascade"),
                        primary_key=True)
    resource_type = Column(TEXT, ForeignKey("resourceType.name", deferrable=True, initially='DEFERRED',
                                            ondelete="cascade"),
                           primary_key=True)

    amount = Column(PositiveInteger, nullable=False)


class MaintenanceBuilding(Base):
    """
    This table stores maintenance costs for each building type
    """

    __tablename__ = 'maintenanceBuilding'

    building_type = Column(String, ForeignKey("buildingType.name", deferrable=True, initially='DEFERRED'),
                           primary_key=True)
    resource_type = Column(TEXT, ForeignKey("resourceType.name", deferrable=True, initially='DEFERRED',
                                            ondelete="cascade"),
                           primary_key=True)

    amount = Column(PositiveInteger, nullable=False)

