from sqlalchemy import *
from datetime import datetime
from sqlalchemy.orm import relationship
from ..database import Base
from ...routers.authentication.schemas import MessageToken
from ...routers.chat.schemas import MessageOut
from ...routers.logic.schemas import ColorCodeScheme

from .domains import Decimal, HexColor

from ..models import *


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

    """
    Stores when the last maintenance check of this user occurred
    """
    last_maintenance_check = Column(TIMESTAMP, nullable=False, default=datetime.utcnow)

    stances = relationship("HasPoliticalStance", back_populates="user", lazy='select')


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
    create_date_time = Column(TIMESTAMP, nullable=False, default=datetime.utcnow)
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


class PoliticalStance(Base):
    """
    Stores which political Ideologies there are
    """
    __tablename__ = "politicalStance"

    name = Column(String, primary_key=True)


class HasPoliticalStance(Base):
    """
    Relation between the user and the political stance

    """
    __tablename__ = "hasPoliticalStance"
    user_id = Column(Integer, ForeignKey("user.id", deferrable=True, initially='DEFERRED', ondelete="cascade"),
                     primary_key=True)

    value = Column(Decimal, nullable=False, default=0)

    stance_name = Column(String, ForeignKey("politicalStance.name",
                                            deferrable=True, initially='DEFERRED', ondelete="cascade"),
                         primary_key=True)

    user = relationship("User", back_populates="stances", lazy='select')


class ColorCodes(Base):
    """
    This table stores which color themes the user has selected
    """
    __tablename__ = "colorCodes"

    user_id = Column(Integer, ForeignKey("user.id", deferrable=True, initially='DEFERRED', ondelete="cascade"),
                     primary_key=True)

    primary_color = Column(HexColor, nullable=False)
    secondary_color = Column(HexColor, nullable=False)
    tertiary_color = Column(HexColor, nullable=False)
    text_color = Column(HexColor, nullable=False)

    def toScheme(self):
        """
        Convert the Object to a scheme
        """
        return ColorCodeScheme(primary_color=self.primary_color, secondary_color=self.secondary_color,
                               tertiary_color=self.tertiary_color, text_color=self.text_color)

