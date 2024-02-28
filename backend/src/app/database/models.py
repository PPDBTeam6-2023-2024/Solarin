from sqlalchemy import *
import uuid

from .database import Base
from sqlalchemy.orm import declarative_base, relationship


class User(Base):
    __tablename__ = 'user'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    email = Column(String, unique=True)
    username = Column(String, unique=True)
    hashed_password = Column(String)
    faction_name = Column(String, nullable=False, unique=True, default=Sequence("default_faction_name_seq"))
    clan = Column(String, ForeignKey("clan.name"))

    def __init__(self, email: str, username: str, hashed_password: str):
        self.email = email
        self.username = username
        self.hashed_password = hashed_password


class Clan(Base):
    __tablename__ = 'clan'
    name = Column(String, primary_key=True)
    message_board = Column(Integer, ForeignKey("message_board.bid"), nullable=False)

    def __init__(self, name: str, message_board_id: int):
        self.name = name
        self.message_board = message_board_id


class Message(Base):
    __tablename__ = 'message'

    mid = Column(Integer, Sequence('message_mid_seq'), primary_key=True)
    sender_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
    message_board = Column(Integer, ForeignKey("message_board.bid"), nullable=False)
    create_date_time = Column(TIMESTAMP, nullable=False, default=func.now())
    parent_message_id = Column(Integer, ForeignKey("message.mid"))
    read = Column(BOOLEAN, nullable=False)
    body = Column(TEXT, nullable=False)

    def __init__(self, sender_id: str, message_board: int, body: str, parent_message_id=None):
        self.sender_id = sender_id
        self.message_board = message_board
        self.body = body
        self.read = False
        self.parent_message_id = parent_message_id

class MessageBoard(Base):
    __tablename__ = 'message_board'
    bid = Column(Integer, Sequence('message_board_bid_seq'), primary_key=True)
    chat_name = Column(String, nullable=False)

    def __init__(self, chat_name: str):
        self.chat_name = chat_name


class ReaderOf(Base):
    __tablename__ = 'reader_of'
    board_id = Column(Integer, ForeignKey("message_board.bid"), primary_key=True)
    user_id = Column(UUID, ForeignKey("user.id"), primary_key=True)


class SpaceRegion(Base):
    __tablename__ = 'space_region'
    space_region_id = Column(Integer, Sequence('space_region_id_seq'), primary_key=True)
    name = Column(TEXT, nullable=False, unique=True)


class Planet(Base):
    __tablename__ = 'planet'
    planet_id = Column(Integer, Sequence('planet_id_seq'), primary_key=True)
    name = Column(TEXT, nullable=False, unique=True)
    planet_type = Column(TEXT, ForeignKey("planet_type.type"), nullable=False)
    space_region_id = Column(Integer, ForeignKey("space_region.space_region_id"), nullable=False)


class PlanetType(Base):
    __tablename__ = 'planet_type'
    type = Column(TEXT, primary_key=True)
    description = Column(TEXT)


class PlanetRegion(Base):
    __tablename__ = 'planet_region'
    region_id = Column(Integer, Sequence('planet_region_id_seq'), primary_key=True)
    planet_id = Column(Integer, ForeignKey("planet.planet_id"), primary_key=True)
    region_type = Column(TEXT, ForeignKey("planet_region_type.region_type"), nullable=False)


class PlanetRegionType(Base):
    __tablename__ = 'planet_region_type'
    region_type = Column(TEXT, primary_key=True)
    description = Column(TEXT)


class City(Base):
    __tablename__ = 'city'

    planet_id = Column(Integer, ForeignKey("planet.planet_id"), primary_key=True)
    region_id = Column(Integer, primary_key=True)
    city_id = Column(Integer, primary_key=True)

    controlled_by = Column(UUID, ForeignKey("user.id"), nullable=False),
    rank = Column(Integer, nullable=False)

    """
    Guarantee a composite Foreign key to access planet Region
    """
    __table_args__ = (ForeignKeyConstraint([planet_id, region_id],
                                           [PlanetRegion.planet_id, PlanetRegion.region_id]),{})

