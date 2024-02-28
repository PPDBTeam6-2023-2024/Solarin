from sqlalchemy import *

from .database import Base
from sqlalchemy.orm import declarative_base, relationship
from ..schemas import MessageToken


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True, index=True)
    email = Column(String, unique=True)
    username = Column(String, unique=True)
    hashed_password = Column(String)
    faction_name = Column(String, nullable=False, unique=True, default=Sequence("default_faction_name_seq"))
    alliance = Column(String, ForeignKey("alliance.name"))


class Alliance(Base):
    __tablename__ = 'alliance'
    name = Column(String, primary_key=True)
    message_board = Column(Integer, ForeignKey("message_board.bid"), nullable=False)


class Message(Base):
    __tablename__ = 'message'

    mid = Column(Integer, Sequence('message_mid_seq'), primary_key=True)
    sender_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    message_board = Column(Integer, ForeignKey("message_board.bid"), nullable=False)
    create_date_time = Column(TIMESTAMP, nullable=False, default=func.now())
    parent_message_id = Column(Integer, ForeignKey("message.mid"))
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
    __tablename__ = 'message_board'
    bid = Column(Integer, Sequence('message_board_bid_seq'), primary_key=True)
    chat_name = Column(String, nullable=False)


class FriendsOf(Base):
    __tablename__ = 'friends_of'
    user1_id = Column(Integer, ForeignKey("user.id"), primary_key=True)
    user2_id = Column(Integer, ForeignKey("user.id"), primary_key=True)
    message_board = Column(Integer, ForeignKey("message_board.bid"), nullable=False)



class SpaceRegion(Base):
    __tablename__ = 'space_region'
    space_region_id = Column(Integer, Sequence('space_region_id_seq'), primary_key=True)
    name = Column(TEXT, nullable=False, unique=True)


class Planet(Base):
    __tablename__ = 'planet'
    id = Column(Integer, Sequence('planet_id_seq'), primary_key=True)
    name = Column(TEXT, nullable=False, unique=True)
    planet_type = Column(TEXT, ForeignKey("planet_type.type"), nullable=False)
    space_region_id = Column(Integer, ForeignKey("space_region.space_region_id"), nullable=False)


class PlanetType(Base):
    __tablename__ = 'planet_type'
    type = Column(TEXT, primary_key=True)
    description = Column(TEXT)


class PlanetRegion(Base):
    __tablename__ = 'planet_region'
    id = Column(Integer, Sequence('planet_region_id_seq'), primary_key=True)
    planet_id = Column(Integer, ForeignKey("planet.id"), primary_key=True)
    region_type = Column(TEXT, ForeignKey("planet_region_type.region_type"), nullable=False)


class PlanetRegionType(Base):
    __tablename__ = 'planet_region_type'
    region_type = Column(TEXT, primary_key=True)
    description = Column(TEXT)


class City(Base):
    __tablename__ = 'city'

    planet_id = Column(Integer, ForeignKey("planet.id"), primary_key=True)
    region_id = Column(Integer, primary_key=True)
    city_id = Column(Integer, primary_key=True)

    controlled_by = Column(Integer, ForeignKey("user.id"), nullable=False),
    rank = Column(Integer, nullable=False)

    """
    Guarantee a composite Foreign key to access planet Region
    """
    __table_args__ = (ForeignKeyConstraint([planet_id, region_id],
                                           [PlanetRegion.planet_id, PlanetRegion.id]),{})

