from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.sql.functions import coalesce
from typing import Union, Annotated

from src.app.database.models import HasResources, ResourceType
from src.app.routers.authentication.router import get_my_id, get_db

router = APIRouter(prefix="/logic")
@router.get("/resources")
async def get_resources(user_id: Annotated[int, Depends(get_my_id)], db=Depends(get_db)):
    user_resources = await db.execute(select(HasResources).where(HasResources.owner_id == user_id))
    resources = await db.execute(select(ResourceType))
    result: dict[str, int] = {}

    for user_resource in user_resources.scalars().all():
        result[user_resource.resource_type] = user_resource.quantity

    for resource in resources.scalars().all():
        result[resource.name] = 0 if not result.get(resource.name, False) else result[resource.name]
    return result
