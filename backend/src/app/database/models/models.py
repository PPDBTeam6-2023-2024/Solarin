import sqlalchemy.orm.state
from sqlalchemy import *

from ..database import Base
from sqlalchemy.orm import declarative_base, relationship, declared_attr

from ...routers.authentication.schemas import MessageToken, BattleStats
from ...routers.chat.schemas import MessageOut
from ...routers.cityManager.schemas import BuildingInstanceSchema, CitySchema
from ...routers.army.schemas import ArmySchema, ArmyConsistsOfSchema
from datetime import timedelta

from sqlalchemy.orm.state import InstanceState


class User(Base):
    """
    Store data of a users account
    """
    __tablename__ = 'user'
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True, index=True)
    email = Column(String, unique=True)
    username = Column(String, unique=True)
    hashed_password = Column(String)
    alliance = Column(String, ForeignKey("alliance.name", deferrable=True, initially='DEFERRED'))
    faction_name = Column(String)


class HasResources(Base):
    """
    Store resources of a user
    """
    __tablename__ = "hasResources"
    owner_id = Column(Integer, ForeignKey("user.id"), primary_key=True)
    resource_type = Column(String, ForeignKey("resourceType.name"), primary_key=True)
    quantity = Column(Integer, nullable=False, default=0)


class Alliance(Base):
    """
    Store the alliances
    """
    __tablename__ = 'alliance'
    name = Column(String, primary_key=True)
    message_board = Column(Integer, ForeignKey("messageBoard.bid"), nullable=False)


class Message(Base):
    """
    Store the messages
    """
    __tablename__ = 'message'

    mid = Column(Integer, Sequence('message_mid_seq'), primary_key=True)
    sender_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    message_board = Column(Integer, ForeignKey("messageBoard.bid"), nullable=False)
    create_date_time = Column(TIMESTAMP, nullable=False, default=func.now())
    parent_message_id = Column(Integer, ForeignKey("message.mid", deferrable=True, initially='DEFERRED'))
    body = Column(TEXT, nullable=False)

    @classmethod
    def fromMessageToken(cls, message_token: MessageToken) -> "Message":
        return cls(
            sender_id=message_token.sender_id,
            message_board=message_token.message_board,
            body=message_token.body,
            parent_message_id=message_token.parent_message_id

        )

    def toMessageOut(self, sender_name):
        return MessageOut(sender_name=sender_name,
                          created_at=self.create_date_time.strftime("/%d/%m/%Y %H:%M:%S"),
                          body=self.body)


class MessageBoard(Base):
    """
    Each message corresponds to a message board
    This table makes it possible to request sequences
    of messages from an alliance or between players.
    """
    __tablename__ = 'messageBoard'
    bid = Column(Integer, Sequence('messageBoard_bid_seq'), primary_key=True)
    chat_name = Column(String, nullable=False)


class FriendsOf(Base):
    """
    Store which users are friends with each other
    """
    __tablename__ = 'friendsOf'
    user1_id = Column(Integer, ForeignKey("user.id"), primary_key=True)
    user2_id = Column(Integer, ForeignKey("user.id"), primary_key=True)
    message_board = Column(Integer, ForeignKey("messageBoard.bid"), nullable=False)


class SpaceRegion(Base):
    """
    Stores the regions in space
    """
    __tablename__ = 'spaceRegion'
    id = Column(Integer, Sequence('spaceRegion_id_seq'), primary_key=True)
    name = Column(String, nullable=False, unique=True)

    planets = relationship("Planet", back_populates="space_region", lazy='select')


class Planet(Base):
    """
    Stores the planets in the game
    """
    __tablename__ = 'planet'
    id = Column(Integer, Sequence('planet_id_seq'), primary_key=True)
    name = Column(TEXT, nullable=False)
    planet_type = Column(TEXT, ForeignKey("planetType.type"), nullable=False)
    space_region_id = Column(Integer, ForeignKey("spaceRegion.id"), nullable=False)

    space_region = relationship("SpaceRegion", back_populates="planets", lazy='select')
    regions = relationship("PlanetRegion", back_populates="planet", lazy='select')


class PlanetType(Base):
    """
    Stores which types of planets are in the game
    (each planet has a type)
    """
    __tablename__ = 'planetType'
    type = Column(TEXT, primary_key=True)
    description = Column(TEXT)


class PlanetRegion(Base):
    """
    Stores the region corresponding to a planet
    """
    __tablename__ = 'planetRegion'
    id = Column(Integer, Sequence('planetRegion_id_seq'), primary_key=True)
    planet_id = Column(Integer, ForeignKey("planet.id"))
    region_type = Column(TEXT, ForeignKey("planetRegionType.region_type"), nullable=False)

    planet = relationship("Planet", back_populates="regions", lazy='joined')
    cities = relationship("City", back_populates="region", lazy='select')


class PlanetRegionType(Base):
    """
    Store all the types a region can be
    """
    __tablename__ = 'planetRegionType'
    region_type = Column(String, primary_key=True)
    description = Column(String)


class City(Base):
    """
    Stores information about a city that is in a region on a planet
    x and y represent the planetary coordinates of the city
    """
    __tablename__ = 'city'

    region_id = Column(Integer, ForeignKey("planetRegion.id"))
    id = Column(Integer, Sequence("city_id_seq"), primary_key=True)
    controlled_by = Column(Integer, ForeignKey("user.id"), nullable=False)
    x = Column(Float(precision=53), nullable=False)
    y = Column(Float(precision=53), nullable=False)

    rank = Column(Integer, nullable=False, default=1)

    region = relationship("PlanetRegion", back_populates="cities", lazy='joined')

    def to_city_schema(self):
        return CitySchema(id=self.id,
                          region_id=self.region_id,
                          controlled_by=self.controlled_by,
                          x=self.x,
                          y=self.y,
                          rank=self.rank,
                          region_type=self.region.region_type,
                          planet_name=self.region.planet.name,
                          planet_id=self.region.planet_id)


class BuildingInstance(Base):
    """
    Stores which buildings a city has
    """
    __tablename__ = "buildingInstance"
    id = Column(Integer, Sequence('buildingInstance_id_seq'), primary_key=True, index=True)
    city_id = Column(Integer, ForeignKey("city.id", deferrable=True, initially='DEFERRED'), nullable=False)
    building_type = Column(String, ForeignKey("buildingType.name", deferrable=True, initially='DEFERRED'),
                           nullable=False)
    rank = Column(Integer, nullable=False, default=1)

    """
    This relation is joined, because when we ask for an instance we will often also be interested in the type its attributes
    """
    type = relationship("BuildingType", back_populates="instances", lazy='joined')

    def to_pydantic(self) -> BuildingInstanceSchema:
        return BuildingInstanceSchema.from_orm(self)
    def to_BuildingOverview(self, building_id: int, city_id_nr: int, building_type_name: str,
                            rank_nr: int) -> "BuildingInstanceSchema":
        return BuildingInstanceSchema(
            id=building_id,
            city_id=city_id_nr,
            building_type=building_type_name,
            rank=rank_nr
        )


class BuildingType(Base):
    """
    Stores the types of buildings that can exist (This table is the parent of an ISA/polymorphic relation)
    """
    __tablename__ = 'buildingType'
    name = Column(String, Sequence("buildingType_name_seq"), primary_key=True)

    type = Column(String, nullable=False)
    required_rank = Column(Integer)
    __mapper_args__ = {
        'polymorphic_on': type
    }

    """
    This relation is NOT joined, in comparison to its corresponding relation, because we don't always 
    need all the instances of the type 
    """
    instances = relationship("BuildingInstance", back_populates="type", lazy='select')


class BarracksType(BuildingType):
    """
    Stores which types of barracks exist (This table is a child of an ISA/polymorphic relation with BuildingType)
    """
    __tablename__ = 'barracksType'
    name = Column(String, ForeignKey("buildingType.name", deferrable=True, initially='DEFERRED'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'Barracks'
    }


class WallType(BuildingType):
    """
    Stores which types of walls exist (This table is a child of an ISA/polymorphic relation with BuildingType)
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
    """
    __tablename__ = 'houseType'
    name = Column(String, ForeignKey("buildingType.name", deferrable=True, initially='DEFERRED'), primary_key=True)
    residents = Column(Integer, nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'house'
    }


class ProductionBuildingType(BuildingType):
    """
    Stores which types of production buildings exist (This table is a child of an ISA/polymorphic relation with BuildingType)
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
    """
    __tablename__ = 'producesResources'
    building_name = Column(String, ForeignKey("productionBuildingType.name", deferrable=True, initially='DEFERRED'),
                           primary_key=True)
    resource_name = Column(String, ForeignKey("resourceType.name", deferrable=True, initially='DEFERRED'),
                           primary_key=True)

    base_production = Column(Integer, nullable=False)
    max_capacity = Column(Integer, nullable=False)


    production_building = relationship("ProductionBuildingType", back_populates="producing_resources", lazy='select')


class ResourceType(Base):
    """
    Types of resources that are in the game
    """
    __tablename__ = 'resourceType'
    name = Column(String, primary_key=True)


class TrainingQueue(Base):
    """
    One entry stores the training data of 1 Entry in a trainingQueue,
    The table keeps track of which units need to be trained and in which order
    """
    __tablename__ = 'trainingQueue'
    id = Column(Integer, primary_key=True)
    building_id = Column(Integer, ForeignKey("buildingInstance.id", deferrable=True, initially='DEFERRED'),
                         primary_key=True)
    army_id = Column(Integer, ForeignKey("army.id", deferrable=True, initially='DEFERRED'), nullable=False)
    train_remaining = Column(Integer)
    troop_type = Column(String, ForeignKey("troopType.type", deferrable=True, initially='DEFERRED'))
    rank = Column(Integer)
    training_size = Column(Integer)


class TroopType(Base):
    """
    Types of troops that are in the game
    """
    __tablename__ = 'troopType'
    type = Column(TEXT, primary_key=True)
    training_time = Column(Integer, nullable=False)
    attack = Column(Integer, nullable=False)
    defense = Column(Integer, nullable=False)
    city_attack = Column(Integer, nullable=False)
    city_defense = Column(Integer, nullable=False)
    recovery = Column(Integer, nullable=False)
    speed = Column(Integer, nullable=False)
    required_rank = Column(Integer)

    @classmethod
    def withBattleStats(cls, type_name: str, training_time: timedelta, battle_stats: BattleStats,
                        required_rank: int) -> "TroopType":
        return cls(
            type=type_name,
            training_time=training_time.total_seconds(),
            attack=battle_stats.attack,
            defense=battle_stats.defense,
            city_attack=battle_stats.city_attack,
            city_defense=battle_stats.city_defense,
            recovery=battle_stats.recovery,
            speed=battle_stats.speed,
            required_rank=required_rank
        )

    in_consist_of = relationship("ArmyConsistsOf", back_populates="troop", lazy='select')


class TroopTypeCost(Base):
    """
    Stores which resources and how much of them it costs to train a unit
    """
    __tablename__ = 'troopTypeCost'
    troop_type = Column(TEXT, ForeignKey("troopType.type", deferrable=True, initially='DEFERRED'), primary_key=True)
    resource_type = Column(TEXT, ForeignKey("resourceType.name", deferrable=True, initially='DEFERRED'),
                           primary_key=True)
    amount = Column(Integer, nullable=False)


class Army(Base):
    """
    Stores data about an army
    """
    __tablename__ = "army"
    id = Column(Integer, Sequence('army_id_seq'), primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    last_update = Column(TIME)
    x = Column(Float(precision=53), nullable=False)
    y = Column(Float(precision=53), nullable=False)

    consists_of = relationship("ArmyConsistsOf", back_populates="army", lazy='select')

    def to_army_schema(self):
        return ArmySchema(id=self.id,
                          user_id=self.user_id,
                          last_update=str(self.last_update),
                          x=self.x,
                          y=self.y)


class ArmyConsistsOf(Base):
    """
    The relation indication which types of units are part of the army and in what quantities
    """
    __tablename__ = "armyConsistsOf"
    army_id = Column(Integer, ForeignKey("army.id", deferrable=True, initially='DEFERRED'), primary_key=True)
    troop_type = Column(String, ForeignKey("troopType.type", deferrable=True, initially='DEFERRED'), primary_key=True)
    rank = Column(Integer, primary_key=True)
    size = Column(Integer, nullable=False)

    army = relationship("Army", back_populates="consists_of", lazy='select')
    troop = relationship("TroopType", back_populates="in_consist_of", lazy='select')

    def to_armyconsistsof_schema(self):
        return ArmyConsistsOfSchema(army_id=self.army_id,
                                    troop_type=self.troop_type,
                                    rank=self.rank,
                                    size=self.size)


class CreationCost(Base):
    """
    Stores the cost to create certain buildings
    Lookup table to define creation prices
    """

    __tablename__ = "CreationCost"
    building_name = Column(String, ForeignKey("buildingType.name", deferrable=True, initially='DEFERRED'),
                           primary_key=True)

    cost_type = Column(String, ForeignKey("resourceType.name", deferrable=True, initially='DEFERRED'), primary_key=True)
    cost_amount = Column(Integer, nullable=False)


class FriendRequest(Base):
    """
    Stores which users have pending friend requests
    """
    __tablename__ = "FriendRequest"
    from_user_id = Column(Integer, ForeignKey("user.id"), primary_key=True)
    to_user_id = Column(Integer, ForeignKey("user.id"), primary_key=True)


class AllianceRequest(Base):
    """
    Stores which users asked to join a faction
    """
    __tablename__ = "allianceRequest"
    user_id = Column(Integer, ForeignKey("user.id"), primary_key=True)
    alliance_name = Column(String, ForeignKey("alliance.name"), nullable=False)

