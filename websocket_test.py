import asyncio
import jwt
import websockets


payload = {
  'mode': 'rw',
  'channel': 'messages'
}

encoded = jwt.encode(payload, '4S7lR9SnY8g3', algorithm='HS256').decode('utf-8')

host = 'ws://localhost:4545/'

async def hello():
    async with websockets.connect(host + encoded) as websocket:

        await websocket.send('hello')

        greeting = await websocket.recv()
        print(greeting)

asyncio.get_event_loop().run_until_complete(hello())