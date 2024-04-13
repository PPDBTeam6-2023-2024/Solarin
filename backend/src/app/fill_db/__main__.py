from confz import FileSource
import asyncio
import json
from sqlalchemy.ext.asyncio import AsyncSession

from ..config import APIConfig
from ..database.database import sessionmanager
from ..database.database_access.data_access import DataAccess
from ..routers.spawn.planet_generation import generate_random_planet
from ..routers.authentication.router import pwd_context
from ..database.database_access.message_access import MessageToken
from .create_tuples import CreateTuples


async def fill_db(data: dict):
    config = APIConfig(config_sources=FileSource(file='config.yml'))    
    sessionmanager.init(config.db.get_connection_string().get_secret_value())

    async with sessionmanager.session() as session:
        await CreateTuples().create_all_tuples(session)
        await create_space_regions(data["space regions"], session)
        await create_users(data["users"], session)
        await create_alliances(data["alliances"], session)
        await create_friendships(data["friendships"], session)
        await session.commit()

async def create_space_region(data: dict, session: AsyncSession):
    region_id = await DataAccess(session=session).PlanetAccess.create_space_region(data["name"])
    for _ in range(data["planet count"]):
        await generate_random_planet(session, region_id)
    await session.flush()

async def create_space_regions(data: list[dict], session: AsyncSession):
    for region in data:
        await create_space_region(region, session)
    await session.flush()    

async def create_user(data: dict, session: AsyncSession):
    data_access = DataAccess(session=session)
    user_id = await data_access.UserAccess.create_user(data["userinfo"]["username"], data["userinfo"]["email"], pwd_context.hash(["userinfo"]["password"]))
    # add resources
    for name, amount in data["resources"].items():
        await data_access.ResourceAccess.add_resource(user_id, name, amount)
    # add armies
    for army in data["armies"]:
        army_id = await data_access.ArmyAccess.create_army(user_id, army["planet nr"], army["x"], army["y"])
        for troop in army["troops"]:
            await data_access.ArmyAccess.add_to_army(army_id, troop["type"], troop["rank"], troop["amount"])
    # add cities
    for city in data["cities"]:
        city_id = await data_access.CityAccess.create_city(city["planet nr"], user_id, city["x"], city["y"])
        for building in city["buildings"]:
            await data_access.BuildingAccess.create_building(user_id, city_id, building)
    await session.flush()

async def create_users(data: list[dict], session: AsyncSession):
    for user in data:
        await create_user(user, session)
    await session.flush()


async def create_alliances(data: list[dict], session: AsyncSession):
    data_access = DataAccess(session=session)
    for alliance in data:
        await data_access.AllianceAccess.create_alliance(alliance["name"])
        forward_dict = {}
        for user in alliance["users"]:
            user_id = await data_access.UserAccess.get_user_id_username(user)
            forward_dict[user] = user_id
            await data_access.AllianceAccess.set_alliance(user_id, alliance["name"])
        message_board = await data_access.MessageAccess.get_alliance_message_board(alliance["name"])
        for chat in alliance["chats"]:
            sender_id = forward_dict["sender name"]
            await data_access.MessageAccess.create_message(MessageToken(sender_id, message_board, chat["body"]))
    await session.flush()

async def create_friendships(data: list[dict], session: AsyncSession):
    data_access = DataAccess(session=session)
    for friendship in data:
        forward_dict = {
            friendship["user1"]: await data_access.UserAccess.get_user_id_username(friendship["user1"]),
            friendship["user2"]: await data_access.UserAccess.get_user_id_username(friendship["user2"])
        }
        await data_access.UserAccess.add_friendship(forward_dict["user1"], forward_dict["user2"])
        message_board = await data_access.MessageAccess.get_player_messageBoard(forward_dict[friendship["user1"]], forward_dict[friendship["user2"]])
        for chat in friendship["chats"]:
            sender_id = forward_dict[chat["sender name"]]
            await data_access.MessageAccess.create_message(MessageToken(sender_id, message_board, chat["body"]))


if __name__ == '__main__':
    data = json.loads(open("./data.json"))
    asyncio.run(fill_db(data))
