from confz import FileSource

from .config import APIConfig

config = APIConfig(config_sources=[FileSource("config.yml")])

