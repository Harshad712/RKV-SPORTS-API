from fastapi import APIRouter,WebSocket
from services.websocket_services import WebSocketManager



app = APIRouter(tags=['sockets'])
websocket_manager = WebSocketManager()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    
    await websocket_manager.connect(websocket)
    try:
        while True:
            message =  await websocket.receive_json()  # Keep the connection alive
            print(f"Received: {message}")
            
            
           
                    
             
    except Exception:
        websocket_manager.disconnect(websocket)


@app.get("/broadcast")
async def broadcast_message():
    await websocket_manager.broadcast({"message": "Hello, WebSocket!"})
    return {"status": "Broadcast completed"}