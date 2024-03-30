from fastapi.websockets import WebSocket
from typing import Optional

from ..core.connection_pool import ConnectionPool


class ConnectionManager:
    def __init__(self):
        # dictionary like this -> boardId: connectionPool
        self.boards: dict[int, ConnectionPool] = {}

    async def connect_board(self, board_id: int, websocket: WebSocket, sub_protocol: Optional[str]=None) -> ConnectionPool:
        if board_id not in self.boards:
            self.boards[board_id] = ConnectionPool()
        con_pool = self.boards[board_id]
        await con_pool.connect(websocket, sub_protocol)
        return con_pool

    def disconnect_board(self, board_id: int, websocket: WebSocket) -> None:
        self.boards[board_id].disconnect(websocket)
        if self.boards[board_id].empty():
            del self.boards[board_id]

