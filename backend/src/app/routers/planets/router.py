from fastapi import APIRouter, Depends
from typing import Annotated, Tuple, List
from fastapi.websockets import WebSocket, WebSocketDisconnect

from ..authentication.router import get_my_id
from ...database.database import get_db
from ...database.database_access.data_access import DataAccess
from .connection_manager import ConnectionManager

router = APIRouter(prefix="/planet", tags=["Planet"])

manager = ConnectionManager()


@router.get("/planets")
async def get_planets(
        user_id: Annotated[int, Depends(get_my_id)],
        db=Depends(get_db)
) -> List[Tuple[int, str]]:
    data_access = DataAccess(db)
    planets = await data_access.PlanetAccess.getAllPlanets()

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

    connection_pool = await manager.connect_planet(planet_id=planet_id, websocket=websocket, sub_protocol=auth_token)

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
                if changed:
                    await connection_pool.broadcast({
                        "request_type": "change_direction",
                        "data": army.to_dict()
                    })
    except WebSocketDisconnect:
        connection_pool.disconnect(websocket)
