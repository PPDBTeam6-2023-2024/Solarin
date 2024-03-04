import uvicorn
from confz import FileSource

from .app import init_app, APIConfig


if __name__ == "__main__":
    config = APIConfig(config_sources=FileSource(file='config.yml'))
    uvicorn.run(app=init_app(config), host="0.0.0.0", port=8000)

