import uvicorn

from . import config
from .app import init_app

if __name__ == "__main__":
    uvicorn.run(app=init_app(config), host="0.0.0.0", port=8000)
