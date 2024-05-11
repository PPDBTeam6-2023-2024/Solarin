from sqlalchemy import *
from datetime import datetime

from ..database import Base
from sqlalchemy.orm import relationship
from ...routers.authentication.schemas import BattleStats
from ...routers.army.schemas import ArmySchema, ArmyConsistsOfSchema
from ...routers.buildingManagement.schemas import TrainingQueueEntry
from ...routers.generalRouter.schemas import GeneralScheme, GeneralModifiersScheme
from datetime import timedelta
from ....logic.formula.compute_properties import *

from .domains import Coordinate, PositiveInteger, Percentage

from ..models import *


class Stat(Base):
    """
    Table for all types of stats of an army
    name: name of the stat
    """

    __tablename__ = 'stat'
    name = Column(String, primary_key=True)


class TroopHasStat(Base):
    """
    Association between stats and troop type

    name: name of the stat
    value: stat base value for this troop
    troop_type: type troop associated with this stat
    """

    __tablename__ = 'troopHasStat'
    stat = Column(String, ForeignKey("stat.name", deferrable=True, initially='DEFERRED',
                                     ondelete="cascade"), primary_key=True)

    value = Column(PositiveInteger, nullable=False)
    troop_type = Column(String, ForeignKey("troopType.type", deferrable=True, initially='DEFERRED', ondelete="cascade"),
                        primary_key=True)

    troop = relationship("TroopType", back_populates="stats", lazy='joined')


class TrainingQueue(Base):
    """
    One entry stores the training data of 1 Entry in a trainingQueue,
    The table keeps track of which units need to be trained and in which order

    id: an id to uniquely identify the TrainingQueue, within a buildingInstance
    This table represents a Weak entity. The reason this id is not unique on an absolute level is the following:
    After training a lot of units, the TrainingQueue will have added and removed a lot of entries. Resulting
    In a high Id number, while all the lower numbers do not exist anymore. By having the id as a weak key,
    We will be able to keep our Id relative low.

    building_id: the id of the building (of type BarrackBuilding), that does the training (and has the training queue)
    train_remaining: the remaining training_time, till all units of this Queue entry are trained.
    troop_type: the type of troop we want to train
    rank: the rank of the units we are training
    troop_size: the amount of troops in this queue that still need to be trained
    """
    __tablename__ = 'trainingQueue'
    id = Column(Integer, primary_key=True)
    building_id = Column(Integer, ForeignKey("buildingInstance.id", deferrable=True, initially='DEFERRED',
                                             ondelete="cascade"),
                         primary_key=True)
    train_remaining = Column(PositiveInteger, nullable=False)
    troop_type = Column(String, ForeignKey("troopType.type", deferrable=True, initially='DEFERRED', ondelete="cascade"))
    rank = Column(PositiveInteger, nullable=False)
    training_size = Column(PositiveInteger, nullable=False)

    def toTrainingQueueEntry(self, unit_training_time):
        """
        Convert TrainingQueue Object to a scheme
        """
        return TrainingQueueEntry(
            id=self.id,
            building_id=self.building_id,
            train_remaining=self.train_remaining,
            troop_type=self.troop_type,
            rank=self.rank,
            troop_size=self.training_size,
            unit_training_time=unit_training_time
        )


class TroopType(Base):
    """
    Types of troops that are in the game
    type: the name of the troop
    training_time: time needed to train a single troop of this type
    attack: attack points of this troop
    defense: defense points of this troop
    city_attack: attack points of this troop (for cities)
    city_defense: defense points of this troop (for cities)
    recovery: the recovery points of a unit (decides likeliness units survive combat)
    speed: speed of a unit
    required_rank: rank of a building needed to train this unit
    """

    __tablename__ = 'troopType'
    type = Column(TEXT, primary_key=True)
    training_time = Column(PositiveInteger, nullable=False)
    required_rank = Column(PositiveInteger)

    stats = relationship("TroopHasStat", back_populates="troop", lazy='joined')
    in_consist_of = relationship("ArmyConsistsOf", back_populates="troop", lazy='select')

    @classmethod
    def withData(cls, type_name: str, training_time: timedelta, battle_stats: BattleStats,
                 required_rank: int) -> "TroopType":
        """
        Create a troop type based on the battle stats
        """

        return cls(
            type=type_name,
            training_time=training_time.total_seconds(),
            required_rank=required_rank
        )

    def getStats(self, rank, amount=1):
        """
        Get the stats of this unit type based on the rank and the amount of this type
        'PropertyUtility.getUnitStatsRanked', makes sure the stats depend on the rank of the unit in question
        """
        stats_dict = {}

        for s in self.stats:
            stats_dict.update({s.stat: PropertyUtility.getUnitStatsRanked(s.value, rank) * amount})

        return stats_dict


class TroopRank(Base):
    """
    Stores the rank of the unit for a specific user (if no entry, the rank is 1)
    (because storing an entry for users that do not get far in the game before stopping does not seem efficient)

    troop_type: the type of the troop
    user_id: the user it is associated with
    rank: the current rank of this unit for this user
    """
    __tablename__ = 'troopRank'
    troop_type = Column(TEXT, ForeignKey("troopType.type", deferrable=True, initially='DEFERRED', ondelete="cascade"),
                        primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id", deferrable=True, initially='DEFERRED', ondelete="cascade"),
                     primary_key=True)
    rank = Column(PositiveInteger, default=1)


class TroopTypeCost(Base):
    """
    Stores which resources and how much of them it costs to train a unit

    troop_type: the type of the troop
    resource_type: the type of resource it will cost
    amount: the base amount of this resource training this unit will cost
    """
    __tablename__ = 'troopTypeCost'
    troop_type = Column(TEXT, ForeignKey("troopType.type", deferrable=True, initially='DEFERRED', ondelete="cascade"),
                        primary_key=True)
    resource_type = Column(TEXT, ForeignKey("resourceType.name", deferrable=True, initially='DEFERRED',
                                            ondelete="cascade"),
                           primary_key=True)
    amount = Column(PositiveInteger, nullable=False)


class Army(Base):
    """
    Stores data about an army

    id: unique id of an army
    user_id: id of the user who controls the army
    planet_id: id of the planet the unit is currently on (can be 'null' in case an army is in space)

    Army positions are always shown as 2 points, and a departure and arrival time.
    Based on this information is possible to do a linear interpolation to determine
    the current position of an army

    x,y is the 'from_position'
    to_x, to_y is the 'to_position'
    departure_time, arrival_time are timestamps, indicating when the army changed its movement, and when it
    would arrive on its desired location
    """
    __tablename__ = "army"
    id = Column(Integer, Sequence('army_id_seq'), primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id", deferrable=True, initially='DEFERRED',
                                         ondelete="cascade"), nullable=False)
    planet_id = Column(Integer, ForeignKey("planet.id"), nullable=True)
    departure_time = Column(DateTime(), nullable=True, default=datetime.utcnow)
    arrival_time = Column(DateTime(), nullable=True, default=datetime.utcnow)
    x = Column(Coordinate, nullable=False)
    y = Column(Coordinate, nullable=False)
    to_x = Column(Coordinate, nullable=False)
    to_y = Column(Coordinate, nullable=False)

    consists_of = relationship("ArmyConsistsOf", back_populates="army", lazy='select')
    planet = relationship("Planet", back_populates="armies", lazy='select')

    def to_army_schema(self):
        """
        Converts the army Object to a scheme
        """
        return ArmySchema(id=self.id,
                          user_id=self.user_id,
                          planet_id=self.planet_id,
                          x=self.x,
                          y=self.y)

    def to_dict(self):
        """
        Retrieve the army information as a dictionary
        """
        return {
            "id": self.id,
            "departure_time": self.departure_time.isoformat(),
            "arrival_time": self.arrival_time.isoformat(),
            "owner": self.user_id,
            "x": self.x,
            "y": self.y,
            "to_x": self.to_x,
            "to_y": self.to_y
        }


class ArmyConsistsOf(Base):
    """
    The relation indication which types of units are part of the army and in what quantities

    army_id: the id of the army the troops belong to
    troop_type: the type of troop that belongs to the army
    rank: the rank of these units
    size: the amount of this kind of troop that is in the army
    (makes it store efficient in comparison to having an entry for each troop)
    """
    __tablename__ = "armyConsistsOf"
    army_id = Column(Integer, ForeignKey("army.id", deferrable=True, initially='DEFERRED', ondelete="cascade"),
                     primary_key=True)
    troop_type = Column(String, ForeignKey("troopType.type", deferrable=True, initially='DEFERRED'), primary_key=True)
    rank = Column(PositiveInteger, primary_key=True)
    size = Column(PositiveInteger, nullable=False)

    army = relationship("Army", back_populates="consists_of", lazy='select')
    troop = relationship("TroopType", back_populates="in_consist_of", lazy='select')

    def to_armyconsistsof_schema(self):
        return ArmyConsistsOfSchema(army_id=self.army_id,
                                    troop_type=self.troop_type,
                                    rank=self.rank,
                                    size=self.size)


class OnArrive(Base):
    """
    To attack users IDLE, we will store when a user attacks another user/city, ... when he arrives at that position
    (This table is a parent of an ISA/polymorphic relation)

    army_id: the army that has the OnArrive event (on arrival of this army we will check the event)
    """
    __tablename__ = 'onArrive'
    army_id = Column(Integer, ForeignKey("army.id", deferrable=True, initially='DEFERRED', ondelete="cascade"),
                     primary_key=True)

    """
    TargetType indicates the difference between attacking an army and a city.
    """
    target_type = Column(String, nullable=False)
    __mapper_args__ = {
        'polymorphic_on': target_type
    }


class AttackArmy(OnArrive):
    """
    Stores which other army we might attack when our army arrives at its position
    (This table is a child of an ISA/polymorphic relation OnArrive)

    army_id: the army that has the OnArrive event (on arrival of this army we will check the event)
    target_id: the id of the army we will attack when we arrive
    """
    __tablename__ = 'attackArmy'

    army_id = Column(Integer, ForeignKey("onArrive.army_id", deferrable=True, initially='DEFERRED', ondelete="cascade"),
                     primary_key=True)

    target_id = Column(Integer, ForeignKey("army.id", deferrable=True, initially='DEFERRED'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'army'
    }


class AttackCity(OnArrive):
    """
    Stores which city we might attack when our army arrives at its position
    (This table is a child of an ISA/polymorphic relation OnArrive)

    army_id: the army that has the OnArrive event (on arrival of this army we will check the event)
    target_id: the id of the city we will attack when we arrive
    """
    __tablename__ = 'attackCity'

    army_id = Column(Integer, ForeignKey("onArrive.army_id", deferrable=True, initially='DEFERRED', ondelete="cascade"),
                     primary_key=True)

    target_id = Column(Integer, ForeignKey("city.id", deferrable=True, initially='DEFERRED'), primary_key=True)
    __mapper_args__ = {
        'polymorphic_identity': 'city'
    }


class EnterPlanet(OnArrive):
    """
        Stores which planet we might enter when our fleet arrives at its position
        (This table is a child of an ISA/polymorphic relation OnArrive)

        army_id: the army that has the OnArrive event (on arrival of this army we will check the event)
        target_id: the id of the planet we will enter when we arrive
        """
    __tablename__ = 'enterPlanet'

    army_id = Column(Integer, ForeignKey("onArrive.army_id", deferrable=True, initially='DEFERRED', ondelete="cascade"),
                     primary_key=True)

    target_id = Column(Integer, ForeignKey("planet.id", deferrable=True, initially='DEFERRED', ondelete="cascade"),
                       primary_key=True)

    x = Column(Coordinate, nullable=False)
    y = Column(Coordinate, nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'planet enter'
    }


class EnterCity(OnArrive):
    """
    Stores which city we might enter when our army arrives at its position
    (This table is a child of an ISA/polymorphic relation OnArrive)

    army_id: the army that has the OnArrive event (on arrival of this army we will check the event)
    target_id: the id of the city we will enter when we arrive
    """
    __tablename__ = 'enterCity'

    army_id = Column(Integer, ForeignKey("onArrive.army_id", deferrable=True, initially='DEFERRED', ondelete="cascade"),
                     primary_key=True)

    target_id = Column(Integer, ForeignKey("city.id", deferrable=True, initially='DEFERRED', ondelete="cascade"),
                       primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'city enter'
    }


class MergeArmies(OnArrive):
    """
    Stores which army we merge with when we arrive

    (This table is a child of an ISA/polymorphic relation OnArrive)

    army_id: the army that has the OnArrive event (on arrival of this army we will check the event)
    target_id: the id of the army we will merge with when we arrive.
    """
    __tablename__ = 'mergeArmies'

    army_id = Column(Integer, ForeignKey("onArrive.army_id", deferrable=True, initially='DEFERRED', ondelete="cascade"),
                     primary_key=True)

    target_id = Column(Integer, ForeignKey("army.id", deferrable=True, initially='DEFERRED'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'merge army'
    }


class ArmyInCity(Base):
    """
    Stores the armies that are present inside a city

    army_id: the id of an army that is inside a city
    city_id: the id of the city we are in.
    Only 1 army can be inside a city at the same time
    """
    __tablename__ = 'armyInCity'
    army_id = Column(Integer, ForeignKey("army.id", deferrable=True, initially='DEFERRED', ondelete="cascade"),
                     primary_key=True)

    city_id = Column(Integer, ForeignKey("city.id", deferrable=True, initially='DEFERRED'), nullable=False,
                     unique=True)


class Generals(Base):
    """
    Stores the possible generals that exist

    name: name of the general
    """
    __tablename__ = 'generals'

    name = Column(String, primary_key=True)

    def __hash__(self):
        """
        Make a hash for Generals so 2 generals with same names are the same
        """
        return hash(self.name)

    def to_scheme(self):
        scheme = GeneralScheme(name= self.name)
        return scheme


class ArmyHasGeneral(Base):
    """
    Stores which generals are assigned to which army, each army has maximum 1 general

    general_name: name of the general
    army_id: id of the army the general is associated with
    """
    __tablename__ = 'armyHasGeneral'

    general_name = Column(String, ForeignKey("generals.name", deferrable=True, initially='DEFERRED',
                                             ondelete="cascade"), nullable=False)
    army_id = Column(Integer, ForeignKey("army.id", deferrable=True, initially='DEFERRED', ondelete="cascade"),
                     primary_key=True)


class GeneralModifier(Base):
    """
    Stores the modifier on certain stats based on a general
    General stat values, will also depend on the political direction of the user
    """
    __tablename__ = 'generalModifier'

    stat = Column(String, ForeignKey("stat.name", deferrable=True, initially='DEFERRED',
                                     ondelete="cascade"), primary_key=True)

    general_name = Column(String, ForeignKey("generals.name", deferrable=True, initially='DEFERRED',
                                             ondelete="cascade"), primary_key=True)

    amount = Column(Percentage, nullable=False)

    political_stance = Column(String, ForeignKey("politicalStance.name", deferrable=True, initially='DEFERRED',
                                                 ondelete="cascade"),
                              nullable=False)

    def to_scheme(self, political_stance_modifier: float):

        scheme = GeneralModifiersScheme(stat=self.stat, modifier=self.amount,
                                        political_stance=self.political_stance,
                                        political_stance_modifier=political_stance_modifier)
        return scheme
