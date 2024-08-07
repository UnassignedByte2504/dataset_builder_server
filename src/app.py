from fastapi import FastAPI
from src.api.routes import router as api_router
from src.sockets.sio import sio_app
from src.config.app_settings import AppSettings
import logging

def create_app() -> FastAPI:
    settings = AppSettings()
    logging.basicConfig(level=getattr(logging, settings.log_level))

    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description=settings.app_description,
    )

    # Mount the Socket.IO app
    app.mount("/ws", sio_app)

    app.include_router(api_router, prefix="/api")

    return app

app = create_app()
