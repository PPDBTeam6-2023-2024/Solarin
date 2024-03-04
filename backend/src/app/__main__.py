import uvicorn
from confz import FileSource

from .app import init_app, APIConfig

config = APIConfig(config_sources=FileSource(file='config.yml'))
app = init_app(config)

if __name__ == "__main__":
    uvicorn.run(app=init_app(config), host="0.0.0.0", port=8000)