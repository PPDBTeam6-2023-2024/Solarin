from fastapi.websockets import WebSocket
from typing import Optional

from ..core.connection_pool import ConnectionPool


class ConnectionManager:
    def __init__(self):
        # dictionary like this -> planetId: connectionPool
        self.planets: dict[int, ConnectionPool] = {}

    async def connect_planet(self, planet_id: int, websocket: WebSocket, sub_protocol: Optional[str]=None) -> ConnectionPool:
        if planet_id not in self.planets:
            self.planets[planet_id] = ConnectionPool()
        con_pool = self.planets[planet_id]
        await con_pool.connect(websocket, sub_protocol)
        return con_pool

    def disconnect_planet(self, planet_id: int, websocket: WebSocket) -> None:
        self.planets[planet_id].disconnect(websocket)
        if self.planets[planet_id].empty():
            del self.planets[planet_id]
