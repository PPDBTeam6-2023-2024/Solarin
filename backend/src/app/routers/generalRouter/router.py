from fastapi import APIRouter, Depends
from ...database.database_access.data_access import DataAccess
from typing import Annotated, List
from ..authentication.router import get_my_id
from ...database.database import get_db, AsyncSession


router = APIRouter(prefix="/general", tags=["General"])

"""
Router for managing communication about generals of an army
"""


