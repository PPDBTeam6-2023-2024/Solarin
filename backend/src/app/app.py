from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers.authentication.router import router as auth_router
from .routers.chat.router import router as chat_router
from .database.database import db
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
app.include_router(chat_router)


@app.on_event("startup")
async def startup():
    await db.connect(config.db)


@app.on_event("shutdown")
async def shutdown():
    await db.disconnect()
