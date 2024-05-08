from sqlalchemy import *
from datetime import datetime

from ..database import Base
from sqlalchemy.orm import relationship

from .domains import Coordinate

from ..models import *


class Planet(Base):
    """
    Stores the planets in the game

    id: unique id to identify the planet
    name: name of the planet
    planet_type: the type of the planet
    created_at: when the planet is created
    x, y: the position of the planet in space
    visible: if the planet is visible to all players
    """
    __tablename__ = 'planet'
    id = Column(Integer, Sequence('planet_id_seq'), primary_key=True)
    name = Column(TEXT, nullable=False)
    planet_type = Column(TEXT, ForeignKey("planetType.type", deferrable=True, initially='DEFERRED'),
                         nullable=False)
    created_at = Column(DateTime(), nullable=True, default=datetime.utcnow)
    x = Column(FLOAT, nullable=False)
    y = Column(FLOAT, nullable=False)
    visible = Column(Boolean, nullable=False, default=False)

    armies = relationship("Army", back_populates="planet", lazy="select")
    regions = relationship("PlanetRegion", back_populates="planet", lazy='selectin')

    @staticmethod
    def to_dict(row: "Planet") -> dict:
        """
        Convert the planet row object to a dictionary
        """
        return {
            "id": row.id,
            "name": row.name,
            "planet_type": row.planet_type,
            "created_at": row.created_at,
            "x": row.x,
            "y": row.y,
            "visible": row.visible
        }


class PlanetType(Base):
    """
    Stores which types of planets are in the game
    (each planet has a type)
    type: the name of the type
    description: an extra description about the planet type
    """
    __tablename__ = 'planetType'
    type = Column(TEXT, primary_key=True)
    description = Column(TEXT)


class PlanetRegion(Base):
    """
    Stores the region corresponding to a planet
    id: id of the region
    planet_id: id of the planet the region is a part of
    x, y: position indicating a point on the planet.
    using voronoi we can generate regions while only storing 1 point.
    To check which region something belongs too, we just check the closest point
    """
    __tablename__ = 'planetRegion'
    id = Column(Integer, Sequence('planetRegion_id_seq'), primary_key=True)
    planet_id = Column(Integer, ForeignKey("planet.id", deferrable=True, initially='DEFERRED',
                                           ondelete="cascade"))
    region_type = Column(TEXT, ForeignKey("planetRegionType.region_type", deferrable=True, initially='DEFERRED'),
                         nullable=False)
    x = Column(Coordinate, nullable=False)
    y = Column(Coordinate, nullable=False)

    planet = relationship("Planet", back_populates="regions", lazy='joined')
    cities = relationship("City", back_populates="region", lazy='select')


class PlanetRegionType(Base):
    """
    Store all the types a region can be
    region_type: name of the type of the region
    description: an extra description about the region type
    """
    __tablename__ = 'planetRegionType'
    region_type = Column(String, primary_key=True)
    description = Column(String)


class AssociatedWith(Base):
    """
    Some region Types are associated with Certain Planet Types
    A region type can only exist on the right type of planet
    To store their relation we use this table
    """
    __tablename__ = 'associatedWith'
    planet_type = Column(String, ForeignKey("planetType.type"), primary_key=True)
    region_type = Column(String, ForeignKey("planetRegionType.region_type"), primary_key=True)