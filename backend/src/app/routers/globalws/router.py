from fastapi import APIRouter, Depends
from fastapi.websockets import WebSocket
import asyncio

from ..authentication.router import get_my_id
from ...database.database import get_db

router = APIRouter(prefix="/globalws", tags=["GlobalWS"])

pool = {}
global_queue = asyncio.Queue()


@router.websocket("/ws")
async def global_ws(websocket: WebSocket, db=Depends(get_db)):
    auth_token = websocket.headers.get("Sec-WebSocket-Protocol")
    user_id = get_my_id(auth_token)

    pool[user_id] = websocket

    await websocket.accept(subprotocol=auth_token)

    try:
        while True:
            msg = await global_queue.get()
            target = msg["target"]
            if target in pool:
                del msg["target"]
                await pool[target].send_json(msg)
    except:
        ...
    finally:
        del pool[user_id]
