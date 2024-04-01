from fastapi.websockets import WebSocket
from typing import Optional


class ConnectionPool:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    def empty(self) -> bool:
        return len(self.active_connections) == 0

    async def connect(self, websocket: WebSocket, subprotocol: Optional[str] = None):
        await websocket.accept(subprotocol=subprotocol)
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, data):
        for connection in self.active_connections:
            await connection.send_json(data)

    @staticmethod
    async def send_personal_message(websocket: WebSocket, data):
        await websocket.send_json(data)


