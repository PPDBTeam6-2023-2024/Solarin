from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers.authentication.router import router as auth_router
from .routers.chat.router import router as chat_router
from .routers.army.router import router as army_router
from .routers.spawn.router import router as spawn_router
from .database.database import sessionmanager
from .routers.planets.router import router as planet_router
from .routers.logic.router import router as logic_router
from .routers.cityManager.router import router as city_router
from .routers.buildingManagement.router import router as building_router
from .routers.unitManagement.router import router as unit_router
from .routers.trading.router import router as trade_router
from .config import APIConfig
from .customize_logger import CustomizeLogger
from .database.models import *
from .routers.generalRouter import router as general_router

def init_app(config: APIConfig) -> FastAPI:
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
    app.include_router(logic_router)
    app.include_router(city_router)
    app.include_router(planet_router)
    app.include_router(army_router)
    app.include_router(building_router)
    app.include_router(unit_router)
    app.include_router(spawn_router)
    app.include_router(trade_router)
    app.include_router(general_router)

    if config.db:
        sessionmanager.init(config.db.get_connection_string().get_secret_value())

        @app.on_event("shutdown")
        async def shutdown():
            await sessionmanager.close()

    return app
