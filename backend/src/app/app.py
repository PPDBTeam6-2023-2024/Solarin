from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers.authentication.router import router as auth_router
from .routers.chat.router import router as chat_router
from .routers.logic.router import router as logic_router
from .database.database import sessionmanager
from .config import APIConfig
from .customize_logger import CustomizeLogger
from .database.database_access.developer_access import DeveloperAccess
from .create_tuples import *


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

    if config.db:
        sessionmanager.init(config.db.get_connection_string().get_secret_value())
        sessionmanager.session()
        @app.on_event("startup")
        async def startup():
            # create all types (planets, resources, troops, ...)
            await create_tuples()


        @app.on_event("shutdown")
        async def shutdown():
            await sessionmanager.close()

    return app
