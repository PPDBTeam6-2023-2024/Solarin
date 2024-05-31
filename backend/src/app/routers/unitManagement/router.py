from fastapi import APIRouter, Depends, Query, Request, WebSocket

from ...database.database_access.data_access import DataAccess
from typing import Annotated, Tuple, List
from ..authentication.router import get_my_id
from ...database.database import get_db, AsyncSession
from ...database.models import *

router = APIRouter(prefix="/unit", tags=["City"])


@router.get("/train_cost/{unit_type}/{building_id}")
async def get_buildings(
        user_id: Annotated[int, Depends(get_my_id)],
        building_id: int,
        unit_type: str,
        db=Depends(get_db)
):
    """
    This endpoint will give back the training cost of a unit, based on the rank of the unit the user has
    """

    da = DataAccess(db)

    rank = await da.BuildingAccess.get_building_rank(building_id)
    cost_list = await da.TrainingAccess.get_troop_cost(unit_type, rank)
    return cost_list


@router.post("/train/{building_id}")
async def get_buildings(
        user_id: Annotated[int, Depends(get_my_id)],
        request: Request,
        building_id: int,
        db=Depends(get_db)
):
    """
    This endpoint will give back the training cost of a unit, based on the rank of the unit the user has

    The output format is a dict with 3 attributes:
    queue: proving the current building queue
    success: provides whether the get request was a success
    message: the message for the user
    """

    data = await request.json()
    da = DataAccess(db)
    troop_type = data["type"]
    amount = int(data["amount"])

    """
    check if the user owns the building
    """
    is_owner = await da.BuildingAccess.is_owner(user_id, building_id)
    if not is_owner:
        return {"queue": [], "success": False, "message":
                "Only the owner of this building can change its training queue"}

    rank = await da.BuildingAccess.get_building_rank(building_id)
    cost_list = await da.TrainingAccess.get_troop_cost(troop_type, rank)
    cost_list = [(c[0], c[1]*amount) for c in cost_list]
    has_resources = await da.ResourceAccess.has_resources(user_id, cost_list)
    if not has_resources:
        training_queue: List[TrainingQueue] = await da.TrainingAccess.get_queue(building_id)

        output = [t[0].toTrainingQueueEntry(t[1]) for t in training_queue]
        return {"queue": output, "success": False, "message":
                "User does not have the right amount of the needed resources"}

    """
    Remove the resources
    """
    for c in cost_list:
        await da.ResourceAccess.remove_resource(user_id, c[0], c[1])

    """
    re-check current training progress
    """
    await da.TrainingAccess.check_queue(building_id)
    await da.BuildingAccess.checked(building_id)
    await da.commit()

    rank = await da.BuildingAccess.get_building_rank(building_id)

    await da.TrainingAccess.train_type(building_id, troop_type, rank, amount)
    await da.commit()

    """
    return all the training queue entries, combined with a status and message indicating 
    if the training was successfully
    """
    training_queue: List[TrainingQueue] = await da.TrainingAccess.get_queue(building_id)

    output = [t[0].toTrainingQueueEntry(t[1]) for t in training_queue]
    return {"queue": output, "success": True, "message": ""}


@router.websocket("/ws/city_troops/{city_id}")
async def websocket_endpoint(websocket: WebSocket, city_id: int, db=Depends(get_db)):
    """
    This websocket will provide the user with the current troops in a city
    Firstly it will send all the troops that are currently in the city.
    Then it will send updates when a new troop is trained
    """
    auth_token = websocket.headers.get("Sec-WebSocket-Protocol")
    user_id = get_my_id(auth_token)
    await websocket.accept(subprotocol=auth_token)

    # no connection manager needed because this is a simple p2p connection

    data_access = DataAccess(db)

    try:
        # send all the troops that are currently in the city
        army_id = await data_access.ArmyAccess.get_army_in_city(city_id)
        troops = await data_access.ArmyAccess.get_troops(army_id)
        troops = [t.to_armyconsistsof_schema().model_dump() for t in troops]
        await websocket.send_json({"troops": troops})
        # send updates when a new troop is trained
        training_queue = await data_access.TrainingAccess.get_queue(city_id)
        while True:

            await websocket.send_json(troops)
    except Exception as e:
        pass
