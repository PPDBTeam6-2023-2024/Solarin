from fastapi.websockets import WebSocket
from typing import Optional, Tuple

from ..core.connection_pool import ConnectionPool


class ConnectionManager:
    def __init__(self):
        # dictionary like this -> Alliance name: connectionPool
        self.alliance_map: dict[str, ConnectionPool] = {}

    async def connect_trade_board(self, alliance_name: str, websocket: WebSocket, sub_protocol: Optional[str]=None) -> Tuple[ConnectionPool, bool]:
        new_conn = False

        if alliance_name not in self.alliance_map:
            self.alliance_map[alliance_name] = ConnectionPool()
            new_conn = True

        con_pool = self.alliance_map[alliance_name]
        await con_pool.connect(websocket, sub_protocol)
        return con_pool, new_conn

    def disconnect_planet(self, alliance_name: str, websocket: WebSocket) -> None:
        self.alliance_map[alliance_name].disconnect(websocket)
        if self.alliance_map[alliance_name].empty():
            del self.alliance_map[alliance_name]
