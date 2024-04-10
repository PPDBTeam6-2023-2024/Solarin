from sqlalchemy import *
from datetime import datetime

from ..database import Base
from sqlalchemy.orm import relationship
from ...routers.authentication.schemas import MessageToken, BattleStats
from ...routers.chat.schemas import MessageOut
from ...routers.cityManager.schemas import BuildingInstanceSchema, CitySchema, BuildingTypeSchema
from ...routers.army.schemas import ArmySchema, ArmyConsistsOfSchema
from ...routers.buildingManagement.schemas import TrainingQueueEntry
from datetime import timedelta
from ....logic.utils.compute_properties import *
from .domains import Coordinate


class User(Base):
    """
    Store data of a user their account

    id: unique id to identify the user (uses a sequence to increase the id counter every time a user creates an account)
    email: the email of the user
    username: username of the user
    hashed_password: the password of the user in hashed format
    alliance: the alliance the user is in. (If the user is not in an alliance, this value is 'null')
    faction_name: the name of the faction the user is leading (if 'null', no faction name is yet configured by the user)
    """
    __tablename__ = 'user'
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    username = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    alliance = Column(String, ForeignKey("alliance.name", deferrable=True, initially='DEFERRED', ondelete='SET NULL'))
    faction_name = Column(String)


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
    quantity = Column(Integer, nullable=False, default=0)


class Alliance(Base):
    """
    Store the alliances
    name: name of the alliance
    message_board: message board associated with the alliance, used to store, which chat is dedicated for this alliance
    """
    __tablename__ = 'alliance'
    name = Column(String, primary_key=True)
    message_board = Column(Integer, ForeignKey("messageBoard.bid", deferrable=True, initially='DEFERRED'),
                           nullable=False)


class Message(Base):
    """
    Store the messages
    mid: unique id for the message
    sender_id: id of the user who send the message
    message_board: the message board (chat) the message is send in
    create_date_time: the timestamp the message was created
    body: the content of the message
    """
    __tablename__ = 'message'

    mid = Column(Integer, Sequence('message_mid_seq'), primary_key=True)
    sender_id = Column(Integer, ForeignKey("user.id", deferrable=True, initially='DEFERRED',
                                           ondelete="SET NULL"), nullable=False)
    message_board = Column(Integer, ForeignKey("messageBoard.bid", deferrable=True, initially='DEFERRED',
                                               ondelete="cascade"), nullable=False)
    create_date_time = Column(TIMESTAMP, nullable=False, default=datetime.utcnow())
    body = Column(TEXT, nullable=False)

    @classmethod
    def fromMessageToken(cls, message_token: MessageToken) -> "Message":
        """
        This class loads a MessageToken, to create a Message object
        """
        return cls(
            sender_id=message_token.sender_id,
            message_board=message_token.message_board,
            body=message_token.body

        )

    def toMessageOut(self, sender_name):
        """
        Convert the Message object to a MessageOut (scheme)
        """
        return MessageOut(sender_name=sender_name,
                          created_at=self.create_date_time.strftime("/%d/%m/%Y %H:%M:%S"),
                          body=self.body)


class MessageBoard(Base):
    """
    Each message corresponds to a message board
    This table makes it possible to request sequences
    of messages from an alliance or between players.

    bid: is the message board unique id, to identify this message board
    chat_name: is a name associated with this chat
    """
    __tablename__ = 'messageBoard'
    bid = Column(Integer, Sequence('messageBoard_bid_seq'), primary_key=True)
    chat_name = Column(String, nullable=False)


class FriendsOf(Base):
    """
    Store which users are friends with each other
    when 2 users are friends with each other only 1 entry will be stored

    user1_id: id of the first user
    user2_id: id of the second user
    message_board: the message board (chat) that is used for these 2 players to send direct messages to each other.
    """
    __tablename__ = 'friendsOf'
    user1_id = Column(Integer, ForeignKey("user.id", deferrable=True, initially='DEFERRED',
                                          ondelete="cascade"), primary_key=True)
    user2_id = Column(Integer, ForeignKey("user.id", deferrable=True, initially='DEFERRED',
                                          ondelete="cascade"), primary_key=True)
    message_board = Column(Integer, ForeignKey("messageBoard.bid"), nullable=False)


class SpaceRegion(Base):
    """
    Stores the regions in space

    id: unique id of the space region
    name: name of the region is space
    """
    __tablename__ = 'spaceRegion'
    id = Column(Integer, Sequence('spaceRegion_id_seq'), primary_key=True)
    name = Column(String, nullable=False, unique=True)

    planets = relationship("Planet", back_populates="space_region", lazy='select')


class Planet(Base):
    """
    Stores the planets in the game

    id: unique id to identify the planet
    name: name of the planet
    planet_type: the type of the planet
    space_region_id: the id of the space region the planet belongs to
    created_at: when the planet is created
    """
    __tablename__ = 'planet'
    id = Column(Integer, Sequence('planet_id_seq'), primary_key=True)
    name = Column(TEXT, nullable=False)
    planet_type = Column(TEXT, ForeignKey("planetType.type", deferrable=True, initially='DEFERRED'),
                         nullable=False)
    space_region_id = Column(Integer, ForeignKey("spaceRegion.id", deferrable=True, initially='DEFERRED'),
                             nullable=False)
    created_at = Column(DateTime(), nullable=True, default=datetime.utcnow())

    space_region = relationship("SpaceRegion", back_populates="planets", lazy='select')
    armies = relationship("Army", back_populates="planet", lazy="select")
    regions = relationship("PlanetRegion", back_populates="planet", lazy='selectin')


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

    rank = Column(Integer, nullable=False, default=1)

    region = relationship("PlanetRegion", back_populates="cities", lazy='joined')

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
                          planet_id=self.region.planet_id)


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
    rank = Column(Integer, nullable=False, default=1)

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

    """
    stores when the data about this building is last checked
    """
    last_checked = Column(TIMESTAMP, nullable=True, default=func.now())


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

    base_production = Column(Integer, nullable=False)
    max_capacity = Column(Integer, nullable=False)

    production_building = relationship("ProductionBuildingType", back_populates="producing_resources", lazy='select')


class StoresResources(Base):
    """
    Stores the resources produced in a production building instance


    """
    __tablename__ = 'storesResources'
    building_id = Column(Integer, ForeignKey('buildingInstance.id', deferrable=True, initially='DEFERRED'),
                         primary_key=True)
    resource_type = Column(String, ForeignKey('resourceType.name', deferrable=True, initially='DEFERRED'),
                           primary_key=True)
    amount = Column(Integer, nullable=False, default=0)


class ResourceType(Base):
    """
    Types of resources that are in the game
    name: the name of the resource type
    """
    __tablename__ = 'resourceType'
    name = Column(String, primary_key=True)


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
    army_id: the id of the army we add our units to after they are trained
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
    army_id = Column(Integer, ForeignKey("army.id", deferrable=True, initially='DEFERRED', ondelete="cascade"),
                     nullable=False)
    train_remaining = Column(Integer)
    troop_type = Column(String, ForeignKey("troopType.type", deferrable=True, initially='DEFERRED', ondelete="cascade"))
    rank = Column(Integer)
    training_size = Column(Integer)

    def toTrainingQueueEntry(self, unit_training_time):
        """
        Convert TrainingQueue Object to a scheme
        """
        return TrainingQueueEntry(
            id=self.id,
            building_id=self.building_id,
            army_id=self.army_id,
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
        """
        Create a troop type based on the battle stats
        """
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

    def getStats(self, rank, amount=1):
        """
        Get the stats of this unit type based on the rank and the amount of this type
        'PropertyUtility.getUnitStatsRanked', makes sure the stats depend on the rank of the unit in question
        """
        return {"attack": PropertyUtility.getUnitStatsRanked(self.attack, rank)*amount,
                "defense": PropertyUtility.getUnitStatsRanked(self.defense, rank)*amount,
                "city_attack": PropertyUtility.getUnitStatsRanked(self.city_attack, rank)*amount,
                "city_defense": PropertyUtility.getUnitStatsRanked(self.city_defense, rank)*amount,
                "recovery": PropertyUtility.getUnitStatsRanked(self.recovery, rank)*amount,
                "speed": PropertyUtility.getUnitStatsRanked(self.speed, rank)*amount}

    in_consist_of = relationship("ArmyConsistsOf", back_populates="troop", lazy='select')


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
    rank = Column(Integer, default=1)


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
    amount = Column(Integer, nullable=False)


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
    departure_time = Column(DateTime(), nullable=True, default=datetime.utcnow())
    arrival_time = Column(DateTime(), nullable=True, default=datetime.utcnow())
    x = Column(Coordinate, nullable=False)
    y = Column(Coordinate, nullable=False)
    to_x = Column(Coordinate, nullable=False)
    to_y = Column(Coordinate, nullable=False)
    last_update = Column(TIME)

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
    cost_amount = Column(Integer, nullable=False)


class FriendRequest(Base):
    """
    Stores which users have pending friend requests

    from_user_id: user id of the sender of the friend request
    to_user_id: user id of the receiver of the friend request
    """
    __tablename__ = "FriendRequest"
    from_user_id = Column(Integer, ForeignKey("user.id", deferrable=True, initially='DEFERRED', ondelete="cascade"),
                          primary_key=True)
    to_user_id = Column(Integer, ForeignKey("user.id", deferrable=True, initially='DEFERRED', ondelete="cascade"),
                        primary_key=True)


class AllianceRequest(Base):
    """
    Stores which users asked to join a faction

    user_id: id of the user who asks to join an alliance
    alliance_name: name of the alliance the user wants to join
    """
    __tablename__ = "allianceRequest"
    user_id = Column(Integer, ForeignKey("user.id", deferrable=True, initially='DEFERRED', ondelete="cascade"),
                     primary_key=True)
    alliance_name = Column(String, ForeignKey("alliance.name", deferrable=True, initially='DEFERRED',
                                              ondelete="cascade"), nullable=False)


class AssociatedWith(Base):
    """
    Some region Types are associated with Certain Planet Types
    A region type can only exist on the right type of planet
    To store their relation we use this table
    """
    __tablename__ = 'associatedWith'
    planet_type = Column(String, ForeignKey("planetType.type"), primary_key=True)
    region_type = Column(String, ForeignKey("planetRegionType.region_type"), primary_key=True)


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
