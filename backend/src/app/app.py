from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.app.modules.authentication.router import auth_router
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
