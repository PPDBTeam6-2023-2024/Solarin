import json
import math

from ..core.connection_pool import ConnectionPool
from fastapi.websockets import WebSocket
from ...database.database_access.data_access import DataAccess
from ....logic.combat.ArriveCheck import ArriveCheck
import asyncio
import datetime
from ...database.exceptions.invalid_action_exception import InvalidActionException
from ..globalws.router import global_queue


class PlanetSocketActions:
    """
    This class gives structure to the socket action methods
    """

    def __init__(self, user_id: int, planet_id: int, data_access: DataAccess,
                 connection_pool: ConnectionPool, websocket: WebSocket):
        """
        The provided parameters are parameters that stay the same for the entire lifetime of this Object
        """

        self.user_id = user_id
        self.planet_id = planet_id
        self.data_access = data_access
        self.connection_pool = connection_pool

        self.websocket = websocket

    async def get_armies(self, data: json):
        """
        handle the 'get_armies' request from the websocket
        -> Return the armies that are on the planet (at least those not inside a city)
        """
        armies = await self.data_access.ArmyAccess.get_armies_on_planet_extra(planet_id=self.planet_id)
        data = {
            "request_type": data["type"],
            "data": [army.to_dict() | {"alliance": army.alliance, "username": army.username, "speed": army.speed} for army in armies]
        }
        await self.connection_pool.send_personal_message(self.websocket, data)

    async def change_directions(self, data: json):
        """
        handle the 'change_directions' request from the websocket
        -> Let an army change its movement
        """

        army_id = data["army_id"]
        to_x = data["to_x"]
        to_y = data["to_y"]

        """
        change the to location to the position of the city/army
        """
        if data.get("on_arrive", False) and \
                (data["target_id"] != army_id or data["target_type"] in ("attack_city", "enter", "enter_planet")):
            if data["target_type"] in ("attack_city", "enter"):
                to_x, to_y = await self.data_access.CityAccess.get_position(data["target_id"])

            if data["target_type"] in ("attack_army", "merge"):
                target_army = await self.data_access.ArmyAccess.get_army_by_id(data["target_id"])
                to_x = target_army.to_x
                to_y = target_army.to_y

        """
        change the direction
        """
        changed, army = await self.data_access.ArmyAccess.change_army_direction(
            user_id=self.user_id,
            army_id=army_id,
            to_x=to_x,
            to_y=to_y
        )

        """
        Here we will check if some attack target message is added, If so we will set the attack target
        """

        """
        Check that an army is not planning to attack/merge with itself
        """
        if data.get("on_arrive", False) and \
                (data["target_id"] != army_id or data["target_type"] in ("attack_city", "enter", "enter_planet")):
            """
            This dict translated a key to a function (function ptr), which can be used
            """
            target_type_dict = {"attack_city": self.data_access.ArmyAccess.attack_city,
                                "attack_army": self.data_access.ArmyAccess.attack_army,
                                "merge": self.data_access.ArmyAccess.add_merge_armies,
                                "enter": self.data_access.ArmyAccess.add_enter_city,
                                "enter_planet": self.data_access.ArmyAccess.add_enter_planet}

            arrive_func = target_type_dict.get(data["target_type"])

            if arrive_func is not None:
                """
                When the action is invalid we will just not do the action
                """
                try:
                    await arrive_func(army_id, data["target_id"])
                except InvalidActionException:
                    pass

                """
                When we add an attack we need to setup an async check
                """

                asyncio.create_task(
                    self.check_army_combat(army_id, (army.arrival_time - datetime.datetime.utcnow()).total_seconds()))

        if changed:
            await self.connection_pool.broadcast({
                "request_type": "change_direction",
                "data": army.to_dict() | {"alliance": army.alliance, "username": army.username, "speed": army.speed}
            })

    async def leave_planet(self, data: json):
        army_id = data["army_id"]
        owner = await self.data_access.ArmyAccess.get_army_owner(army_id)
        if owner.id == self.user_id:
            await self.data_access.ArmyAccess.leave_planet(army_id)
            await self.data_access.commit()
            await self.connection_pool.broadcast({"request_type": "reload"})

    async def leave_city(self, data: json):
        army_id = data["army_id"]

        owner = await self.data_access.ArmyAccess.get_army_owner(army_id)
        if owner.id == self.user_id:
            await self.data_access.ArmyAccess.leave_city(army_id)
            await self.data_access.commit()
            await self.connection_pool.broadcast({"request_type": "reload"})

    async def check_army_combat(self, army: int, delay):
        """
        This function will wait some time before checking army combat (This function will be called as a asyncio task)
        """
        delay = max(0, delay)
        await asyncio.sleep(delay + 0.4)  # safety wait a 0.4 seconds
        await ArriveCheck.check_arrive(army, self.data_access)
        """
        On reload frontend needs to reload its cities and armies on the map
        """
        await self.data_access.commit()
        await self.connection_pool.broadcast({"request_type": "reload"})

    async def load_on_arrive(self):
        """
        When a new planet websocket is openend, we need to load all our IDLE on arrive events
        So they update directly
        """

        """
        put all old pending in a separate tasks
        """

        pending_on_arrives = await self.data_access.ArmyAccess.get_pending_attacks(self.planet_id)
        tasks = []
        for pending_on_arrive in pending_on_arrives:
            tasks.append(asyncio.create_task(
                self.check_army_combat(pending_on_arrive[0],
                                       (pending_on_arrive[1] - datetime.datetime.utcnow()).total_seconds())))
        return tasks

    async def create_city(self, data: json):
        """
        Create a new city on the position of the army
        """
        army_id = data["army_id"]

        """
        Create the new city
        """

        planet_id, x, y = await self.data_access.ArmyAccess.get_current_position(army_id)

        all_cities = await self.data_access.PlanetAccess.get_planet_cities(self.planet_id)

        """
        check if the city creation is not to close to another city
        """
        min_dis = 2

        for city in all_cities:
            distance = math.sqrt((city.x-x)**2+(city.y-y)**2)
            min_dis = min(min_dis, distance)

        """
        when city to close to another city give feedback notification to user
        """
        if min_dis < 0.06:
            await global_queue.put({"target": self.user_id, "type": "city_to_close"})
            return

        city_id = await self.data_access.CityAccess.create_city(planet_id, self.user_id, x, y)

        await self.data_access.ArmyAccess.enter_city(city_id, army_id)

        await self.data_access.commit()

        await self.connection_pool.broadcast({"request_type": "reload"})