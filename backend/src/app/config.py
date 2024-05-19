from confz import BaseConfig, FileSource
from pydantic import SecretStr, DirectoryPath, AnyUrl
from typing import Optional
from enum import Enum


class DBConfig(BaseConfig):
    user: str
    password: SecretStr
    host: str
    port: int
    database: str

    def get_connection_string(self) -> SecretStr:
        return SecretStr(f"postgresql+asyncpg://{self.user}:{self.password.get_secret_value()}@{self.host}:{self.port}/{self.database}")


class LogLevel(Enum):
    NOTSET = "NOTSET"
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class LoggingConfig(BaseConfig):
    path: DirectoryPath
    filename: str
    level: LogLevel
    rotation: str
    retention: str
    format: str


class APIConfig(BaseConfig):
    db: Optional[DBConfig] = None
    CORS_sources: Optional[list[AnyUrl]] = []
    logging: Optional[LoggingConfig] = None
    idle_time: Optional[int] = None

