import asyncio
import websockets

class PlayerState():
    def __init__():
        self.actions = []
        self.length = 0
        self.position = None


state = {
    'players': []
}
initialState = state

async def restart_game(websocket):
    websockets.broadcast('reset')

async def server_app(websocket):
    async for message in websocket:
        await websocket.send(message)


async def main():
    async with websockets.serve(server_app, "localhost", 8765):
        await asyncio.Future()  # run forever

asyncio.run(main())