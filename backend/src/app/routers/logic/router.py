from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.sql.functions import coalesce
from typing import Union, Annotated

from ....app.routers.authentication.router import get_my_id, get_db
from ....app.database.database_access.data_access import DataAccess
router = APIRouter(prefix="/logic")


@router.get("/resources")
async def get_resources(user_id: Annotated[int, Depends(get_my_id)], db=Depends(get_db)):
    """
    get all the resources of a user
    """
    data_access = DataAccess(db)
    result = await data_access.ResourceAccess.get_resources(user_id)
    return result
