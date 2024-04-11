import datetime

from fastapi import APIRouter, Depends
from typing import Annotated, Tuple, List
from fastapi.websockets import WebSocket, WebSocketDisconnect
import asyncio
from fastapi import APIRouter, Depends
from typing import Annotated, Tuple, List, Optional
from ....logic.combat.ArriveCheck import ArriveCheck
from ..authentication.router import get_my_id
from ...database.database import get_db
from ...database.database_access.data_access import DataAccess
from .connection_manager import ConnectionManager
from .schemas import PlanetOut, Region

router = APIRouter(prefix="/planet", tags=["Planet"])

manager = ConnectionManager()


@router.get("/planets")
async def get_planets(
        user_id: Annotated[int, Depends(get_my_id)],
        db=Depends(get_db)
) -> List[Tuple[int, str]]:
    data_access = DataAccess(db)
    planets = await data_access.PlanetAccess.get_all_planets()

    return planets


async def check_army_combat(army: int, delay, da: DataAccess, connection_pool):
    """
    This function will wait some time before checking army combat
    """
    delay = max(0, delay)
    await asyncio.sleep(delay+1)  # safety wait a 1 seconds
    await ArriveCheck.check_arrive(army, da)
    """
    On reload frontend needs to reload its cities and armies on the map
    """
    await connection_pool.broadcast({"request_type": "reload"})


@router.websocket("/ws/{planet_id}")
async def planet_socket(
        websocket: WebSocket,
        planet_id: int,
        db=Depends(get_db)
):
    auth_token = websocket.headers.get("Sec-WebSocket-Protocol")
    user_id = get_my_id(auth_token)

    data_access = DataAccess(db)

    connection_pool, new_conn = await manager.connect_planet(planet_id=planet_id, websocket=websocket, sub_protocol=auth_token)

    """
    We will take pending attacks into account so we can directly update the data
    We only need to do this when a new connection is established
    """
    if new_conn:
        """
        put all old pending in a separate tasks
        """

        pending_attacks = await data_access.ArmyAccess.get_pending_attacks(planet_id)

        for pending_attack in pending_attacks:
            asyncio.create_task(check_army_combat(pending_attack[0], (pending_attack[1] - datetime.datetime.utcnow()).total_seconds(),
                                                  data_access, connection_pool))

    """
    Start the websocket loop
    """
    try:
        while True:
            data = await websocket.receive_json()

            if data["type"] == "get_armies":
                armies = await data_access.ArmyAccess.get_armies_on_planet(planet_id=planet_id)
                data = {
                    "request_type": data["type"],
                    "data": [army.to_dict() for army in armies]
                }
                await connection_pool.send_personal_message(websocket, data)
            elif data["type"] == "change_direction":
                army_id = data["army_id"]
                to_x = data["to_x"]
                to_y = data["to_y"]

                changed, army = await data_access.ArmyAccess.change_army_direction(
                    user_id=user_id,
                    army_id=army_id,
                    to_x=to_x,
                    to_y=to_y
                )

                """
                Here we will check if some attack target message is added, If so we will set the attack target
                """
                if data.get("on_arrive", False) and (data["target_id"] != army_id or
                                                     data["target_type"] in ("attack_city", "enter")):

                    if data["target_type"] == "attack_city":
                        await data_access.ArmyAccess.attack_city(army_id, data["target_id"])
                    elif data["target_type"] == "attack_army":
                        await data_access.ArmyAccess.attack_army(army_id, data["target_id"])
                    elif data["target_type"] == "merge":
                        await data_access.ArmyAccess.add_merge_armies(army_id, data["target_id"])
                    elif data["target_type"] == "enter":
                        await data_access.ArmyAccess.add_enter_city(army_id, data["target_id"])

                    """
                    When we add an attack we need to setup an async check
                    """
                    asyncio.create_task(check_army_combat(army_id, (army.arrival_time-datetime.datetime.utcnow()).total_seconds(),
                                                          data_access, connection_pool))

                if changed:
                    await connection_pool.broadcast({
                        "request_type": "change_direction",
                        "data": army.to_dict()
                    })

            elif data["type"] == "leave_city":
                army_id = data["army_id"]
                # Fetch current coordinates and speed of the army
                owner = await data_access.ArmyAccess.get_army_owner(army_id)
                if owner.id == user_id:
                    await data_access.ArmyAccess.leave_city(army_id)
                    await data_access.commit()
                    await connection_pool.broadcast({"request_type": "reload"})

    except WebSocketDisconnect:
        connection_pool.disconnect(websocket)

@router.get("/regions/{planet_id}")
async def get_planet_regions(
        user_id: Annotated[int, Depends(get_my_id)],
        planet_id: int,
        db=Depends(get_db)
) -> Optional[list[Region]]:
    data_access = DataAccess(db)
    planet = await data_access.PlanetAccess.get_planet(planet_id)

    if not planet:
        return []

    return [
        Region(
            region_type=region.region_type,
            x=region.x,
            y=region.y
        )
        for region in planet.regions
    ]