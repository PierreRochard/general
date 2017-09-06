import asyncio

import jwt
import websockets


async def hello():
    async with websockets.connect(host + encoded) as websocket:
        while True:
            greeting = await websocket.recv()
            print(greeting)

if __name__ == '__main__':

    payload = {
        'mode': 'rw',
        'channel': 'messages_table_update'
    }

    encoded = jwt.encode(payload, '4S7lR9SnY8g3', algorithm='HS256').decode('utf-8')
    print(encoded)
    host = 'ws://localhost:4545/'
    asyncio.get_event_loop().run_until_complete(hello())
