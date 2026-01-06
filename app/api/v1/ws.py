from fastapi import APIRouter, WebSocket, WebSocketDisconnect

router = APIRouter()
connections: list[WebSocket] = []

@router.websocket("/ws/listings")
async def websocket_listings(websocket: WebSocket):
    await websocket.accept()
    connections.append(websocket)
    try:
        while True:
            await websocket.receive_text()  # just keep the connection alive
    except WebSocketDisconnect:
        connections.remove(websocket)

# Helper function to broadcast new listings
async def broadcast_new_listing(listing):
    for connection in connections:
        await connection.send_json(listing)
