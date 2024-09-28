from fastapi import WebSocket


class ConnectionManager:
    def __init__(self) -> None:
        self.active_connections: dict[int,WebSocket] = {}

    async def connect(self, websocket: WebSocket,user_id:int):
        await websocket.accept()
        self.active_connections[user_id] = websocket

    def disconnect(self, websocket: WebSocket,user_id:int):
        if user_id in self.active_connections:
            del self.active_connections[user_id]

    async def send_personal_messages(self,msg:str,user_id:int):
        websocket = self.active_connections.get(user_id,None)
        if websocket:
            await websocket.send_text(msg)

    async def broadcast(self, msg: str):
        for connection in self.active_connections.values():
            await connection.send_text(msg)
