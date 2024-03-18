from fastapi import APIRouter, Depends, Query

from ...database.database import get_db
from ...database.database_access.army_access import *
from ..authentication.router import get_my_id
from typing import List, Annotated
from .schemas import *

router = APIRouter(prefix="/army", tags=["Army"])


@router.get("/armies", response_model=List[ArmySchema])
async def get_armies(userid: Annotated[int, Depends(get_my_id)], planetid: int) -> List[ArmySchema]:
    armies_db = await ArmyAccess.getArmies(userid, planetid)

    armies = [ArmySchema.from_orm(army) for army in armies_db]
    return armies


@router.get("/troops", response_model=List[ArmyConsistsOfSchema])
async def get_troops(armyid: int):
    troops_db = await ArmyAccess.getTroops(armyid)

    troops = [ArmyConsistsOfSchema.from_orm(troop) for troop in troops_db]

    return troops
