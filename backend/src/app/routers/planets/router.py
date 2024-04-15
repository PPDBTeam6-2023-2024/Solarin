from fastapi.websockets import WebSocket, WebSocketDisconnect

from fastapi import APIRouter, Depends
from typing import Annotated, Tuple, List, Optional

from ..authentication.router import get_my_id
from ...database.database import get_db
from ...database.database_access.data_access import DataAccess
from .connection_manager import ConnectionManager
from .schemas import PlanetOut, Region
from .planet_socket_actions import PlanetSocketActions
router = APIRouter(prefix="/planet", tags=["Planet"])
manager = ConnectionManager()


@router.get("/planets")
async def get_planets(
        user_id: Annotated[int, Depends(get_my_id)],
        db=Depends(get_db)
) -> List[Tuple[int, str]]:
    """
    Retrieve all the existing planets
    """
    data_access = DataAccess(db)
    planets = await data_access.PlanetAccess.get_all_planets()

    return planets


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

    planet_actions = PlanetSocketActions(user_id, planet_id, data_access, connection_pool, websocket)

    if new_conn:
        await planet_actions.load_on_arrive()

    """
    Start the websocket loop
    """
    try:
        while True:
            data = await websocket.receive_json()

            data_type_map = {"get_armies": planet_actions.get_armies,
                             "change_direction": planet_actions.change_directions,
                             "leave_city": planet_actions.leave_city,
                             "create_city": planet_actions.create_city}

            """
            Execute mapped planet socket action function
            """
            planet_action_func = data_type_map.get(data["type"])
            if planet_action_func is not None:
                await planet_action_func(data)

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