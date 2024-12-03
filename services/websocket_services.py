from fastapi import  WebSocket
from typing import List



class WebSocketManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        print(f"New connection: {websocket.client}")
        print(f"Length of connections: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        print(f"Disconnected: {websocket.client}, remaining: {len(self.active_connections)}")

    async def broadcast(self, message: dict):
        print(f"Broadcasting to {len(self.active_connections)} connections")
        for connection in list(self.active_connections):
            try:
                await connection.send_json(message)
                print(f"Sent message to {connection.client}")
            except Exception as e:
                print(f"Error sending message to {connection.client}: {e}")
                self.disconnect(connection)