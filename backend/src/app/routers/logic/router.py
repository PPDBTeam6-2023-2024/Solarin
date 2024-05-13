from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.functions import coalesce
from typing import Union, Annotated

from .schemas import PoliticalStanceInput, PoliticalStanceChange

from ....app.routers.authentication.router import get_my_id, get_db
from ....app.database.database_access.data_access import DataAccess
from ....app.database.exceptions.invalid_action_exception import InvalidActionException
from .maintenance_socket_actions import MaintenanceSocketActions
router = APIRouter(prefix="/logic")


@router.get("/resources")
async def get_resources(user_id: Annotated[int, Depends(get_my_id)], db=Depends(get_db)):
    """
    get all the resources of a user
    """
    data_access = DataAccess(db)
    result = await data_access.ResourceAccess.get_resources(user_id)
    return result


@router.get("/politics")
async def get_political_stance(user_id: Annotated[int, Depends(get_my_id)], db=Depends(get_db)):
    """
    get the political values of a user
    """
    data_access = DataAccess(db)
    result = await data_access.UserAccess.get_politics(user_id)

    return result


@router.post("/update_politics")
async def update_politics(user_id: Annotated[int, Depends(get_my_id)], changes: PoliticalStanceChange, db=Depends(get_db)):
    """
    Update the political values of a user
    :param user_id: the user whose values are changing
    :param changes: the new values as percentage changes
    :param db: Database session dependency
    """
    data_access = DataAccess(db)
    current_stance = await data_access.UserAccess.get_politics(user_id)

    cost = []
    for key, value in changes.Cost.items():
        cost.append((key, value))

    has_resources: bool = await data_access.ResourceAccess.has_resources(user_id, cost)

    if not has_resources:
        raise InvalidActionException("The user does not have enough resources")

    for cost_type in cost:
        await data_access.ResourceAccess.remove_resource(user_id, cost_type[0], cost_type[1])

    # convert to dict using helper function
    current_stance_dict = current_stance

    updated_stance = {}
    for key, value in changes.dict().items():
        if key == "Cost":
            continue
        attr = key.lower()
        change_percent = float(value.replace('%', '')) / 100
        if attr in current_stance_dict:
            updated_value = max(0, min(1, current_stance_dict[attr] + change_percent))
            updated_stance[attr] = updated_value

    await data_access.UserAccess.update_politics(user_id, updated_stance)

    return {"message": "Political stance updated successfully", "new_stance": updated_stance}


@router.websocket("/maintenance")
async def websocket_endpoint(
        websocket: WebSocket, db: AsyncSession = Depends(get_db)
):


    auth_token = websocket.headers.get("Sec-WebSocket-Protocol")

    await websocket.accept(subprotocol=auth_token)

    user_id = get_my_id(auth_token)

    """
    start receiving new requests
    """
    data_access = DataAccess(db)

    maintenance_actions = MaintenanceSocketActions(user_id, data_access, websocket)

    try:
        while True:
            data = await websocket.receive_json()
            if data["type"] == "get_maintenance_cost":
                await maintenance_actions.maintenance_request(data)
            print('action here')

    except WebSocketDisconnect:
        await websocket.close()
