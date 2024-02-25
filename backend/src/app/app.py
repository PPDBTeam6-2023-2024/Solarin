from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from typing import Annotated
from uuid import UUID
from sqlalchemy import select

from .routers.auth import auth_router, get_my_id
from .models import User
from .database import db
from .config import APIConfig
from .customize_logger import CustomizeLogger

config = APIConfig()

app = FastAPI(title="SolarinAPI", root_path="/api")

if config.logging:
    app.logger = CustomizeLogger.make_logger(config=config.logging)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)


@app.on_event("startup")
async def startup():
    await db.connect(config.db)


@app.on_event("shutdown")
async def shutdown():
    await db.disconnect()

@app.get("/me")
async def me(user_id: Annotated[UUID, Depends(get_my_id)], db=Depends(db.get_db)):
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalars().all()

@app.get("/hello")
async def root():
    return {"message": "Hello World"}
