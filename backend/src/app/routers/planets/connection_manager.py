from fastapi.websockets import WebSocket
from typing import Optional, Tuple

from ..core.connection_pool import ConnectionPool


class ConnectionManager:
    def __init__(self):
        # dictionary like this -> planetId: connectionPool
        self.planets: dict[int, ConnectionPool] = {}

    async def connect_planet(self, planet_id: int, websocket: WebSocket, sub_protocol: Optional[str]=None) -> Tuple[ConnectionPool, bool]:
        new_conn = False

        if planet_id not in self.planets:
            self.planets[planet_id] = ConnectionPool()
            new_conn = True

        con_pool = self.planets[planet_id]
        await con_pool.connect(websocket, sub_protocol)
        return con_pool, new_conn

    def disconnect_planet(self, planet_id: int, websocket: WebSocket) -> None:
        self.planets[planet_id].disconnect(websocket)
        if self.planets[planet_id].empty():
            del self.planets[planet_id]
