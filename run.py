import uvicorn
from src.app import app
from src.config.app_settings import AppSettings

if __name__ == "__main__":
    settings = AppSettings()
    uvicorn.run(app, host=settings.app_host, port=settings.app_port)
