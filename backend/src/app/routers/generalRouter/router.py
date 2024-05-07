from fastapi import APIRouter, Depends, Request

from ...database.database_access.data_access import DataAccess
from typing import Annotated, List
from ..authentication.router import get_my_id
from ...database.database import get_db, AsyncSession


router = APIRouter(prefix="/general", tags=["General"])

"""
Router for managing communication about generals of an army
"""


@router.get("/available_generals")
async def get_cities(
        user_id: Annotated[str, Depends(get_my_id)],
        db=Depends(get_db)
):
    """
    Retrieve all generals a user cna still assign to its army

    """

    data_access = DataAccess(db)
    generals = await data_access.GeneralAccess.get_available_generals(user_id)
    generals = [general.to_scheme() for general in generals]
    return generals


@router.post("/add_general")
async def add_general(
        request: Request,
        user_id: Annotated[str, Depends(get_my_id)],
        db=Depends(get_db)
):
    """
    Assign a general to an army
    """

    data = await request.json()

    army_id = data["army_id"]
    general_name = data["general_name"]

    data_access = DataAccess(db)
    await data_access.GeneralAccess.assign_general(user_id, army_id, general_name)
    await data_access.commit()

    return {"success": True}

