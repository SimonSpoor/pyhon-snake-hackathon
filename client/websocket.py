import websockets

async def start_server():
    async with websockets.connect("ws://localhost:6969") as websocket:
        await websocket.send("")