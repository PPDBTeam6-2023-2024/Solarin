from sqlalchemy import *

from ..database import Base
from sqlalchemy.orm import relationship
from ...routers.cityManager.schemas import BuildingInstanceSchema, CitySchema, BuildingTypeSchema

from .domains import Coordinate, PositiveInteger
import datetime
from ..models import *


class City(Base):
    """
    Stores information about a city that is in a region on a planet.

    id: unique id to identify the city
    region_id: the id of the region in which the city is located
    controlled_by: id of the user who is currently the owner of the city
    rank: the rank (=level) of a city

    x, y: represent the planetary coordinates of the city.
    """
    __tablename__ = 'city'

    region_id = Column(Integer, ForeignKey("planetRegion.id", deferrable=True, initially='DEFERRED'))
    id = Column(Integer, Sequence("city_id_seq"), primary_key=True)
    controlled_by = Column(Integer, ForeignKey("user.id", deferrable=True, initially='DEFERRED'), nullable=False)
    x = Column(Coordinate, nullable=False)
    y = Column(Coordinate, nullable=False)

    rank = Column(PositiveInteger, nullable=False, default=1)

    region = relationship("PlanetRegion", back_populates="cities", lazy='joined')

    population = Column(Integer, default= 1024)

    def to_city_schema(self):
        """
        Convert the City object to a CitySchema (scheme)

        """
        return CitySchema(id=self.id,
                          region_id=self.region_id,
                          controlled_by=self.controlled_by,
                          x=self.x,
                          y=self.y,
                          rank=self.rank,
                          region_type=self.region.region_type,
                          planet_name=self.region.planet.name,
                          planet_id=self.region.planet_id,
                          population=self.population)


class BuildingInstance(Base):
    """
    Stores which buildings a city has
    id: unique id to identify the building
    city_id: id of city that has this building
    building_type: type of building this instance has (ProductionBuilding, Barracks,...)
    rank: rank (=level) of this building
    """

    __tablename__ = "buildingInstance"
    id = Column(Integer, Sequence('buildingInstance_id_seq'), primary_key=True, index=True)
    city_id = Column(Integer, ForeignKey("city.id", deferrable=True, initially='DEFERRED', ondelete="cascade"),
                     nullable=False)
    building_type = Column(String, ForeignKey("buildingType.name", deferrable=True, initially='DEFERRED'),
                           nullable=False)
    rank = Column(PositiveInteger, nullable=False, default=1)

    """
    stores when the data about this building is last checked
    """
    last_checked = Column(TIMESTAMP, nullable=False, default=datetime.utcnow)

    """
    This relation is joined, because when we ask for an instance we will often also be interested in the type 
    its attributes
    """
    type = relationship("BuildingType", back_populates="instances", lazy='joined')

    def to_schema(self, type_category) -> BuildingInstanceSchema:
        """
        Convert the buildinginstance Object to a scheme
        """
        b = BuildingInstanceSchema(
            id=self.id,
            city_id=self.city_id,
            building_type=self.building_type,
            rank=self.rank,
            type=type_category,
        )

        return b


class BuildingType(Base):
    """
    Stores the types of buildings that can exist (This table is the parent of an ISA/polymorphic relation)

    name: is the name of this buildingType
    type: Column entry to indicate which child it has a polymorphic relationship with (Barracks, ...)
    """
    __tablename__ = 'buildingType'
    name = Column(String, Sequence("buildingType_name_seq"), primary_key=True)

    type = Column(String, nullable=False)
    required_rank = Column(Integer)
    __mapper_args__ = {
        'polymorphic_on': type
    }

    def to_schema(self, resource_cost_type: str, resource_cost_amount: str) -> BuildingTypeSchema:
        """
        Convert this buildingType object into a scheme
        """
        rank = self.required_rank
        if rank is None:
            rank = 0
        b_type_schema = BuildingTypeSchema(
            name=self.name,
            type=self.type,
            required_rank=rank,
            resource_cost_type=resource_cost_type,
            resource_cost_amount=resource_cost_amount

        )
        return b_type_schema

    """
    This relation is NOT joined, in comparison to its corresponding relation, because we don't always 
    need all the instances of the type 
    """
    instances = relationship("BuildingInstance", back_populates="type", lazy='select')


class BarracksType(BuildingType):
    """
    Stores which types of barracks exist (This table is a child of an ISA/polymorphic relation with BuildingType)
    name: name of the BarrackType building.
    Every row in this table indicates a building that can be used as a barrack
    """
    __tablename__ = 'barracksType'
    name = Column(String, ForeignKey("buildingType.name", deferrable=True, initially='DEFERRED'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'Barracks'
    }


class WallType(BuildingType):
    """
    Stores which types of walls exist (This table is a child of an ISA/polymorphic relation with BuildingType)
    name: name of the WallType building.
    Every row in this table indicates a building that can be used as a wall building
    """
    __tablename__ = 'wallType'
    name = Column(String, ForeignKey("buildingType.name", deferrable=True, initially='DEFERRED'), primary_key=True)
    defense = Column(Integer, nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'wall'
    }


class TowerType(BuildingType):
    """
    Stores which types of towers exist (This table is a child of an ISA/polymorphic relation with BuildingType)
    name: name of the TowerType building.
    Every row in this table indicates a building that can be used as a tower building
    """
    __tablename__ = 'towerType'
    name = Column(String, ForeignKey("buildingType.name", deferrable=True, initially='DEFERRED'), primary_key=True)
    attack = Column(Integer, nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'tower'
    }


class HouseType(BuildingType):
    """
    Stores which types of houses exist (This table is a child of an ISA/polymorphic relation with BuildingType)
    name: name of the HouseType building.
    Every row in this table indicates a building that can be used as a house building
    """
    __tablename__ = 'houseType'
    name = Column(String, ForeignKey("buildingType.name", deferrable=True, initially='DEFERRED'), primary_key=True)
    residents = Column(Integer, nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'house'
    }


class ProductionBuildingType(BuildingType):
    """
    Stores which types of production buildings exist
    (This table is a child of an ISA/polymorphic relation with BuildingType)

    name: name of the ProductionBuildingType building.
    Every row in this table indicates a building that can be used as a production building, that
    produces certain resources
    """
    __tablename__ = 'productionBuildingType'
    name = Column(String, ForeignKey("buildingType.name", deferrable=True, initially='DEFERRED'), primary_key=True)
    __mapper_args__ = {
        'polymorphic_identity': 'productionBuilding'
    }

    producing_resources = relationship("ProducesResources", back_populates="production_building", lazy='select')


class ProducesResources(Base):
    """
    Stores which resources a production building produces
    Each productionBuildingType has specific resources it produces,
    This table, will store these relations.

    building_name: name of the productionBuildingType
    resource_name: name of the resource we want to produce
    base_production: the base production of this resource, this building produces (resource per hour)
    max_capacity: max amount of this resource that can be stored inside this building without it being collected.
    The resources produced by a productionBuilding can be buffered inside this building, till a certain capacity
    This entry stores its max capacity
    """
    __tablename__ = 'producesResources'
    building_name = Column(String, ForeignKey("productionBuildingType.name", deferrable=True, initially='DEFERRED',
                                              ondelete="cascade"),
                           primary_key=True)
    resource_name = Column(String, ForeignKey("resourceType.name", deferrable=True, initially='DEFERRED',
                                              ondelete="cascade"),
                           primary_key=True)

    base_production = Column(PositiveInteger, nullable=False)
    max_capacity = Column(PositiveInteger, nullable=False)

    production_building = relationship("ProductionBuildingType", back_populates="producing_resources", lazy='select')


class CreationCost(Base):
    """
    Stores the cost to create/ upgrade certain buildings
    Lookup table to define creation prices

    building_name: the name of the building type
    cost_type: resource type of the cost
    cost_amount: how much of the provided resource this would cost
    """

    __tablename__ = "CreationCost"
    building_name = Column(String, ForeignKey("buildingType.name", deferrable=True, initially='DEFERRED'),
                           primary_key=True)

    cost_type = Column(String, ForeignKey("resourceType.name", deferrable=True, initially='DEFERRED'), primary_key=True)
    cost_amount = Column(PositiveInteger, nullable=False)

class CityCosts(Base):
    """
    Stores the costs related to city-related activities.

    activity: The type of activity the cost is associated with, such as 'construction' or 'upgrade'.
    resource_type: The type of resource required, linked via foreign key to a 'resourceType' table.
    cost_amount: The amount of the resource required to complete the activity.
    time_cost: The time required to complete the activity, measured in seconds.
    """
    __tablename__ = "CityCosts"
    activity = Column(String, primary_key=True)
    resource_type = Column(String, ForeignKey("resourceType.name"), primary_key=True)
    time_cost = Column(Integer, nullable=True)
    cost_amount = Column(Integer, nullable=False)

class CityUpdateQueue(Base):
    """
    Queue that holds cities being updated
    city_id: the id number of a city
    start_time: the time at which the update started
    duration: the duration of the update in seconds
    """
    __tablename__ = "CityUpdateQueue"
    city_id = Column(ForeignKey("city.id"), primary_key=True)
    start_time = Column(DateTime, nullable=False)
    duration = Column(Integer)
