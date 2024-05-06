from fastapi import APIRouter, Depends
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
    print(generals)
    return generals

