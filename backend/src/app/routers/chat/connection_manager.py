from fastapi.websockets import WebSocket


class ConnectionPool:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    def empty(self) -> bool:
        return len(self.active_connections) == 0

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, data: dict):
        for connection in self.active_connections:
            await connection.send_json(data)


class ConnectionManager:
    def __init__(self):
        # dictionary like this -> boardId: connectionPool
        self.boards: dict[int, ConnectionPool] = {}

    async def connect_board(self, board_id: int, websocket: WebSocket) -> ConnectionPool:
        if board_id not in self.boards:
            self.boards[board_id] = ConnectionPool()
        con_pool = self.boards[board_id]
        await con_pool.connect(websocket)
        return con_pool

    def disconnect_board(self, board_id: int, websocket: WebSocket) -> None:
        self.boards[board_id].disconnect(websocket)
        if self.boards[board_id].empty():
            del self.boards[board_id]

