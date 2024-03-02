from sqlalchemy import *

from .database import Base
from sqlalchemy.orm import declarative_base, relationship
from ..schemas import MessageToken, BattleStats
from datetime import timedelta



class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True, index=True)
    email = Column(String, unique=True)
    username = Column(String, unique=True)
    hashed_password = Column(String)
    faction_name = Column(String, nullable=False, unique=True, default=Sequence("user_faction_name_seq"))
    alliance = Column(String, ForeignKey("alliance.name", deferrable=True, initially='DEFERRED'))


class Alliance(Base):
    __tablename__ = 'alliance'
    name = Column(String, primary_key=True)
    message_board = Column(Integer, ForeignKey("messageBoard.bid"), nullable=False)


class Message(Base):
    __tablename__ = 'message'

    mid = Column(Integer, Sequence('message_mid_seq'), primary_key=True)
    sender_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    message_board = Column(Integer, ForeignKey("messageBoard.bid"), nullable=False)
    create_date_time = Column(TIMESTAMP, nullable=False, default=func.now())
    parent_message_id = Column(Integer, ForeignKey("message.mid", deferrable=True, initially='DEFERRED'))
    body = Column(TEXT, nullable=False)

    @classmethod
    def fromMessageToken (cls, message_token: MessageToken) -> "Message":
        return cls(
            sender_id=message_token.sender_id,
            message_board= message_token.message_board,
            body= message_token.body,
            parent_message_id= message_token.parent_message_id

        )


class MessageBoard(Base):
    __tablename__ = 'messageBoard'
    bid = Column(Integer, Sequence('messageBoard_bid_seq'), primary_key=True)
    chat_name = Column(String, nullable=False)


class FriendsOf(Base):
    __tablename__ = 'friendsOf'
    user1_id = Column(Integer, ForeignKey("user.id"), primary_key=True)
    user2_id = Column(Integer, ForeignKey("user.id"), primary_key=True)
    message_board = Column(Integer, ForeignKey("messageBoard.bid"), nullable=False)


class SpaceRegion(Base):
    __tablename__ = 'spaceRegion'
    id = Column(Integer, Sequence('spaceRegion_id_seq'), primary_key=True)
    name = Column(String, nullable=False, unique=True)


class Planet(Base):
    __tablename__ = 'planet'
    id = Column(Integer, Sequence('planet_id_seq'), primary_key=True)
    name = Column(TEXT, nullable=False, unique=True)
    planet_type = Column(TEXT, ForeignKey("planetType.type"), nullable=False)
    space_region_id = Column(Integer, ForeignKey("spaceRegion.id"), nullable=False)


class PlanetType(Base):
    __tablename__ = 'planetType'
    type = Column(TEXT, primary_key=True)
    description = Column(TEXT)


class PlanetRegion(Base):
    __tablename__ = 'planetRegion'
    id = Column(Integer, Sequence('planetRegion_id_seq'), primary_key=True)
    planet_id = Column(Integer, ForeignKey("planet.id"))
    region_type = Column(TEXT, ForeignKey("planetRegionType.region_type"), nullable=False)


class PlanetRegionType(Base):
    __tablename__ = 'planetRegionType'
    region_type = Column(String, primary_key=True)
    description = Column(String)


class City(Base):
    __tablename__ = 'city'

    region_id = Column(Integer, ForeignKey("planetRegion.id"))
    id = Column(Integer, Sequence("city_id_seq"), primary_key=True)
    controlled_by = Column(Integer, ForeignKey("user.id"), nullable=False)

    rank = Column(Integer, nullable=False, default=1)


class BuildingInstance(Base):
    __tablename__ = "buildingInstance"
    id = Column(Integer, Sequence('buildingInstance_id_seq'), primary_key=True, index=True)
    city_id = Column(Integer, ForeignKey("city.id", deferrable=True, initially='DEFERRED'), nullable=False)
    building_type = Column(String, ForeignKey("buildingType.name", deferrable=True, initially='DEFERRED'), nullable=False)
    rank = Column(Integer, nullable=False, default=1)


class BuildingType(Base):
    __tablename__ = 'buildingType'
    name = Column(String, Sequence("buildingType_name_seq"), primary_key=True)


class BarracksType(Base):
    __tablename__ = 'barracksType'
    name = Column(String, ForeignKey("buildingType.name", deferrable=True, initially='DEFERRED'), primary_key=True)
    #required_rank = Column(Integer, nullable=False)
    #resource_cost_type = Column(ForeignKey("resourceType.type"), nullable=False)
    #resource_cost_amount = Column(Integer, nullable=False)


class WallType(Base):
    __tablename__ = 'wallType'
    id = Column(Integer, Sequence("wallType_id_seq"), primary_key=True)
    name = Column(TEXT, nullable=False)
    requiredRank = Column(Integer, nullable=False)
    resource_cost_type = Column(ForeignKey("resourceType.name"),nullable=False)
    resource_cost_amount = Column(Integer,nullable=False)


class TowerType(Base):
    __tablename__ = 'towerType'
    id = Column(Integer, Sequence("towerType_id_seq"), primary_key=True)
    name = Column(TEXT, nullable=False)
    requiredRank = Column(Integer, nullable=False)
    resource_cost_type = Column(ForeignKey("resourceType.name"),nullable=False)
    resource_cost_amount = Column(Integer,nullable=False)


class Wall(Base):
    __tablename__ = 'wall'
    id = Column(String, ForeignKey("buildingType.name"), primary_key=True)
    typeId = Column(Integer, ForeignKey("wallType.id"), nullable=False)
    #towers = relationship("Tower", back_populates="parent")
    defence = Column(Integer, nullable=False)


class Tower(Base):
    __tablename__ = 'tower'
    id = Column(String, ForeignKey("buildingType.name"), primary_key=True)
    type_id = Column(Integer, ForeignKey("towerType.id"), nullable=False)
    attack = Column(Integer, nullable=False)
    #wall = relationship("Wall", back_populates="children")


class HouseType(Base):
    __tablename__ = 'house'
    name = Column(String, ForeignKey("buildingType.name", deferrable=True, initially='DEFERRED'), primary_key=True)
    residents = Column(Integer, nullable=False)


class ProductionBuildingType(Base):
    __tablename__ = 'productionBuildingType'
    name = Column(String, ForeignKey("buildingType.name", deferrable=True, initially='DEFERRED'), primary_key=True)
    base_production = Column(Integer, nullable=False)
    max_capacity = Column(Integer, nullable=False)


class ProducesResources(Base):
    __tablename__ = 'producesResources'
    building_name = Column(String, ForeignKey("productionBuildingType.name", deferrable=True, initially='DEFERRED'), primary_key=True)
    resource_name = Column(String, ForeignKey("resourceType.name", deferrable=True, initially='DEFERRED'), primary_key=True)


class ResourceType (Base):
    __tablename__ = 'resourceType'
    name = Column(String, primary_key=True)


class TrainingQueue(Base):
    __tablename__ = 'trainingQueue'
    id = Column(Integer, primary_key=True)
    building_id = Column(Integer, ForeignKey("buildingInstance.id", deferrable=True, initially='DEFERRED'),
                         primary_key=True)
    army_id = Column(Integer, ForeignKey("army.id", deferrable=True, initially='DEFERRED'), nullable=False)
    train_remaining = Column(Integer)
    troop_type = Column(String, ForeignKey("troopType.type", deferrable=True, initially='DEFERRED'))
    rank = Column(Integer)
    training_size = Column(Integer)
    #barracks = relationship("Barracks", back_populates="trainingQueue")


class TroopType(Base):
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
    def withBattleStats(cls, type_name: str, training_time: timedelta, battle_stats: BattleStats, required_rank: int) -> "TroopType":
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


class TroopTypeCost(Base):
    __tablename__ = 'troopTypeCost'
    troop_type = Column(TEXT, ForeignKey("troopType.type", deferrable=True, initially='DEFERRED'), primary_key=True)
    resource_type = Column(TEXT, ForeignKey("resourceType.name", deferrable=True, initially='DEFERRED'), primary_key=True)
    amount = Column(Integer, nullable=False)


class Army(Base):
    __tablename__ = "army"
    id = Column(Integer, Sequence('army_id_seq'), primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    last_update = Column(TIME)


class ArmyConsistsOf(Base):
    __tablename__ = "armyConsistsOf"
    army_id = Column(Integer, ForeignKey("army.id", deferrable=True, initially='DEFERRED'), primary_key=True)
    troop_type = Column(String, ForeignKey("troopType.type", deferrable=True, initially='DEFERRED'), primary_key=True)
    rank = Column(Integer, primary_key=True)
    size = Column(Integer, nullable=False)
