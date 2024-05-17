import uvicorn

from .app import init_app, APIConfig

config = APIConfig()
app = init_app(config)

if __name__ == "__main__":
    uvicorn.run(app=init_app(config), host="0.0.0.0", port=8000)
